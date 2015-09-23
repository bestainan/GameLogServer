# -*- coding:utf-8 -*-
"""
    联盟 转让联盟领导
"""

from apps.logs.action import action_base
from apps.utils import game_define


def log(user, union_uid, union_name, new_leader_uid, union_level):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_UNION_SET_LEADER

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(union_uid))
    log_lst.append(str(union_name))
    log_lst.append(str(new_leader_uid))
    log_lst.append(str(union_level))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['union_uid'] = int(log_part_lst[1])
    result['union_name'] = log_part_lst[2]
    result['union_new_leader'] = int(log_part_lst[3])
    result['union_level'] = int(log_part_lst[4])

    return result