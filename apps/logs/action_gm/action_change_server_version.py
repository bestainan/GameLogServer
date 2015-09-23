# -*- coding:utf-8 -*-
"""
    修改服务器版本信息
"""
from apps.logs.action_gm import action_base_gm
from apps.game_manager import game_manage_define


def log(manager, server_id, old_version, new_version):
    """
        输出日志
    """
    action = game_manage_define.GM_ACTION_CHANGE_SERVER_VERSION
    log_lst = action_base_gm.log_base(manager)

    log_lst.append(str(action))
    log_lst.append(str(server_id))
    log_lst.append(str(old_version))
    log_lst.append(str(new_version))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['server_id'] = log_part_lst[1]
    result['old'] = log_part_lst[2]
    result['new'] = log_part_lst[3]

    return result
