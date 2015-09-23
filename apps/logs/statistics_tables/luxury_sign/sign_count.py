# -*- coding:utf-8 -*-
"""
    豪华签到次数
"""

import datetime
from apps.game_manager.util import dat_log_util
from apps.logs import daily_log_dat


def get_table(search_start_date, search_end_date, server_id=-1):
    # 豪华签到
    new_sign_lst = dat_log_util.read_file_with_filename("LUXURY_SIGN", search_start_date, search_end_date, server_id, 'tables')
    # print new_sign_lst
    return new_sign_lst