# -*- coding:utf-8 -*-

"""
用户构成
开始时间	20101101	结束时间	20101103
游戏分区	所有	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道名称	所有	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

日期	活跃用户	用户流失	回流用户	注：回流用户统计方式需与cp商讨
2010/9/19	2970	20	20
2010/9/20	2971	30	30
总计	5941	50	50
PS：本表用户数均取角色数
"""


import datetime
from apps.game_manager.util import dat_log_util


def get_table(search_start_date, search_end_date, channel_id=-1, server_id=-1):
    new_log_lst = []
    if not search_start_date or not search_end_date:
        return new_log_lst
    now_date = datetime.date.today()
    if server_id != -1:
        if search_start_date < now_date:
            new_log_lst = dat_log_util.read_file_with_filename("USER_STRUCTURE", search_start_date, search_end_date, server_id, "tables")

    return new_log_lst

    # all_log_lst = daily_log_dat.get_new_log_lst(retained_day, search_end_date)
    #
    # if channel_id >= 0:
    #     all_log_lst = daily_log_dat.filter_logs(all_log_lst, function=lambda x: x['platform_id'] == channel_id)
    # if server_id >= 0:
    #     all_log_lst = daily_log_dat.filter_logs(all_log_lst, function=lambda x: x['server_id'] == server_id)

    #获取所有登录事件
    # all_login_lst = daily_log_dat.filter_logs(all_log_lst, action=game_define.EVENT_ACTION_ROLE_LOGIN)


    # 搜索日期到今天的所有日志
    # retained_day = search_start_date - datetime.timedelta(days=4)
    # all_login_lst = []
    # total_days = (search_end_date - retained_day).days+1
    # for i in xrange(total_days):
    #     search_date = retained_day + datetime.timedelta(days=i)
    #     date_str = "_"+search_date.strftime('%Y%m%d')
    #     login_lst = mysql_util.get_role_action_lst('EVENT_ACTION_ROLE_LOGIN'+str(date_str),search_date, search_date,channel_id, server_id,None, None)
    #     all_login_lst.extend(login_lst)
     # 获取日期数
    # search_days = (search_end_date - search_start_date).days
    #
    # table_result = []
    # for i in xrange(search_days+1):
    #     cur_date = search_start_date + datetime.timedelta(days=i)
    #     # 今日全部日志
    #     today_login_lst = daily_log_dat.get_new_log_lst_with_log(all_login_lst, cur_date, cur_date)
    #     # 获取登录日志列表
    #     today_login_uid_lst = daily_log_dat.get_set_with_key(today_login_lst, 'uid')
    #
    #     today_new_user_login_lst = daily_log_dat.filter_logs(today_login_lst, function=lambda log:log['install'] == cur_date)
    #     today_new_user_uid_num = daily_log_dat.get_set_num_with_key(today_new_user_login_lst, 'uid')
    #     # 登录用户数
    #     today_login_uid_num = len(today_login_uid_lst)
    #     # 活跃用户数
    #     today_active_uid_num = today_new_user_uid_num
    #
    #     # 流失用户（3天内没登录）
    #     today_lost_uid_num = len(daily_log_dat.get_lost_user_set(all_login_lst, cur_date))
    #     # 回流用户（3天内没登录 但今天登录）
    #     login_back_num = len(daily_log_dat.get_lost_back_user_set(all_login_lst, cur_date))
    #
    #     row = [cur_date.strftime("%m/%d/%Y"), today_login_uid_num, today_active_uid_num, today_lost_uid_num, login_back_num]
    #     table_result.append(row)

    # return table_result
