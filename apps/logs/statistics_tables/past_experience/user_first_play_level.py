# -*- coding:utf-8 -*-

"""
    用户首日等级留存
查询日期	20101101
分区查询	总/1区/2区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道标示	UC/91	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

用户首日等级留存	"1.选取当天新登录的用户的最大等级统计，并计算这批用户的次日留存率
2.有效用户按登录用户计算"

等级 人数	占比 次日留存率
1	100	5.00%	31%
2	100	5.00%	32%
3	100	5.00%	33%
4	100	5.00%	34%
5	100	5.00%	35%
6	100	5.00%	36%
7	100	5.00%	37%
13	100	5.00%	43%
14	100	5.00%	44%
15	100	5.00%	45%
16	100	5.00%	46%
17	100	5.00%	47%
18	100	5.00%	48%
19	100	5.00%	49%
20	100	5.00%	50%
总计	2000	5.00%	45%
PS：本表用户数均取角色数
"""


import datetime
from apps.utils import game_define
from apps.logs import daily_log_dat
from apps.game_manager.util import mysql_util
from apps.game_manager.util import dat_log_util


# 获取比率
def _get_level_user_num_rate(level_user_num, total_user):
    """

    """
    if total_user <= 0:
        return 0
    return round(float(level_user_num) / float(total_user), 2) * 100


 # 获取比率
def _get_retained_1_login_rate(level_user_num, retained_1_login_uid_set):
    if retained_1_login_uid_set <= 0:
        return 0
    return  round(float(level_user_num) / float(retained_1_login_uid_set), 2) * 100



def get_table(search_start_date, server_id=-1):
    """
        获取展示表格
        register_start_date 注册开始时间
        register_end_date 注册结束时间
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """
    new_log_lst = dat_log_util.read_file_dict_with_filename("USER_DETAIL",search_start_date,server_id,'tables')
    user_num_dict = dict()
    lost_user_num_dict = dict()
    for dat in new_log_lst.values():
        cur_lv = dat['level']
        if search_start_date == dat['install']:
            user_num_dict[cur_lv] = user_num_dict.get(cur_lv, 0) + 1
        #这里再查第二天的new_log_lst
        if search_start_date == dat['install'] and dat['last_play_time'].date() == dat['install']:
            lost_user_num_dict[cur_lv] = lost_user_num_dict.get(cur_lv, 0) + 1

    num_total = 0
    for _table_lv in xrange(1, 121):
        num_total += user_num_dict.get(_table_lv, 0)

    # 遍历全部等级
    table_row_lst = []
    for _table_lv in xrange(1, 121):
        # 停留人数
        user_num = user_num_dict.get(_table_lv, 0)
        # 流失人数
        lost_num = lost_user_num_dict.get(int(_table_lv), 0)

        # 留存人数
        stand_num = user_num - lost_num

        # 等级比率
        level_rate = str(_get_rate(user_num, num_total)* 100) + "%"
        # 留存人数比率
        level_lost_rate = str(_get_rate(stand_num , num_total) * 100) + "%"
        #todo:
        # if _t
        # 等级	停留人数	留存人数比率	等级流存率
        content = [_table_lv, user_num, level_rate, level_lost_rate]
        table_row_lst.append(content)

    return table_row_lst

def _get_rate(lost_num, arrive_num):
    if arrive_num <= 0:
        return 0

    return round(float(lost_num)/float(arrive_num), 2)


# print get_table(datetime.date(2015,5,21),datetime.date(2015,5,21))