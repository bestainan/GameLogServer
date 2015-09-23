# -*- coding:utf-8 -*-
"""
    宝物升级强化
"""

from apps.logs.action import action_base
from apps.utils import game_define


def log(user, treasure_old_tid, treasure_old_exp, treasure_new_exp, treasure_old_level, treasure_new_level, material_treasure_tid_lst, cost_gold):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_TREASURE_LEVEL_UP
    cur_gold = user.player.get_gold()
    total_cost_gold = user.player.total_cost_gold

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(treasure_old_tid))
    log_lst.append(str(treasure_old_exp))
    log_lst.append(str(treasure_new_exp))
    log_lst.append(str(treasure_old_level))
    log_lst.append(str(treasure_new_level))
    log_lst.append(str(material_treasure_tid_lst))
    log_lst.append(str(cost_gold))
    log_lst.append(str(cur_gold))
    log_lst.append(str(total_cost_gold))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['treasure_id'] = int(log_part_lst[1])
    result['treasure_old_exp'] = int(log_part_lst[2])
    result['treasure_new_exp'] = int(log_part_lst[3])
    result['treasure_old_level'] = int(log_part_lst[4])
    result['treasure_new_level'] = int(log_part_lst[5])
    result['treasure_level_up_material'] = action_base.get_val(log_part_lst, 6, [], True)
    result['cost_gold'] = int(log_part_lst[7])
    result['cur_gold'] = int(log_part_lst[8])
    result['total_cost_gold'] = int(log_part_lst[9])
    result['old_gold'] = result['cur_gold'] + result['cost_gold']
    return result