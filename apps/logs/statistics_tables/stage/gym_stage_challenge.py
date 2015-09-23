# -*- coding:utf-8 -*-


"""
副本通用表头
注册时间	开始时间	20100919	结束时间	20100920
查询时间	开始时间	20100920	结束时间	20100923
游戏分区	总区服/一区/二区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道名称	所有	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

挑战数	挑战这个副本的次数，以成功扣除体力为准
通过数	通过这个副本的次数
扫荡次数	钻石扫荡次数
成功率	通过数/挑战数
数据采集	选取2月份版本跟新首日用户数据进行分析


普通副本挑战次数，成功率

普通副本	副本名称	挑战数	通过数	扫荡次数	成功率	首次挑战次数	首次挑战成功次数
PS：挑战次数=角色挑战次数
"""

import datetime
from apps.utils import game_define
from apps.logs import daily_log_dat
from apps.config import game_config
from apps.game_manager.util import dat_log_util

def get_table(search_start_date, search_end_date, register_start_date=None, register_end_date=None, channel_id=-1, server_id=-1):
    """
        获取展示表格
        register_start_date 注册开始时间
        register_end_date 注册结束时间
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """
    # 获取搜索区间日志
    new_log_lst = dat_log_util.read_file_with_filename("GYM_STAGE_CHALLENGE", search_start_date, search_end_date,server_id,'tables')
    return new_log_lst
