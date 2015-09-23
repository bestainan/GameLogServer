# -*- coding:utf-8 -*-

import datetime
import pickle
import os
from apps.utils.logs_out_path_of_server import get_server_path

# 用户消耗统计


def get_table(search_start_date,user_id, server_id):
    dat_lst=read_file_with_user_get('user_cost_log', search_start_date, user_id, server_id)
    return dat_lst


def read_file_with_user_get(file_name,search_start_date,user_id,server_id):
    data_lst = []
    OUT_PUT_PATH_LST=get_server_path(search_start_date)
    print OUT_PUT_PATH_LST
    if not user_id or not search_start_date :
        return data_lst
    if int(server_id) == -1:
        return data_lst
    else:
		try:
			log_path = OUT_PUT_PATH_LST[int(server_id)].format(cur_date=search_start_date,use_path=file_name)

		except:
			return data_lst
    print log_path
    if os.path.exists(log_path):
        cur_date = search_start_date
        file_path = log_path+"%s" % (user_id)
        print file_path
        if not os.path.exists(file_path):
            return data_lst
        file=open(file_path,'r')
        for log_line in file.readlines():
            data_lst.append(eval(log_line))

    return data_lst
