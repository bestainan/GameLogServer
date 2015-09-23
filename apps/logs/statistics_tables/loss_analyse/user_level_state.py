# -*- coding:utf-8 -*-


"""
    每日玩家等级表现
注册时间	开始时间	20100919	结束时间	20100920
查询时间	开始时间	20100920	结束时间	20100923

"查询说明：
1.若输入注册时间，则查询表示查询注册玩家在查询时间段活跃用户的信息
2.若不输入注册时间，则查询表示查询在查询时间段的活跃用户信息"


游戏分区	总区服/一区/二区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道名称	所有	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

每日玩家等级表现

时间	登陆用户数	新增用户数	1	2	3	4	5	6	7	8	9	10	11	…
20101103	1419 		124	125	126	127	128	129	130	131	132	133	134
20101104	1419 		124	125	126	127	128	129	130	131	132	133	134
20101105	1419 		124	125	126	127	128	129	130	131	132	133	134
20101106	1419 		124	125	126	127	128	129	130	131	132	133	134
20101107	1419 		124	125	126	127	128	129	130	131	132	133	134
20101108	1419 		124	125	126	127	128	129	130	131	132	133	134
20101109	1419 		124	125	126	127	128	129	130	131	132	133	134
注：1.以上条件代表，2010年09月19日-2010年09月20日产生的角色，在2010年11月3日-2010年11月09日之间每天的登陆用户（去重）等级分布情况
        2.若不输入注册时间，则以上条件代表，在2010年11月3日-2010年11月09日之间每天的所选区服内登陆用户（去重）等级分布情况
PS：本表用户数均取角色数

"""
import time
import datetime
from apps.game_manager.util import dat_log_util



def get_table(search_start_date, search_end_date, player_min_lv, player_max_lv, register_start_date=None, register_end_date=None, cur_server=-1):
    """
        获取展示表格
        register_start_date 注册开始时间
        register_end_date 注册结束时间
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """
    search_days = (search_end_date - search_start_date).days + 1

    table_result = []
    for i in xrange(search_days):
        cur_date = search_start_date + datetime.timedelta(days=i)

        new_log_lst = dat_log_util.read_file_with_single_day("USER_DETAIL", cur_date, cur_server)
        user_level_state = dat_log_util.read_file_with_single_day("USER_LEVEL_STATE", cur_date, cur_server)

        if new_log_lst and user_level_state:
            # 到此时的总用户数
            by_this_time_uid_num = len(new_log_lst)
            # 登录用户数
            today_login_uid_num = user_level_state[0]
            # 新增用户数
            today_new_uid_num = user_level_state[1]
            # 等级用户数
            level_user_num_lst = []
            for _lv in xrange(player_min_lv, player_max_lv + 1):
                # 计算等级用户数
                _user_detail_dict = new_log_lst
                if register_start_date and register_end_date:
                    user_num = len([_dat['uid'] for _dat in _user_detail_dict.values() if _dat['level'] == _lv and _dat['server_id'] > 0 and _dat['platform_id'] > 0 and register_start_date <= _dat['install'] <= register_end_date])
                else:
                    user_num = len([_dat['uid'] for _dat in _user_detail_dict.values() if _dat['level'] == _lv])
                # 插入数据
                level_user_num_lst.append(user_num)
            row = [cur_date.strftime('%Y-%m-%d'), by_this_time_uid_num, today_login_uid_num, today_new_uid_num]
            row.extend(level_user_num_lst)
            table_result.append(row)
    return table_result



def get_level_user_num(uid_level_dict, level):
    """
        获取等级玩家数量
    """
    num = 0
    for _level in uid_level_dict.values():
        if _level == level:
            num += 1
    return num









#
# # -*- coding:utf-8 -*-
#
#
# """
#     每日玩家等级表现
# 注册时间	开始时间	20100919	结束时间	20100920
# 查询时间	开始时间	20100920	结束时间	20100923
#
# "查询说明：
# 1.若输入注册时间，则查询表示查询注册玩家在查询时间段活跃用户的信息
# 2.若不输入注册时间，则查询表示查询在查询时间段的活跃用户信息"
#
#
# 游戏分区	总区服/一区/二区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
# 渠道名称	所有	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）
#
# 每日玩家等级表现
#
# 时间	登陆用户数	新增用户数	1	2	3	4	5	6	7	8	9	10	11	…
# 20101103	1419 		124	125	126	127	128	129	130	131	132	133	134
# 20101104	1419 		124	125	126	127	128	129	130	131	132	133	134
# 20101105	1419 		124	125	126	127	128	129	130	131	132	133	134
# 20101106	1419 		124	125	126	127	128	129	130	131	132	133	134
# 20101107	1419 		124	125	126	127	128	129	130	131	132	133	134
# 20101108	1419 		124	125	126	127	128	129	130	131	132	133	134
# 20101109	1419 		124	125	126	127	128	129	130	131	132	133	134
# 注：1.以上条件代表，2010年09月19日-2010年09月20日产生的角色，在2010年11月3日-2010年11月09日之间每天的登陆用户（去重）等级分布情况
#         2.若不输入注册时间，则以上条件代表，在2010年11月3日-2010年11月09日之间每天的所选区服内登陆用户（去重）等级分布情况
# PS：本表用户数均取角色数
#
# """
# import time
# import datetime
# from apps.game_manager.util import dat_log_util
#
#
#
# def get_table(search_start_date, search_end_date, player_min_lv, player_max_lv, register_start_date=None, register_end_date=None):
#     """
#         获取展示表格
#         register_start_date 注册开始时间
#         register_end_date 注册结束时间
#         search_start_date 查询开始时间
#         search_end_date 查询结束时间
#     """
#
#     new_log_lst = dat_log_util.read_file_with_user_level_state("USER_DETAIL", search_start_date, search_end_date)
#     user_level_state = dat_log_util.read_file_with_user_level_state("USER_LEVEL_STATE", search_start_date,
#                                                                     search_end_date)
#
#     # search_dat = []
#     # if register_start_date and register_end_date:
#     #     for _user_detail in new_log_lst:
#     #         register_user_detail = dict()
#     #         for _uid, _dat in _user_detail.items():
#     #             install_date = _dat['install']
#     #             if register_start_date <= install_date <= register_end_date:
#     #                 register_user_detail[_uid] = _dat
#     #                 # print (str(register_user_detail[_uid]) + '\n')
#     #                 search_dat.append(register_user_detail[_uid])
#     # print (str((search_dat)) + '\n')
#
#     # else:
#     search_dat = new_log_lst
#
#     # 获取日期数
#     search_days = (search_end_date - search_start_date).days
#
#     table_result = []
#     for i in xrange(search_days+1):
#         cur_date = search_start_date + datetime.timedelta(days=i)
#         # 到此时的总用户数
#         by_this_time_uid_num = len(search_dat[i])
#         # 登录用户数
#         today_login_uid_num = user_level_state[i][0]
#         # 新增用户数
#         today_new_uid_num = user_level_state[i][1]
#         # 等级用户数
#         level_user_num_lst = []
#         for _lv in xrange(player_min_lv, player_max_lv + 1):
#             # 计算等级用户数
#             _user_detail_dict = search_dat[i]
#             if register_start_date and register_end_date:
#                 user_num = len([_dat['uid'] for _dat in _user_detail_dict.values() if _dat['level'] == _lv and _dat['server_id'] >0 and _dat['platform_id'] > 0 and register_start_date <= _dat['install'] <= register_end_date])
#             else:
#                 user_num = len([_dat['uid'] for _dat in _user_detail_dict.values() if _dat['level'] == _lv])
#             # 插入数据
#             level_user_num_lst.append(user_num)
#         row = [cur_date.strftime('%Y-%m-%d'), by_this_time_uid_num, today_login_uid_num, today_new_uid_num]
#         row.extend(level_user_num_lst)
#         table_result.append(row)
#     return table_result
#
#
#
# def get_level_user_num(uid_level_dict, level):
#     """
#         获取等级玩家数量
#     """
#     num = 0
#     for _level in uid_level_dict.values():
#         if _level == level:
#             num += 1
#     return num
#
#
