# -*- coding:utf-8 -*-
"""
    添加回复bug系统邮件
"""
from apps.logs.action_gm import action_base_gm
from apps.game_manager import game_manage_define


def log(manager, mail):
    """
        输出日志
    """
    action = game_manage_define.GM_ACTION_ADD_BUG_MAIL
    log_lst = action_base_gm.log_base(manager)

    log_lst.append(str(action))
    log_lst.append(str(mail))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['mail'] = log_part_lst[1]

    return result
