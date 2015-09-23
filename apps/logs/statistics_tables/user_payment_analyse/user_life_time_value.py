# -*- coding:utf-8 -*-


"""
    用户终身价值
开始日期	20101101	结束日期	20101101
分区查询	总/1区/2区	（默认总数、下拉菜单手动选择区服）
渠道标示	UC/91	（默认总数、下拉菜单手动选择渠道）				注：用户终身价值待商定


LTV	用户终身价值	某日新注册用户N人，他们在第M天的LTV值，即这N个人在这M天中的总充值额/N。（每天都分开算）


日期	新增登录用户	LTV-1	LTV-2	LTV-3	LTV-4	LTV-5	LTV-6	LTV-7	……	LTV15	LTV30	LTV60
2013/11/20	1000	10	11	12	13	14	15	16	17	18	19
2013/11/21	1000	10	11	12	13	14	15	16	17	18	19
2013/11/22	1000	10	11	12	13	14	15	16	17	18	19
2013/11/23	1000	10	11	12	13	14	15	16	17	18	19
2013/11/24	1000	10	11	12	13	14	15	16	17	18	19
2013/11/25	1000	10	11	12	13	14	15	16	17	18	19
2013/11/26	1000	10	11	12	13	14	15	16	17	18	19
2013/11/27	1000	10	11	12	13	14	15	16	17	18	19
2013/11/28	1000	10	11	12	13	14	15	16	17	18	19
2013/11/29	1000	10	11	12	13	14	15	16	17	18	19
PS：本表人数均取角色数
"""

import datetime
import time
from apps.logs import daily_log_dat
from apps.utils import game_define
from apps.game_manager.util import mysql_util


def get_table(search_start_date, search_end_date, channel_id=-1, server_id=-1):
    """
        获取表格
    """
    # 获取搜索区间日志
    today_data = time.localtime()
    today = datetime.datetime(today_data.tm_year, today_data.tm_mon, today_data.tm_mday)
    search_total_day = (search_end_date - search_start_date).days
    table_lst = []
    for i in xrange(search_total_day + 1):
        _register_date = search_start_date + datetime.timedelta(days=1 * i)
        date_str = "_" + _register_date.strftime('%Y%m%d')
        # 获取当天日志
        # _row_log_lst = mysql_util.get_role_action_lst('EVENT_ACTION_ROLE_LOGIN'+str(date_str), _search_date, _search_date, channel_id, server_id, None, None)
        # 获取新用户日志
        # new_user_lst = daily_log_dat.get_set_with_key(_row_log_lst, 'uid',  function=lambda log: log['install'] == _search_date)
        # new_user_num = len(new_user_lst)
        new_user_num = mysql_util.get_today_new_num('uid', 'EVENT_ACTION_ROLE_LOGIN' + str(date_str), _register_date,
                                                    channel_id, server_id)
        # print new_user_num  获取新增登录用户
        ltv_day_lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 30, 60]
        ltv_val_lst = []
        for ltv_days in ltv_day_lst:

            # start_date + ltv_day_lst  if > today  return ltv_val_lst.append('-')


            start_date = _register_date
            end_date = _register_date + datetime.timedelta(days=ltv_days)
            total_recharge_money = 0
            for _day in xrange((end_date - start_date).days):
                search_date = start_date + datetime.timedelta(days=_day)
                date_str = "_" + search_date.strftime('%Y%m%d')
                total_recharge_money += mysql_util.get_install_recharge_sum('add_rmb', _register_date,
                                                                            'EVENT_ACTION_RECHARGE_PLAYER' + str(
                                                                                date_str), channel_id, server_id, None)

                # total_recharge_money += daily_log_dat.get_sum_int_with_key(ltv_recharge_log_lst, 'add_rmb')

            ltv_val = _get_ltv_value(new_user_num, total_recharge_money)
            ltv_val_lst.append(ltv_val)
            today = str(today).split(' ')[0]

            start_day = datetime.datetime(int(str(start_date).split('-')[0]),
                                          int(str(start_date).split('-')[1]),
                                          int(str(start_date).split('-')[2]))

            today = datetime.datetime(int(today.split('-')[0]),
                                      int(today.split('-')[1]),
                                      int(today.split('-')[2]))

            account = (today - start_day).days + 1


            if len(ltv_val_lst) > account:
                row_lst.append('-')
            else:
                row_lst = [_register_date.strftime('%Y-%m-%d'), new_user_num]
                row_lst.extend(ltv_val_lst)

        table_lst.append(row_lst)

    return table_lst


# 获取新用户日志
def _get_ltv_value(user_num, total_recharge_money):
    """
        获取ltv值
    """
    if user_num <= 0:
        return 0
    return round(float(total_recharge_money) / float(user_num), 4)
