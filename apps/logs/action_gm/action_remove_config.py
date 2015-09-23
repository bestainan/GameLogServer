# -*- coding:utf-8 -*-
"""
    删除配置文件
"""
from apps.logs.action_gm import action_base_gm
from apps.game_manager import game_manage_define


def log(manager, file_name):
    """
        输出日志
    """
    action = game_manage_define.GM_ACTION_REMOVE_CONFIG
    log_lst = action_base_gm.log_base(manager)

    log_lst.append(str(action))
    log_lst.append(str(file_name))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['file'] = log_part_lst[1]

    return result
