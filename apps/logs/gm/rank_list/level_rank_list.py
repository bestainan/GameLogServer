#coding:utf-8

from apps.game_manager.util import dat_log_util


def get_table(search_start_date,server_id):
    """
        获取等级排行表
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """

    new_log_lst = []
    new_log_lst = dat_log_util.read_file_with_filename("LEVEL_RANK_LIST",search_start_date,search_start_date,server_id)

    return new_log_lst

