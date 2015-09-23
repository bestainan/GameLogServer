# -*- coding:utf-8 -*-

import pickle
import os
from apps.utils.logs_out_path_of_server import get_server_path

# 联盟用户副本信息统计

def get_table(search_start_date, server_id):
    result = read_file_with_user_get(search_start_date,server_id)
    return result


def read_file_with_user_get(search_start_date,server_id):
    dat_lst = []
    OUT_PUT_PATH_LST=get_server_path(search_start_date)
    if int(server_id) == -1:
        return dat_lst

    if not search_start_date :
        return dat_lst
    log_path=OUT_PUT_PATH_LST[int(server_id)].format(cur_date=search_start_date,use_path='tables')
    if os.path.exists(log_path):
        union_buy_reward_file_path = log_path+ 'UNION_STAGE'
        if os.path.exists(union_buy_reward_file_path):
            f = pickle.load(open(union_buy_reward_file_path,'r'))
            for i in f:
                dat_lst.append(i)

    return dat_lst
