# -*- coding:utf-8 -*-
import datetime
import cPickle
import pickle
import os
from apps.utils import game_define
from apps.utils.logs_out_in_path import CATCH_LOGS_DAT_LST
from apps.utils.logs_out_path_of_server import get_server_path

CATCH_LOGS_DAT ='/zgame/HaiMaLogParse'


def read_file(action, from_date, to_date, server_id=10003, folder='all_action'):
    dat_lst = []
    total_days = (to_date - from_date).days + 1
    for i in xrange(total_days):
        # 每行的日期
        dat_dict = dict()
        cur_date = from_date + datetime.timedelta(days=i)
        # 注：用到通服的需要改
        if server_id == -1:
            for each_id in get_server_path(cur_date).keys():
                SERVER_LOGS_DATA_LST = get_server_path(cur_date)
                file_path = SERVER_LOGS_DATA_LST[each_id].format(cur_date=cur_date, use_path=folder)+game_define.EVENT_LOG_ACTION_SQL_NAME_DICT[action]
                print file_path
                if os.path.exists(file_path):
                    out_put_file = open(file_path, 'r')
                    dat_dict = pickle.load(out_put_file)
                    dat_lst.extend(dat_dict)
                    out_put_file.close()
                # print dat_dict
        else:
            SERVER_LOGS_DATA_LST = get_server_path(cur_date)
            file_path = SERVER_LOGS_DATA_LST[server_id].format(cur_date=cur_date, use_path=folder)+game_define.EVENT_LOG_ACTION_SQL_NAME_DICT[action]
            print file_path
            if os.path.exists(file_path):
                out_put_file = open(file_path, 'r')
                dat_dict = pickle.load(out_put_file)
                dat_lst.extend(dat_dict)
                out_put_file.close()

    return dat_lst

def read_file_with_filename(file_name, from_date, to_date, server_id=10003, folder='tables'):
    dat_lst = []
    total_days = (to_date - from_date).days + 1
    for i in xrange(total_days):
        dat_dict = dict()
        # 每行的日期
        cur_date = from_date + datetime.timedelta(days=i)
        SERVER_LOGS_DATA_LST = get_server_path(cur_date)
        file_path = SERVER_LOGS_DATA_LST[server_id].format(cur_date=cur_date, use_path=folder) + file_name
        print file_path
        if os.path.exists(file_path):
            out_put_file = open(file_path, 'r')
            dat_dict = pickle.load(out_put_file)
            dat_lst.extend(dat_dict)
            out_put_file.close()
        # print "ss",dat_dict

    return dat_lst

def read_file_with_filename_dict(file_name, from_date, to_date, server_id=10003, folder='tables'):
    dat_dict_all = dict()
    total_days = (to_date - from_date).days + 1
    for i in xrange(total_days):
        # 每行的日期
        dat_dict = dict()
        cur_date = from_date + datetime.timedelta(days=i)
        SERVER_LOGS_DATA_LST = get_server_path(cur_date)
        if -1 == server_id:
            for each_ser_id in SERVER_LOGS_DATA_LST.keys():
                file_path = SERVER_LOGS_DATA_LST[each_ser_id].format(cur_date=cur_date, use_path=folder) + file_name
                print file_path
                if os.path.exists(file_path):
                    out_put_file = open(file_path, 'r')
                    dat_dict = pickle.load(out_put_file)
                    for key, value in dat_dict.items():
                        dat_dict_all.setdefault(key, []).extend(value)
                    out_put_file.close()
            # print "ss",dat_dict
        else:
            file_path = SERVER_LOGS_DATA_LST[server_id].format(cur_date=cur_date, use_path=folder) + file_name
            print file_path
            if os.path.exists(file_path):
                out_put_file = open(file_path, 'r')
                dat_dict = pickle.load(out_put_file)
                for key, value in dat_dict.items():
                    dat_dict_all.setdefault(key, []).extend(value)
                out_put_file.close()
            # print "ss",dat_dict

    return dat_dict_all

def read_file_with_single_day(file_name, search_date, server_id=10003, folder='tables'):
    # dat_lst = []
    dat_dict = []
    # 每行的日期
    SERVER_LOGS_DATA_LST = get_server_path(search_date)
    path = SERVER_LOGS_DATA_LST[server_id].format(cur_date=search_date, use_path=folder)
    if os.path.exists(path):
        file_path = path + file_name
        print file_path
        if os.path.exists(file_path):
            out_put_file = open(file_path, 'r')
            dat_dict = pickle.load(out_put_file)
            # dat_lst.extend([dat_dict])
            out_put_file.close()
        print dat_dict
    return dat_dict

def read_file_with_user_level_state(file_name, from_date, to_date, server_id=10003, folder='tables'):
    dat_lst = []
    total_days = (to_date - from_date).days + 1
    for i in xrange(total_days):
        dat_dict = dict()
        # 每行的日期
        cur_date = from_date + datetime.timedelta(days=i)
        SERVER_LOGS_DATA_LST = get_server_path(cur_date)
        path = SERVER_LOGS_DATA_LST[server_id].format(cur_date=cur_date, use_path=folder)
        if os.path.exists(path):
            file_path = path + file_name
            print file_path
            if os.path.exists(file_path):
                out_put_file = open(file_path, 'r')
                dat_dict = pickle.load(out_put_file)
                dat_lst.extend([dat_dict])
                out_put_file.close()
            # print dat_dict
    return dat_lst

def read_file_dict_with_filename(file_name, search_date, server_id=10003, folder='tables'):
    dat_dict = dict()
    # 注：用到通服的需要改
    if server_id == -1:
        for each_id in get_server_path(search_date).keys():
            SERVER_LOGS_DATA_LST = get_server_path(search_date)
            if os.path.exists(SERVER_LOGS_DATA_LST[each_id].format(cur_date=search_date, use_path=folder)):
                file_path = SERVER_LOGS_DATA_LST[each_id].format(cur_date=search_date, use_path=folder) + file_name
                print file_path
                if os.path.exists(file_path):
                    out_put_file = open(file_path, 'r')
                    _tmp_dict = cPickle.load(out_put_file)
                    dat_dict = dict(dat_dict, **_tmp_dict)  # 两个字典合并
                    out_put_file.close()
    else:
        SERVER_LOGS_DATA_LST = get_server_path(search_date)
        if os.path.exists(SERVER_LOGS_DATA_LST[server_id].format(cur_date=search_date, use_path=folder)):
            file_path = SERVER_LOGS_DATA_LST[server_id].format(cur_date=search_date, use_path=folder) + file_name
            print file_path
            if os.path.exists(file_path):
                out_put_file = open(file_path, 'r')
                dat_dict = cPickle.load(out_put_file)
                out_put_file.close()
                # print dat_dict

    return dat_dict

#TODO:在此之上不要修改 在此之下添加自己函数

def read_action_single_file(file_name,uid,event,sreach_data,server_id,dir_name):

    event_id = int(event.split('-')[0])
    CATCH_LOGS_DAT_LST = get_server_path(sreach_data)
    action_file = CATCH_LOGS_DAT_LST[server_id].format(cur_date = sreach_data,use_path = dir_name)
    action_file = action_file  +str(uid) + os.sep + game_define.EVENT_LOG_ACTION_SQL_NAME_DICT[event_id]
    print action_file
    if os.path.exists(action_file):
        with open(action_file, 'r') as out_put_file:
            try:
                while out_put_file:
                    yield cPickle.load(out_put_file)
            except EOFError,e:
                print e

def walk_uid_file(from_date,to_date):
    # 遍历目录下所有文件
    # 'd:'+os.sep+'UID'
    # 返回文件绝对路径列表
    file_list = []
    total_days = (to_date - from_date).days + 1
    for i in xrange(total_days):
        cur_date = from_date + datetime.timedelta(days=i)
        cur_date = CATCH_LOGS_DAT +os.sep + 'data'+os.sep+ str(cur_date) +os.sep + 'ALL_USER_ACTION/'

        for dirname, subdirlist, filelist in os.walk(cur_date):
            for i in filelist:
                file_list.append(dirname + os.sep + i)
    return file_list


def cpickle_load_one_day(sreach_data,dir_name,file_name,server_id):
    dat_lst = []
    SERVER_LOGS_DATA_LST = get_server_path(sreach_data)
    action_file_abs_path = SERVER_LOGS_DATA_LST[int(server_id)].format(cur_date = sreach_data,use_path = dir_name) + file_name
    print action_file_abs_path
    if os.path.exists(action_file_abs_path):
        out_put_file = open(action_file_abs_path, 'r')
        dat_lst = cPickle.load(out_put_file)
    return dat_lst


def read_file_double_lst(file_name, from_date, to_date, server_id=10003, folder='tables'):
    dat_lst1 = []
    dat_lst2 = []
    total_days = (to_date - from_date).days + 1
    for i in xrange(total_days):
        tmp_lst = []
        # 每行的日期
        cur_date = from_date + datetime.timedelta(days=i)
        SERVER_LOGS_DATA_LST = get_server_path(cur_date)
        file_path = SERVER_LOGS_DATA_LST[server_id].format(cur_date=cur_date, use_path=folder) + file_name
        print file_path
        if os.path.exists(file_path):
            out_put_file = open(file_path, 'r')
            tmp_lst = pickle.load(out_put_file)
            dat_lst1.extend(tmp_lst[0])
            dat_lst2.extend([tmp_lst[1]])   # 表头 只取一个最合适的
            out_put_file.close()
        # print tmp_lst

    return dat_lst1, dat_lst2