# -*- coding:utf-8 -*-
"""
    删除系统邮件
"""
from apps.logs.action_gm import action_base_gm
from apps.game_manager import game_manage_define


def log(manager, version):
    """
        输出日志
    """
    action = game_manage_define.GM_ACTION_DELETE_MAIL
    log_lst = action_base_gm.log_base(manager)

    log_lst.append(str(action))
    log_lst.append(str(version))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['version'] = log_part_lst[1]

    return result
