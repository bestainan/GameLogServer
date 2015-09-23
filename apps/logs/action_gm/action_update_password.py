# -*- coding:utf-8 -*-
"""
    修改管理员密码
"""
import datetime

from apps.logs.action_gm import action_base_gm
from apps.game_manager import game_manage_define


def log(gm):
    """
        输出日志
    """
    action = game_manage_define.GM_ACTION_UPDATE_PASSWORD

    log_lst = action_base_gm.log_base(gm)

    log_lst.append(str(action))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])

    return result