#coding:utf-8
import datetime
from apps.game_manager.mysql import server_list
"""
    注：server 与 parse的此文件不一样 要各自修改!!
    注：server 与 parse的此文件不一样 要各自修改!!
    注：server 与 parse的此文件不一样 要各自修改!!
"""


def get_server_id_lst():
    """
        获取游戏服务器id列表 [10001,30001,10003,10004,10005,10006]
    """
    all_server_list = server_list.get_all_server(True)
    server_id_lst = []
    for item in all_server_list:
        server_id = int(item['id'])
        server_id_lst.append(server_id)
    return server_id_lst



def get_server_path(date_time, date_time1=None):
    if date_time >= datetime.date(2015, 06, 01):
        SERVER_LOGS_DATA_LST = {}
        for ser_id in get_server_id_lst():
            SERVER_LOGS_DATA_LST[ser_id] = "/home/ubuntu/data/HaiMaLogParse/%s/{cur_date}/{use_path}/" % (ser_id)

        return SERVER_LOGS_DATA_LST

    elif date_time <= datetime.date(2015, 05, 31):
        SERVER_LOGS_DATA_LST = {
            10003: '/home/ubuntu/data/FeiLiuLogParse/fengce_data/{cur_date}/{use_path}/',
            10004: '/home/ubuntu/data/FeiLiuLogParse/fengce_data/{cur_date}/{use_path}/',
            10005: '/home/ubuntu/data/FeiLiuLogParse/fengce_data/{cur_date}/{use_path}/',
            30001: "/home/ubuntu/data/FeiLiuLogParse/fengce_data/{cur_date}/{use_path}/",
            10001: "/home/ubuntu/data/FeiLiuLogParse/fengce_data/{cur_date}/{use_path}/",
            20003: "/home/ubuntu/data/FeiLiuLogParse/fengce_data/{cur_date}/{use_path}/",
            -1: '/home/ubuntu/data/FeiLiuLogParse/fengce_data/{cur_date}/{use_path}/',
        }

        return SERVER_LOGS_DATA_LST


def get_serverid_lst(from_date=None, to_date=None):
    if None == from_date and None == to_date:  # mysql 读取
        server_id_lst = get_server_id_lst()
        server_id_lst.append(-1)
        return server_id_lst
    elif from_date == "ying" and to_date == "fang":
        server_id_lst = [10003, 10004, 10005, 10006, -1]
        return server_id_lst

    elif from_date >= datetime.date(2015, 07, 01) and to_date >= datetime.date(2015, 07, 01):
        server_id_lst = get_server_id_lst()
        return server_id_lst

    elif from_date >= datetime.date(2015, 06, 01) and to_date >= datetime.date(2015, 06, 01):
        server_id_lst = [10003, 10004, 10005]
        return server_id_lst

    elif from_date >= datetime.date(2015, 05, 21) and to_date >= datetime.date(2015, 05, 21):
        server_id_lst = [20003]
        return server_id_lst
