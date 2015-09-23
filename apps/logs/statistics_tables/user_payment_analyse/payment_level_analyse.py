# -*- coding:utf-8 -*-

"""
各等级充值情况 和 付费用户等级流失情况 这两个表相同

注册时间	开始时间	20100919	结束时间	20100920(修改为一个日期)
查询时间	查询	20100920
游戏分区	总区服/一区/二区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道名称	所有	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

"查询说明：
1.若输入注册时间，则查询表示查询注册玩家在查询时间段活跃用户的信息
2.若不输入注册时间，则查询表示查询在查询时间段的活跃用户信息"

停留人数=留存人数+流失人数
流失人数定义：到达该等级后截止至数据捞取当天，未登录天数大于等于3天的玩家
等级付费率=充值人数/到达人数
等级流失率=流失人数/到达人数

等级	停留人数	留存人数	流失人数	到达人数	充值金额	充值次数	充值人数	等级付费率	等级流失率
1
2
3
4
…
PS：本表人数均取角色数

"""

import datetime
from apps.logs import daily_log_dat
from apps.utils import game_define
from apps.game_manager.util import mysql_util
from apps.game_manager.util import dat_log_util


def get_table(search_start_date, search_end_date, register_start_date=None, register_end_date=None, channel_id=-1,
              server_id=-1):
    """
        获取各等级充值状况表格
    """
    # 获取搜索区间日志
    now_date = datetime.date.today()
    if search_end_date >= now_date:
        search_end_date = search_end_date-datetime.timedelta(days=1)
    total_recharge_log_lst = []
    total_days = (search_end_date - search_start_date).days + 1
    for i in xrange(total_days):
        search_date = search_start_date + datetime.timedelta(days=i)
        date_str = "_" + search_date.strftime('%Y%m%d')
        recharge_log_lst = mysql_util.get_role_action_lst('EVENT_ACTION_RECHARGE_PLAYER' + str(date_str), search_date,
                                                          search_date, channel_id, server_id, register_start_date,
                                                          register_end_date)
        total_recharge_log_lst.extend(recharge_log_lst)

    channel_server_str = ""
    if channel_id >= 0:
        channel_server_str += "platform_id = " + str(channel_id) + " and "
    if server_id >= 0:
        channel_server_str += " server_id = " + str(server_id) + " and "
    if register_start_date:
        channel_server_str += "  '%s' <= install and " % register_start_date
    if register_end_date:
        channel_server_str += " install  <= '%s'  " % register_end_date

    # if channel_server_str:
    #     sql = "SELECT * FROM user_detail WHERE %s " % channel_server_str
    # else:
    #     sql = "SELECT * FROM user_detail"
    # print sql
    # result = mysql_util.query(sql)
    # if channel_server_str:
    old_log_dict = dat_log_util.read_file_dict_with_filename("USER_DETAIL", search_end_date, server_id, 'tables')
    if register_start_date and register_end_date:
        new_log_dict = dict()
        for uid, detail in old_log_dict.items():
            if register_start_date <= detail['install'] <= register_end_date:
                new_log_dict[uid] = detail
    else:
        new_log_dict = old_log_dict

    user_num_dict = dict()
    lost_user_num_dict = dict()
    arrive_user_num = dict()
    for dat in new_log_dict.values():
        cur_lv = dat['level']
        user_num_dict[cur_lv] = user_num_dict.get(cur_lv, 0) + 1
        if dat['last_play_time'].date() < (search_end_date - datetime.timedelta(days=3)):
            lost_user_num_dict[cur_lv] = lost_user_num_dict.get(cur_lv, 0) + 1

    for _table_lv in xrange(1, 121):
        arrive_num = sum([user_num_dict.get(lv, 0) for lv in xrange(_table_lv, 121)])
        arrive_user_num[_table_lv] = arrive_num

    # 获取所有等级停留人数
    table_row_lst = []
    for _table_lv in xrange(1, 121):
        level_recharge_lst = daily_log_dat.get_recharge_lst_with_user_level(total_recharge_log_lst, _table_lv)
        recharge_uid_lst = daily_log_dat.get_user_uid_lst(level_recharge_lst)
        # 停留人数
        user_num = user_num_dict.get(_table_lv, 0)
        # 流失人数
        lost_num = lost_user_num_dict.get(_table_lv, 0)
        # 留存人数
        stand_num = user_num - lost_num
        # 到达等级人数
        arrive_num = arrive_user_num[_table_lv]
        # 充值金额
        recharge_money = daily_log_dat.get_recharge_total_money(level_recharge_lst)
        # 充值次数
        recharge_num = len(level_recharge_lst)
        # 充值人数
        recharge_user_num = len(recharge_uid_lst)
        # 等级付费率
        level_pay_rate = _get_level_pay_rate(recharge_user_num, arrive_num)
        # 等级流失率 流失人数/到达人数
        level_lost_rate = _get_level_lost_rate(lost_num, arrive_num)

        content = [_table_lv, user_num, stand_num, lost_num, arrive_num, recharge_money, recharge_num,
                   recharge_user_num, str(level_pay_rate * 100) + "%", str(level_lost_rate * 100) + "%"]
        table_row_lst.append(content)

    return table_row_lst


def _get_level_pay_rate(recharge_user_num, arrive_num):
    if arrive_num <= 0:
        return 0
    return round(float(recharge_user_num) / float(arrive_num), 4)


def _get_level_lost_rate(lost_num, arrive_num):
    if arrive_num <= 0:
        return 0
    return round(float(lost_num) / float(arrive_num), 4)


def _get_level_uid_lst(level, uid_level_dict):
    """
        获取指定等级玩家UID 列表
    """
    return [_uid for _uid, _lv in uid_level_dict.items() if _lv == level]


def _get_arrive_level_uid_lst(level, uid_level_dict):
    """
        获取到达等级的玩家
    """
    return [_uid for _uid, _lv in uid_level_dict.items() if _lv >= level]
