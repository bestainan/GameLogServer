# -*- coding:utf-8 -*-

import datetime
import pickle
import os
from apps.utils.logs_out_path_of_server import get_server_path

# 联盟用户签到信息统计
def get_table(search_start_date, search_end_date, server_id):
	result = read_file_with_user_get(search_start_date, search_end_date, server_id)
	return result

def read_file_with_user_get(search_start_date, search_end_date, server_id):
	dat_lst = []

	if int(server_id) == -1:
		return dat_lst

	if not search_end_date or not search_start_date:
		return dat_lst


	total_day = (search_end_date-search_start_date).days+1
	for i in xrange(total_day):
		cur_date = search_start_date+datetime.timedelta(days=i)
		OUT_PUT_PATH=get_server_path(cur_date)
		log_path=OUT_PUT_PATH[int(server_id)].format(cur_date=cur_date,use_path='tables')
		union_sign_file_path = log_path+  'UNION_SIGN'
		if os.path.exists(union_sign_file_path):
			for j in pickle.load(open(union_sign_file_path, 'r')):
				a = j
			dat_lst.append(a)
	return dat_lst