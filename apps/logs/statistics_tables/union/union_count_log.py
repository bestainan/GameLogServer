# -*- coding:utf-8 -*-

import datetime

import pickle
import os
from apps.utils.logs_out_path_of_server import get_server_path

# 联盟信息统计
def get_table(search_start_date, search_end_date,server_id):
	result = read_file_with_user_get(search_start_date,search_end_date,server_id)
	return result

def read_file_with_user_get(search_start_date,search_end_date,server_id):
	dat_lst=[]
	OUT_PUT_PATH_LST=get_server_path(search_start_date)
	#print server_id
	if int(server_id) == -1:
		return dat_lst
	# else:
	# 	try:
	# 		 # log_path = OUT_PUT_PATH_LST[int(server_id)].format(cur_date=search_start_date,use_path='tables')
	# 	except:
	# 		return dat_lst
	if not search_start_date or not search_end_date:
		return dat_lst

	#print total_day
	total_day = (search_end_date-search_start_date).days+1
	print total_day
	for i in xrange(total_day):
		cur_date = search_start_date+datetime.timedelta(days=i)
		path=OUT_PUT_PATH_LST[int(server_id)].format(cur_date=cur_date,use_path='tables')
		print path
		union_count_file_path=path + 'UNION_COUNT'
		print union_count_file_path
		#print union_count_file_path
		if os.path.exists(union_count_file_path):
			print 'do it '
			f = open(union_count_file_path, 'r')
			for j in  pickle.load(f):
				print j
				dat_lst.append(j)
	return dat_lst