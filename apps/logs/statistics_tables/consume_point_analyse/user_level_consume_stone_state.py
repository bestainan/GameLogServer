# -*- coding:utf-8 -*-

"""
等级消耗情况
注册时间	开始时间	20100919	结束时间	20100920
查询时间	开始时间	20100920	结束时间	20100923

游戏分区	总区服/一区/二区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道名称	所有	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

钻石等级消耗


等级	消耗人数	消耗数量	到达人数	等级消耗ARPPU	等级消耗率
1	7	6670	446	952.86 	1.57%
2	20	24110	368	1205.50 	5.43%
3	35	57110	340	1631.71 	10.29%
4	59	32642	313	553.25 	18.85%
5	62	86414	292	1393.77 	21.23%
…
PS：本表人数均取角色数

等级消耗ARPPU: 消耗数量/消耗人数
等级消耗率: 消耗人数/达到人数
"""

import datetime
from apps.logs import daily_log_dat
from apps.game_manager.util import dat_log_util
def get_table(search_start_date, server_id):
    """
        获取展示表格
        register_start_date 注册开始时间
        register_end_date 注册结束时间
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """
    # 获取搜索区间日志
    new_log_dict = dat_log_util.read_file_dict_with_filename("USER_STONE_CONSUME",search_start_date, server_id)
    # print(new_log_dict)
    # if channel_id >= 0:
    #     new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['platform_id'] == channel_id)
    # if server_id >= 0:
    #     new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['server_id'] == server_id)
    # #获取符合条件的日志
    # if register_start_date and register_end_date:
    #     new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda log: register_start_date <= log['install'] <= register_end_date)

    # 获取所有钻石消耗的日志
    # cost_stone_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda log: 'cost_stone' in log)
    # level_log_dict = get_user_level_dict(cost_stone_log_lst)
    table_result = []
    for _lv in xrange(1, 121):
        # print("--------------------"+str(_lv) + "--------------------")
        row = []
        # print(""+str(new_log_dict.get('level_total_cost_%s' % _lv,0)))
        sum_cost_stone= new_log_dict.get('level_total_cost_%s' % _lv,0)
        cur_lv_num= new_log_dict.get('level_user_cost_num_%s' % _lv,0)
        #到达人数
        arrive_user_num =  new_log_dict.get('level_user_arrive_%s' % _lv,0)
        level_arppu = new_log_dict.get('level_arppu_%s' % _lv,0)
        # 等级
        row.append(str(_lv))
        # 消耗人数
        row.append(str(cur_lv_num))
        # 消耗数量
        row.append(str(sum_cost_stone))
        # 到达人数
        row.append(arrive_user_num)
        # 等级消耗ARPPU
        row.append(str(level_arppu))
        # 等级消耗率
        if arrive_user_num == 0:
            row.append(str(0) + "%")
        else:
            row.append(str(round(float(cur_lv_num) / float(arrive_user_num), 2) * 100) + "%")
        # row = [_lv, action_total_cost_stone, user_num, action_cost_num, take_part_rate, first_cost_stone_rate, cur_user_num_rate]
        # print("row: "+str(row))
        table_result.append(row)

    return table_result

def get_user_level_dict(cost_stone_log_lst):
    """
        获取等级 字典
    """
    level_log_dict = dict()

    for _lv in xrange(1, 121):
        _log_lst = daily_log_dat.get_log_lst_with_level(cost_stone_log_lst, _lv)
        level_log_dict[_lv] = _log_lst
    return level_log_dict

