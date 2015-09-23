# -*- coding:utf-8 -*-


"""
特殊副本通用表头
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

抓宠	参与人数	总参与次数	完成人数	总完成次数	到达要求人数	参与率	成功率
PS：挑战次数=角色挑战次数
"""

import datetime

from apps.game_manager.util import dat_log_util
from apps.config import game_config


def get_table(search_start_date, search_end_date):
    """
        获取展示表格
        register_start_date 注册开始时间
        register_end_date 注册结束时间
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """
    # 获取搜索区间日志
    new_log_lst = dat_log_util.read_file_with_user_level_state("GOLD_STAGE_CHALLENGE", search_start_date, search_end_date)

    table_lst = []
    search_days = (search_end_date - search_start_date).days+1
    if new_log_lst:
     for _day in xrange(search_days):
            new_log = new_log_lst[_day]
            new_log.sort(lambda x, y: cmp(x[0], y[0]))
            row_date = search_start_date + datetime.timedelta(days=_day)
            for _lv in new_log:
                stage_config = game_config.get_stages_config(int(_lv[0]))
                # 副本名称
                stage_name = stage_config['stageInfo']+"_"+str(stage_config['id'])
                join_user_num = _lv[1]  # 参与人数
                join_num = _lv[2] # 总参与次数
                win_user_num = _lv[3] # 完成人数
                complete_count = _lv[4] # 总完成次数
                all_user_num = _lv[5] # 到达要求人数
                join_rate = _lv[6] # 参与率
                win_rate = _lv[7] # 成功率
                row_lst = [
                    row_date.strftime('%m/%d/%Y'),  # 日期
                    stage_name,# 关卡名称
                    join_user_num,  # 参与人数
                    win_user_num, # 完成人数
                    all_user_num, # 到达要求人数
                    str(join_rate * 100)+"%", # 参与率
                    join_num, # 总参与次数
                    complete_count, # 总完成次数
                    str(win_rate * 100)+"%" # 成功率
                ]
                table_lst.append(row_lst)
    return table_lst