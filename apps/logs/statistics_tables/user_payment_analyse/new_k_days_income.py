# -*- coding:utf-8 -*-

"""
新增K日收益统计
注册时间	2010.9.19	结束时间	2010.9.26
游戏分区	所有	（可以查单区，默认所有区）
渠道名称	所有	（可以查单独的渠道，默认所有渠道）

日期	新增设备	第1天	第2天	第3天	第4天	第5天	第6天	第7天	第15日	第30日	30日以上
2010/9/19	124	3000	3000	3000	3000	3000	3000	3000
2010/9/20	125	3000	3000	3000	3000	3000	3000	3000
2010/9/21	126	3000	3000	3000	3000	3000	3000
2010/9/22	127	3000	3000	3000	3000	3000
2010/9/23	128	3000	3000	3000	3000
2010/9/24	129	3000	3000	3000
2010/9/25	130	3000	3000
2010/9/26	131	3000
*指定日期内的注册用户，在注册以后的K日内收益的累计值
*第1天为注册当天、之后天数自然延展
PS：本表人数均取角色数
"""
"""注：锁定当天安装客户端的且充值的用户（即当天安装且充值），在查看它们以后多天的充值情况"""

import datetime
from apps.logs import daily_log_dat
from apps.game_manager.util import mysql_util

ALL_RECHARGE_LOG_LST = []
ROW_NEW_USER_UID_LST = []


def get_table(register_star_date, register_end_date, channel_id=-1, server_id=-1):
    """
        新增K日收益统计
    """
    now_date = datetime.date.today()
    total_days = (now_date-register_star_date).days+1
    all_login_log_lst = []
    global ALL_RECHARGE_LOG_LST
    ALL_RECHARGE_LOG_LST = []
    for i in xrange(total_days):
        search_date = register_star_date+datetime.timedelta(days=i)
        date_str = "_"+search_date.strftime('%Y%m%d')
        # 获得查询日期到今天的所有登陆 和 充值数据
        login_log_lst = mysql_util.get_role_action_lst('EVENT_ACTION_ROLE_LOGIN'+str(date_str),search_date,search_date, channel_id, server_id,None, None)
        recharge_log_lst = mysql_util.get_role_action_lst('EVENT_ACTION_RECHARGE_PLAYER'+str(date_str),search_date,search_date, channel_id, server_id,None, None)
        all_login_log_lst.extend(login_log_lst)
        ALL_RECHARGE_LOG_LST.extend(recharge_log_lst)

    # 计算数据
    row_days = (register_end_date - register_star_date).days+1
    table_lst = []
    for _day in xrange(row_days):
        global ROW_NEW_USER_UID_LST
        ROW_NEW_USER_UID_LST = []
        row_date = register_star_date + datetime.timedelta(days=_day)
        # 获取新用户
        ROW_NEW_USER_UID_LST = daily_log_dat.get_set_with_key(all_login_log_lst, 'uid', function=lambda log: log['install'] == row_date)
        # 获取新增设备
        new_device_num = daily_log_dat.get_set_num_with_key(all_login_log_lst, 'dev_id', function=lambda log: log['install'] == row_date)
        # 日期
        recharge_date_1 = row_date + datetime.timedelta(days=0)
        recharge_date_2 = row_date + datetime.timedelta(days=1)
        recharge_date_3 = row_date + datetime.timedelta(days=2)
        recharge_date_4 = row_date + datetime.timedelta(days=3)
        recharge_date_5 = row_date + datetime.timedelta(days=4)
        recharge_date_6 = row_date + datetime.timedelta(days=5)
        recharge_date_7 = row_date + datetime.timedelta(days=6)
        recharge_date_15 = row_date + datetime.timedelta(days=14)
        recharge_date_30 = row_date + datetime.timedelta(days=29)
        recharge_date_up = row_date + datetime.timedelta(days=29)

        # 获取充值总额
        row = []
        row.append(row_date.strftime('%Y-%m-%d'))
        row.append(new_device_num)
        row.append(compute_k_days(recharge_date_1))                                # 第1日
        row.append(compute_k_days(recharge_date_2))                                # 第2日
        row.append(compute_k_days(recharge_date_3))                                # 第3日
        row.append(compute_k_days(recharge_date_4))                                # 第4日
        row.append(compute_k_days(recharge_date_5))                                # 第5日
        row.append(compute_k_days(recharge_date_6))                                # 第6日
        row.append(compute_k_days(recharge_date_7))                                # 第7日
        row.append(compute_k_days(recharge_date_7, _to_days=recharge_date_15))     # 第7~30日
        row.append(compute_k_days(recharge_date_15, _to_days=recharge_date_30))    # 第15~30日
        row.append(compute_k_days(recharge_date_up, compute='greater'))            # 第30日以后

        table_lst.append(row)
    return table_lst


def compute_k_days(_k_days, _to_days=None, compute=None):
    global ALL_RECHARGE_LOG_LST, ROW_NEW_USER_UID_LST
    _k_days_total_rmb = []
    if "greater" == compute and _k_days:
        _k_days_total_rmb = daily_log_dat.get_sum_int_with_key(ALL_RECHARGE_LOG_LST, 'add_rmb', function=lambda log: _k_days < log['log_time'].date() and log['uid'] in ROW_NEW_USER_UID_LST)
    elif _to_days and _k_days and _k_days < _to_days:
        _k_days_total_rmb = daily_log_dat.get_sum_int_with_key(ALL_RECHARGE_LOG_LST, 'add_rmb', function=lambda log: _k_days < log['log_time'].date() <= _to_days and log['uid'] in ROW_NEW_USER_UID_LST)
    elif _k_days:
        _k_days_total_rmb = daily_log_dat.get_sum_int_with_key(ALL_RECHARGE_LOG_LST, 'add_rmb', function=lambda log: log['log_time'].date() == _k_days and log['uid'] in ROW_NEW_USER_UID_LST)

    return _k_days_total_rmb