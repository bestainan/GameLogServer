# -*- coding:utf-8 -*-
"""
    获取月卡钻石
"""

from apps.logs.action import action_base
from apps.utils import game_define


def log(user, add_stone):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_MONTH_CARD
    cur_stone = user.player.get_stone()

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(add_stone))
    log_lst.append(str(cur_stone))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['add_stone'] = int(log_part_lst[1])
    result['cur_stone'] = int(log_part_lst[2])
    result['old_stone'] = result['cur_stone'] - result['add_stone']
    return result