# -*- coding:utf-8 -*-

"""
体力消耗统计

"""
from apps.utils import game_define
from apps.config import game_config
from apps.game_manager.util import dat_log_util
import math


def get_table(search_start_date, search_end_date,server_id):
    table_lst = dat_log_util.read_file_with_filename("STAMINA_COST",search_start_date,search_end_date,server_id,'tables')

    return table_lst

