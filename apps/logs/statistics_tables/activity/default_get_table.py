#coding:utf-8


import cPickle
from apps.game_manager.util import dat_log_util
CATCH_LOGS_DAT ='/zgame/FeiLiuLogParse'
# CATCH_LOGS_DAT ='/zgame/HaiMaLogParse'


def get_table(search_date,dir_name,file_name,server_id):
    table_lst = dat_log_util.cpickle_load_one_day(search_date,dir_name,file_name,server_id)
    try:
        if len(table_lst[0]):
            return table_lst
        else:
            return []
    except:
        return []


def get_table_one_list(search_date,dir_name,file_name,server_id):
    table_lst = dat_log_util.cpickle_load_one_day(search_date,dir_name,file_name,server_id)
    if len(table_lst):
        return table_lst
    else:
        return []

