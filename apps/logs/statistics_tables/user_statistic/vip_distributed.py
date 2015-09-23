# -*- coding:utf-8 -*-


"""
vip分布（具体情况根据游戏而定）
注册时间	开始时间	20100919	结束时间	20100920
查询时间	开始时间	20100920	结束时间	20100923

"查询说明：
1.若输入注册时间，则查询表示查询注册玩家在查询时间段活跃用户的信息
2.若不输入注册时间，则查询表示查询在查询时间段的活跃用户信息"
查询时间	开始时间	20100920	结束时间	20100923
游戏分区	总区服/一区/二区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道名称	所有	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

注：以下情况会根据游戏具体情况进行修订
条件	首冲	月卡 vip0	vip1	vip2	vip3	vip4	vip5	vip6	vip7	vip8	vip9	vip10	。。。
总体	124	124	125	124	125	126	127	128	129	130	131	132	133	134
新增	124	124	125	124	125	126	127	128	129	130	131	132	133	134
比率
比率=新增vip数/新增用户数
PS：本表用户均取角色数
"""
import datetime
from apps.game_manager.util import mysql_util


def get_table(search_start_date=None, search_end_date=None, server_id=-1, register_start_date=None, register_end_date=None):
    table_result = []
    total_days = (search_end_date-search_start_date).days+1
    for _day in xrange(total_days):
        # -------------总体-----------------
        total_line = []
        new_user_line = []
        add_line = []
        rate_line = []
        # 每行的日期
        row_date = search_start_date + datetime.timedelta(days=_day)
        date_str = '_'+row_date.strftime('%Y%m%d')
        # 插入数据
        total_line.append(row_date.strftime('%Y-%m-%d'))
        new_user_line.append(row_date.strftime('%Y-%m-%d'))
        add_line.append(row_date.strftime('%Y-%m-%d'))
        rate_line.append(row_date.strftime('%Y-%m-%d'))
        # 首冲
        first_recharge = mysql_util.get_first_recharge_shop_index_uid_num('uid', 'EVENT_ACTION_RECHARGE_PLAYER'+str(date_str), row_date, 'shop_index', -1, -1, server_id, register_start_date, register_end_date)
        # 月卡
        month_card_recharge = mysql_util.get_recharge_shop_index_uid_num('uid', 'EVENT_ACTION_RECHARGE_PLAYER'+str(date_str), row_date, 'shop_index', 1, -1, server_id, register_start_date, register_end_date)
        # vip总体登录
        total_line.extend(['总体', first_recharge, month_card_recharge])
        vip_level_lst = [0]*13

        uid_level_lst = mysql_util.get_vip_distributed_uid('EVENT_ACTION_ROLE_LOGIN'+str(date_str), -1, server_id, register_start_date, register_end_date)
        for _uid_level in uid_level_lst:
            _vip_level = int(_uid_level['vip_level'])
            vip_level_lst[_vip_level] = int(_uid_level['count(uid)'])
        total_line.extend(vip_level_lst)

        # -------------新增-----------------
        new_install_num = mysql_util.get_today_new_num('uid', 'EVENT_ACTION_ROLE_LOGIN'+str(date_str), row_date, -1, server_id)
        add_line.extend(['今日新增用户'])
        add_line.extend([new_install_num] * 15)
        # 首冲
        first_recharge = mysql_util.get_first_recharge_shop_index_uid_num('uid', 'EVENT_ACTION_RECHARGE_PLAYER'+str(date_str), row_date, 'shop_index', -1, -1, server_id, row_date, row_date)
        # 月卡
        month_card_recharge = mysql_util.get_recharge_shop_index_uid_num('uid', 'EVENT_ACTION_RECHARGE_PLAYER'+str(date_str), row_date, 'shop_index', 1, -1, server_id, row_date, row_date)
        # vip 新增充值
        new_user_line.extend(['新增', first_recharge, month_card_recharge])
        new_vip_level_lst = [0]*13
        new_uid_level_lst = mysql_util.get_vip_distributed_uid('EVENT_ACTION_ROLE_LOGIN'+str(date_str), -1, server_id, row_date, row_date)
        for _uid_level in new_uid_level_lst:
            _vip_level = int(_uid_level['vip_level'])
            new_vip_level_lst[_vip_level] = int(_uid_level['count(uid)'])
        new_user_line.extend(new_vip_level_lst)

        # -------------比率-----------------
        rate_line.extend(['比率'])
        for _index in xrange(2, 17):
            rate = division(new_user_line[_index], add_line[_index])
            rate_line.append(str(rate*100)+'%')

        table_result.extend([total_line, new_user_line, add_line, rate_line])
    return table_result


def division(num_1, num2):
    if not num2:
        return 0
    return round(float(num_1)/float(num2), 4)
# def get_table(register_start_date=None, register_end_date=None, search_start_date=None, search_end_date=None, server_id=-1):
#     """
#         获取展示表格
#         register_start_date 注册开始时间
#         register_end_date 注册结束时间
#         search_start_date 查询开始时间
#         search_end_date 查询结束时间
#     """
#     if register_start_date and register_end_date:
#         table_lst = get_create_table_with_register(search_start_date, search_end_date, register_start_date, register_end_date, server_id)
#     else:
#         table_lst = get_create_table(search_start_date, search_end_date, server_id)
#     return table_lst
#
#
# def get_create_table(search_start_date, search_end_date, server_id):
#     new_log_lst = dat_log_util.read_file_with_filename("VIP_DISTRIBUTED", search_start_date, search_end_date, server_id)
#     # new_log_lst = read_file_with_filename("VIP_DISTRIBUTED4", search_start_date, search_end_date)
#     # print new_log_lst
#     table_lst = []
#     # print(new_log_lst)
#     for index, new_log in enumerate(new_log_lst):
#         cur_date = search_start_date + datetime.timedelta(days=index/5)
#         if type(new_log) != dict:
#             new_log.insert(0, cur_date.strftime('%m/%d/%Y'))
#             if index % 5 == 0:
#                 new_log.extend(new_log_lst[index+4]['Total'])
#             table_lst.append(new_log)
#     # print table_lst
#     return table_lst
#
#
# def get_create_table_with_register(search_start_date, search_end_date, register_start_date, register_end_date, server_id):
#     new_log_lst = dat_log_util.read_file_with_filename("VIP_DISTRIBUTED", search_start_date, search_end_date, server_id)
#     # new_log_lst = read_file_with_filename("VIP_DISTRIBUTED4", search_start_date, search_end_date)
#     table_lst = []
#     for index, new_log in enumerate(new_log_lst):
#         cur_date = search_start_date + datetime.timedelta(days=index/5)
#         if type(new_log) != dict:
#             new_log.insert(0, cur_date.strftime('%m/%d/%Y'))
#             if index % 5 == 0:
#                 table_line_extend = _sum_total_line(new_log_lst[index+4], register_start_date, register_end_date)
#                 new_log.extend(table_line_extend)
#             table_lst.append(new_log)
#     # print table_lst
#     return table_lst
#
#
# def _sum_total_line(table_line_dict, register_start_date, register_end_date):
#     table_line_extend = [0] * 13
#     for date_str in table_line_dict.keys():
#         if date_str != 'Total' and date_str != 'cur_date':
#             date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
#             if register_start_date <= date <= register_end_date:
#                 for i in xrange(13):
#                     table_line_extend[i] += table_line_dict[date_str][i]
#     return table_line_extend
# import os
# import pickle
# CATCH_LOGS_DAT = 'D:'
# def read_file_with_filename(file_name, from_date,to_date):
#     dat_lst = []
#     if os.path.exists(CATCH_LOGS_DAT):
#         total_days = (to_date - from_date).days + 1
#         for i in xrange(total_days):
#             dat_dict = dict()
#             # 每行的日期
#             cur_date = from_date + datetime.timedelta(days=i)
#             print CATCH_LOGS_DAT+"\%s" % (file_name)
#             if os.path.exists(CATCH_LOGS_DAT+"\%s" % (file_name)):
#                 out_put_file = open(CATCH_LOGS_DAT+"\%s" % (file_name), 'r')
#                 dat_dict = pickle.load(out_put_file)
#                 dat_lst.extend(dat_dict)
#                 out_put_file.close()
#
#     return dat_lst

# def _output_VIP_DISTRIBUTED():
#     out_put_file_path = "D:"
#     out_put_file = open(out_put_file_path + '\VIP_DISTRIBUTED1', 'w')
#     result = [['\xe6\x80\xbb\xe4\xbd\x93\xe7\x99\xbb\xe5\xbd\x95', 17, 6, 1912, 204, 101, 23, 64, 32, 18, 5, 3, 1, 0, 0, 0], ['\xe6\x96\xb0\xe5\xa2\x9e\xe5\x85\x85\xe5\x80\xbc', 7, 1, 414, 5, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], ['\xe6\x96\xb0\xe5\xa2\x9e\xe8\xa7\x92\xe8\x89\xb2\xe6\x95\xb0', 421, 421, 421, 421, 421, 421, 421, 421, 421, 421, 421, 421, 421, 421, 421], ['\xe6\xaf\x94\xe7\x8e\x87', 0.02, 0.0, 0.98, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
#     pickle.dump(result, out_put_file)
#     out_put_file.close()
# _output_VIP_DISTRIBUTED()
# print "get table:"
# get_table(datetime.date(2015,5,30),datetime.date(2015,5,31),-1)
# get_table(datetime.date(2015,5,30),datetime.date(2015,5,31),-1,datetime.date(2015,5,30),datetime.date(2015,5,31))
