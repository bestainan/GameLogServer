# -*- coding:utf-8 -*-
"""
    修改玩家信息
"""
from apps.logs.action_gm import action_base_gm
from apps.game_manager import game_manage_define


def log(manager, server_id, user_id, change_key, old_value, new_value):
    """
        输出日志
    """
    action = game_manage_define.GM_ACTION_EDIT_PLAYER

    log_lst = action_base_gm.log_base(manager)

    log_lst.append(str(action))
    log_lst.append(str(server_id))
    log_lst.append(str(user_id))
    log_lst.append(str(change_key))
    log_lst.append(str(old_value))
    log_lst.append(str(new_value))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['server_id'] = log_part_lst[1]
    result['user_id'] = log_part_lst[2]
    result['key'] = log_part_lst[3]
    result['old'] = log_part_lst[4]
    result['new'] = log_part_lst[5]

    return result
