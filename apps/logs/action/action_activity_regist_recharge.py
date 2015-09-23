# -*- coding:utf-8 -*-
"""
    活动1__豪华签到
"""
from apps.logs.action import action_base
from apps.utils import game_define


def log(user, activity_tid, add_gold, add_stone, add_free_draw, item_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_ACTIVITY_REGIST_RECHARGE
    cur_gold = user.player.get_gold()
    cur_stone = user.player.get_stone()
    cur_free_draw = user.player.get_free_draw_material()
    log_lst = action_base.log_base(user)
    log_lst.append(str(action))
    log_lst.append(str(activity_tid))
    log_lst.append(str(add_gold))
    log_lst.append(str(cur_gold))
    log_lst.append(str(add_stone))
    log_lst.append(str(cur_stone))
    log_lst.append(str(add_free_draw))
    log_lst.append(str(cur_free_draw))
    log_lst.append(str(item_str))

    log_str = '$$'.join(log_lst)

    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['activity_tid'] = int(log_part_lst[1])
    result['add_gold'] = int(log_part_lst[2])
    result['cur_gold'] = int(log_part_lst[3])
    result['add_stone'] = int(log_part_lst[4])
    result['cur_stone'] = int(log_part_lst[5])
    result['add_free_draw'] = int(log_part_lst[6])
    result['cur_free_draw'] = int(log_part_lst[7])
    result['add_item_list'] = action_base.get_val(log_part_lst, 8, [], True)
    result['old_gold'] = result['cur_gold'] - result['add_gold']
    result['old_stone'] = result['cur_stone'] - result['add_stone']
    result['old_free_draw'] = result['cur_free_draw'] - result['add_free_draw']
    return result

