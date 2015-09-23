# # -*- coding:utf-8 -*-
#
# from apps.utils import game_define
# from apps.game_manager.util import dat_log_util
#
#
#
#
#
# def get_table(start_data,end_data):
#
#     row_lst = []
#     new_log_lst = dat_log_util.read_file_with_filename("EVENT_ACTION_EQUIP_LEVEL_UP_MULTI",start_data,end_data)
#     new_log_lst1 = dat_log_util.read_file_with_filename("EVENT_ACTION_EQUIP_LEVEL_UP",start_data,end_data)
#     _lst = []
#     _lst.extend(new_log_lst)
#     _lst.extend(new_log_lst1)
#
#     for each_item in _lst:
#         log_time = each_item['log_time'].strftime("%Y-%m-%d %H:%M:%S")
#         uid = each_item['uid']
#         action_name = game_define.EVENT_LOG_ACTION_DICT[each_item['action']]
#         cost_gold = each_item['cost_gold']
#         cost_item_list = each_item['cost_item_list's][1]
#         row_list_append = [log_time,uid,action_name,cost_gold,cost_item_list]
#         row_lst.append(row_list_append)
#
#     return row_lst

from apps.utils.logs_out_in_path import OUT_PUT_PATH_LST
from apps.game_manager.util import dat_log_util
import pickle
import os
def get_table(search_start_date,server_id):

    """
        获取装备强化记录
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """
    new_log_lst = read_file_with_filename("EQUIPMENT_ST_RECORD",search_start_date,server_id)

    return new_log_lst

def read_file_with_filename(file_path,cur_date,server_id):
    data_lst=[]
    if int(server_id)==-1:
        return data_lst
    else:
		try:
			log_path = OUT_PUT_PATH_LST[int(server_id)]
		except:
			return data_lst

    if os.path.exists(log_path):
        file_path=log_path+"%s/tables/%s" %(cur_date,file_path)
        if not os.path.exists(file_path):
            return data_lst
        #print union_count_filepath
        if os.path.exists(file_path):
            f=open(file_path,'r')
            for i in pickle.load(f):
                data_lst.append(i)
	return data_lst




