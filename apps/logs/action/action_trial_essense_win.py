# -*- coding:utf-8 -*-
"""
    熔炼精华胜利
"""

from apps.logs.action import action_base
from apps.utils import game_define


def log(user, cost_stamina, item_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_TRIAL_ESSENSE_WIN

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(cost_stamina))
    log_lst.append(str(item_str))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['cost_stamina'] = int(log_part_lst[1])
    result['add_item_list'] = action_base.list_parse(log_part_lst[2])
    return result