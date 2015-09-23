# -*- coding:utf-8 -*-


import pickle
import os

from apps.utils.logs_out_path_of_server import get_server_path

# 联盟商店信息统计
def get_table(search_start_date,server_id):
	result = read_file_with_user_get(search_start_date,server_id)
	return result

def read_file_with_user_get(cur_date,server_id):
	dat_lst = []
	OUT_PUT_PATH_LST=get_server_path(cur_date)
	if int(server_id) == -1:
		return dat_lst

	if not cur_date:
		return dat_lst
	log_path=OUT_PUT_PATH_LST[int(server_id)].format(cur_date=cur_date,use_path='tables')
	if os.path.exists(log_path ):
		union_count_file_path=log_path +'UNION_SHOP'
		if os.path.exists(union_count_file_path):
			f = open(union_count_file_path, 'r')
			dat_lst = pickle.load(f)

	return dat_lst
