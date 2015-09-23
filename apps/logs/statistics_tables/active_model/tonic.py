# -*- coding:utf-8 -*-


"""
活动模块分析

日期	参与人数	总钓鱼次数	点击钓鱼界面次数	到达要求人数	参与率
2013/11/21
2013/11/22
2013/11/23
…

"""

import datetime
from apps.game_manager.util import dat_log_util
def get_table(search_start_date, search_end_date, register_start_date=None, register_end_date=None, channel_id=-1, cur_server_id=-1):
    """
        获取展示表格
        register_start_date 注册开始时间
        register_end_date 注册结束时间
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """
    # 获取搜索区间日志
    new_log_lst = []
    total_days = (search_end_date-search_start_date).days+1
    for i in xrange(total_days):
        search_date = search_start_date+datetime.timedelta(days=i)
        new_log = dat_log_util.read_file_with_single_day("TONIC", search_date, cur_server_id)
        if new_log:
            new_log.insert(0, search_date.strftime('%m/%d/%Y'))
            new_log[4] = str(new_log[4] * 100)+"%"
            new_log_lst.append(new_log)
    # new_log_lst = dat_log_util.read_file_with_user_level_state("TONIC", search_start_date, search_end_date, cur_server_id)
    # for index, new_log in enumerate(new_log_lst):
    #     cur_date = search_start_date + datetime.timedelta(days=index)
    #     new_log.insert(0, cur_date.strftime('%m/%d/%Y'))
    #     new_log[4] = str(new_log[4] * 100)+"%"
    return new_log_lst