# -*- coding:utf-8 -*-
"""
    商城
"""

from apps.logs.action import action_base
from apps.utils import game_define


def log(user, cost_gym_point, cur_gym_point, item_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_GYM_SHOP_BUY

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(cost_gym_point))
    log_lst.append(str(cur_gym_point))
    log_lst.append(str(item_str))
    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    # print("action_gym_shop log_part_lst: "+str(log_part_lst))
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['cost_gym_point'] = int(log_part_lst[1])
    result['cur_gym_point'] = int(log_part_lst[2])
    result['add_item_list'] = action_base.get_val(log_part_lst, 3, [], True)
    result['old_gym_point'] = result['cur_gym_point'] + result['cost_gym_point']

    return result