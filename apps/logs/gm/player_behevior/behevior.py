#coding:utf-8

from apps.game_manager.util import dat_log_util
from apps.utils import game_define

def get_table(uid,event,sreach_data,server_id,dir_name):
    head_list = []
    table_list = []

    event = event.split('-')[0]
    uid_action_dict = dat_log_util.read_action_single_file("UID_ACTION_PATH",uid, event,sreach_data,server_id,dir_name)

    for action_dict in uid_action_dict:
        temp_head = []
        temp_content = []
        for _action_key,_val in action_dict.items():
            if 'log_time' == _action_key:
                temp_content.insert(0,str(_val))
                temp_head.insert(0,{'width': 50, 'name': u'%s' % game_define.LOG_EVENT_VALUE[_action_key]})
            if 'install' == _action_key:
                temp_head.insert(1,{'width': 50, 'name': u'%s' % game_define.LOG_EVENT_VALUE[_action_key]})
                temp_content.insert(1,action_dict[_action_key])
            temp_head.append({'width': 50, 'name': u'%s' % game_define.LOG_EVENT_VALUE[_action_key]})
            temp_content.append(_val)
        table_list.append(temp_content)
        head_list.append(temp_head)
    try:
        return head_list[0],table_list
    except:
        return [],[]