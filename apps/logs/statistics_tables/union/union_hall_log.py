# -*- coding:utf-8 -*-
from apps.game_manager.util import dat_log_util

READ_FILE_FLODER = 'tables'
READ_FILE_NMAE = 'UNION_HALL'


# 联盟殿堂信息统计
def get_table(search_start_date, server_id):
    tmp_list = dat_log_util.read_file_with_filename(READ_FILE_NMAE, search_start_date, search_start_date, server_id, READ_FILE_FLODER)
    return tmp_list
