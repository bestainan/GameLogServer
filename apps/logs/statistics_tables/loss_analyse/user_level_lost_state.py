# -*- coding:utf-8 -*-


"""
整体用户等级流失情况
注册时间	开始时间	20100919	结束时间	20100920
查询时间	开始时间	20100920	结束时间	20100923

"查询说明：
1.若输入注册时间，则查询表示查询注册玩家在查询时间段活跃用户的信息
2.若不输入注册时间，则查询表示查询在查询时间段的活跃用户信息"

游戏分区	总区服/一区/二区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道名称	所有	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

整体用户等级流失情况

等级	停留人数	留存人数	流失人数	到达人数	等级流失率
1	65	9	56	370	15.14%
2	21	3	18	305	5.90%
3	32	10	22	284	7.75%
4	22	11	11	252	4.37%
…
PS：本表人数均取角色数

"""
import time
import datetime
from apps.utils import game_define
from apps.logs import daily_log_dat
from apps.game_manager.util import dat_log_util
from apps.game_manager.util import mysql_util


def get_table(search_end_date, register_start_date=None, register_end_date=None, server_id=-1):
    """
        获取展示表格
        register_start_date 注册开始时间
        register_end_date 注册结束时间
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """
    # new_log_lst = {}
    new_log_lst = dat_log_util.read_file_dict_with_filename("USER_DETAIL",search_end_date,server_id, 'tables')

    # sql = "SELECT * FROM USER_LEVEL_LOST_STATE"
    # result = mysql_util.query(sql)
    user_num_dict = dict()
    lost_user_num_dict = dict()
    arrive_user_num = dict()
    for dat in new_log_lst.values():
        cur_lv = dat['level']
        if register_start_date and register_end_date:
            if dat['last_play_time'].date() < (search_end_date - datetime.timedelta(days=3)) and register_start_date <= dat['install'] <= register_end_date:
                lost_user_num_dict[cur_lv] = lost_user_num_dict.get(cur_lv, 0) + 1
            if register_start_date <= dat['install'] <= register_end_date:
                user_num_dict[cur_lv] = user_num_dict.get(cur_lv, 0) + 1
        else:
            if dat['last_play_time'].date() < (search_end_date - datetime.timedelta(days=3)):
                lost_user_num_dict[cur_lv] = lost_user_num_dict.get(cur_lv, 0) + 1
            user_num_dict[cur_lv] = user_num_dict.get(cur_lv, 0) + 1

    for _table_lv in xrange(1, 121):
        if register_start_date and register_end_date:
            arrive_num = sum([user_num_dict.get(lv, 0) for lv in xrange(_table_lv, 121)])
            arrive_user_num[_table_lv] = arrive_num
        else:
            arrive_num = sum([user_num_dict.get(lv, 0) for lv in xrange(_table_lv, 121)])
            arrive_user_num[_table_lv] = arrive_num

    # 遍历全部等级
    table_row_lst = []
    for _table_lv in xrange(1, 121):
        # 停留人数
        user_num = user_num_dict.get(_table_lv, 0)
        # 流失人数
        lost_num = lost_user_num_dict.get(_table_lv, 0)
        # 留存人数
        stand_num = user_num - lost_num
        # 到达等级人数
        arrive_num = arrive_user_num[_table_lv]
        # 等级流失率
        level_lost_rate = str(_get_level_lost_rate(lost_num, arrive_num) * 100) + "%"
        # 等级	停留人数	留存人数	流失人数	到达人数	等级流失率
        content = [_table_lv, user_num, stand_num, lost_num, arrive_num, level_lost_rate]
        table_row_lst.append(content)
    return table_row_lst


def _get_level_lost_rate(lost_num, arrive_num):
    if arrive_num <= 0:
        return 0
    return round(float(lost_num) / float(arrive_num), 2)


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

