# -*- coding:utf-8 -*-
"""
    装备转换返还
"""

from apps.logs.action import action_base
from apps.utils import game_define


def log(user, add_gold, add_gym_point, cur_gym_point, add_item_str, remove_equip_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_EQUIP_EXCHANGE_GET_ITEMS
    cur_gold = user.player.get_gold()

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(add_gold))
    log_lst.append(str(cur_gold))
    log_lst.append(str(add_gym_point))
    log_lst.append(str(cur_gym_point))
    log_lst.append(str(add_item_str))
    log_lst.append(str(remove_equip_str))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['add_gold'] = int(log_part_lst[1])
    result['cur_gold'] = int(log_part_lst[2])
    result['add_gym_point'] = int(log_part_lst[3])
    result['cur_gym_point'] = int(log_part_lst[4])
    result['add_item_list'] = action_base.get_val(log_part_lst, 5, [], True)
    result['remove_equip_list'] = action_base.get_val(log_part_lst, 6, [], True)
    result['old_gold'] = result['cur_gold'] - result['add_gold']
    result['old_gym_point'] = result['cur_gym_point'] - result['add_gym_point']
    return result