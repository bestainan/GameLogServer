# -*- coding:utf-8 -*-

import datetime
import pickle
import os
from apps.utils.logs_out_path_of_server import get_server_path

# 好友信息统计


def get_table(search_start_date, search_end_date,  server_id):
    dat_lst=read_file_with_user_get('FRIEND_COUNT', search_start_date, search_end_date, server_id)
    return dat_lst

def read_file_with_user_get(file_name,search_start_date,search_end_date,server_id):
    data_lst = []
    if int(server_id) == -1:
        return data_lst
    total_day = (search_end_date-search_start_date).days+1
    print total_day
    for i in xrange(total_day):
        cur_date = search_start_date+datetime.timedelta(days=i)
        OUT_PUT_PATH_LST=get_server_path(cur_date)
        log_path=OUT_PUT_PATH_LST[int(server_id)].format(cur_date=cur_date,use_path='tables')
        file_path = log_path+ file_name
        if not os.path.exists(file_path):
            continue
        try:
            data_lst.append(pickle.load(open(file_path, 'r')))
        except :
            pass
    print data_lst
    return data_lst

