#coding:utf-8
# import os
# import cPickle
# from apps.utils import game_define
# from apps.game_manager import game_manage_define
# from apps.config import game_config
# from apps.game_manager.mysql import server_list
# from apps.utils import mem_key_name
# import datetime
from apps.logs.gm.gm_operation.view_description import *


OUT_PUT_PATH = "/home/ubuntu/data/ManagerLogParse/{cur_date}/{use_path}/"

monster_id_name = game_config.get_monster_config_with_id_name()
item_id_name, item_id_type = game_config.get_item_config_with_id_name()
all_server_dict = server_list.get_server_id_name_dict()

SERVER_HIDDEN_NAME_DICT = {
    1: u'隐藏',
    0: u'显示',
}

def get_table(account, search_date):
    head_list = [
        {'width': 50, 'name': u'时间'},
        {'width': 50, 'name': u'事件'},
        {'width': 50, 'name': u'操作'},
    ]
    table_list = []
    # action_list = []

    gm_action_dict = read_file_with_account(account, search_date)
    print gm_action_dict

    for action_dict in gm_action_dict:
        action = int(action_dict['action'])
        view_function = game_manage_define.GM_LOG_ACTION_NAME_DICT[action]
        print action_dict
        print "-------------------------------------"
        print view_function
        row_lst = [action_dict['log_time'].strftime("%Y-%m-%d %H:%M:%S"), str(game_manage_define.GM_LOG_ACTION_DICT[action])]
        content = eval(view_function)(action_dict)
        print content
        row_lst.append(content)
        table_list.append(row_lst)
        # if action == game_manage_define.GM_ACTION_MANAGER_LOGIN:
        #     row_lst = [action_dict['log_time'].strftime("%Y-%m-%d %H:%M:%S"), str(game_manage_define.GM_LOG_ACTION_DICT[action])]
        #     content = "上次登录时间:"+str(action_dict['last_login_time'])+"\t上次登录IP:"+str(action_dict['last_login_ip'])
        #     row_lst.append(content)
        #     table_list.append(row_lst)
        # elif action == game_manage_define.GM_ACTION_CHANGE_MONSTER:
        #     row_lst = [action_dict['log_time'].strftime("%Y-%m-%d %H:%M:%S"), str(game_manage_define.GM_LOG_ACTION_DICT[action])]
        #     mon_name = monster_id_name[int(action_dict['mon_tid'])]
        #     change_key = game_manage_define.GM_ACTION_CHANGE_KEY[action_dict['key']]
        #     content = "服务器ID:"+str(action_dict['server_id'])+"\t用户ID:"+str(action_dict['user_id'])+"\t宠物名称:"+mon_name.encode('utf-8')+"\t修改属性 "+change_key+":"+str(action_dict['old'])+"-->"+str(action_dict['new'])
        #     row_lst.append(content)
        #     table_list.append(row_lst)
        # temp_head = []
        # temp_content = []
        # for _action_key, _val in action_dict.items():
        #     if 'log_time' == _action_key:
        #         temp_content.insert(0, str(_val))
        #         temp_head.insert(0, {'width': 50, 'name': u'%s' % game_manage_define.GM_ACTION_VALUE[_action_key]})
        #         continue
            # if 'action' == _action_key:
            #     print _action_key
            #     print game_manage_define.GM_LOG_ACTION_DICT[_val]
            #     temp_content.insert(1, str(game_manage_define.GM_LOG_ACTION_DICT[_val]))
            #     print temp_content
            #     temp_head.insert(1, {'width': 50, 'name': u'%s' % game_manage_define.GM_ACTION_VALUE[_action_key]})
            #     print temp_head
            #     continue
        #     temp_head.append({'width': 50, 'name': u'%s' % game_manage_define.GM_ACTION_VALUE[_action_key]})
        #     temp_content.append(_val)
        # table_list.append(temp_content)
        # head_list.append(temp_head)
    try:
        return head_list, table_list
    except:
        return [], []


def read_file_with_account(account, search_date):
    account_file = OUT_PUT_PATH.format(cur_date=search_date, use_path="operation")
    account_file = account_file + account
    if os.path.exists(account_file):
        with open(account_file, 'r') as out_put_file:
            try:
                while out_put_file:
                    account_dict = cPickle.load(out_put_file)
                    return account_dict
            except EOFError, e:
                print e


# def read_single_operation_file(event_id, search_date):
#     action_file = OUT_PUT_PATH.format(cur_date=search_date, use_path="operation")
#     action_file = action_file + game_manage_define.GM_LOG_ACTION_NAME_DICT[event_id]
#     if os.path.exists(action_file):
#         with open(action_file, 'r') as out_put_file:
#             try:
#                 while out_put_file:
#                     operation_dict = cPickle.load(out_put_file)
#                     return operation_dict
#             except EOFError, e:
#                 print e
