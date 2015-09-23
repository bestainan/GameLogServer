# -*- coding:utf-8 -*-
"""
    玩家7天登陆领奖
"""

from apps.logs.action import action_base
from apps.utils import game_define


def log(user, gold, stone, free_draw, monster_str, equip_str, item_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_LOGIN_7_REWARD
    cur_gold = user.player.get_gold()
    cur_stone = user.player.get_stone()
    cur_free_draw = user.player.get_free_draw_material()

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(gold))
    log_lst.append(str(cur_gold))
    log_lst.append(str(stone))
    log_lst.append(str(cur_stone))
    log_lst.append(str(free_draw))
    log_lst.append(str(cur_free_draw))
    log_lst.append(str(monster_str))
    log_lst.append(str(equip_str))
    log_lst.append(str(item_str))

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
    result['add_stone'] = int(log_part_lst[3])
    result['cur_stone'] = int(log_part_lst[4])
    result['add_free_draw'] = int(log_part_lst[5])
    result['cur_free_draw'] = int(log_part_lst[6])
    result['add_monster_list'] = action_base.get_val(log_part_lst, 7, [], True)
    result['add_equip_list'] = action_base.get_val(log_part_lst, 8, [], True)
    result['add_item_list'] = action_base.get_val(log_part_lst, 9, [], True)
    result['old_gold'] = result['cur_gold'] - result['add_gold']
    result['old_stone'] = result['cur_stone'] - result['add_stone']
    result['old_free_draw'] = result['cur_free_draw'] - result['add_free_draw']
    return result