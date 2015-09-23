#coding:utf-8

import pickle
from apps.game_manager.util import dat_log_util

def get_table(start_date_date, end_date_date):

    #遍历所有玩家文件夹
        #查询事件文件中是否有关键字cost_stone（消耗钻石）
    row_list = dict()
    action_file_abs_path = dat_log_util.walk_uid_file(start_date_date,end_date_date)
    print len(action_file_abs_path)
    raw_input('wait...')
    for file in action_file_abs_path:
        if 'EVENT_ACTION' in file:
            with open(file,'r') as f:
                action_file = pickle.load(f)
                for action in action_file:
                    if 'cost_stone' in action.keys():
                        if action['uid'] not in row_list:
                            row_list[action['uid']] = action['cost_stone']
                        else:
                            row_list[action['uid']] += action['cost_stone']

    table_lst = []
    row_list = sorted(row_list.items(), key=lambda d: d[1], reverse=True)
    top_num = xrange(1, len(row_list))
    for row,num in zip(row_list, top_num):
        row_list_append = ((num, row[0], row[1]))
        table_lst.append(row_list_append)


    return table_lst











