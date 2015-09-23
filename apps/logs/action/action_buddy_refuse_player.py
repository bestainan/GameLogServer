# -*- coding:utf-8 -*-
"""
    拒绝好友 user 拒绝buddy_uid的申请
"""

from apps.logs.action import action_base
from apps.utils import game_define


def log(user, buddy_uid):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_BUDDY_REFUSE_PLAYER

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(buddy_uid))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['buddy_uid'] = int(log_part_lst[1])

    return result