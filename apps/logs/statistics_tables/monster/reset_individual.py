# -*- coding:utf-8 -*-

"""
英雄洗练统计
注册时间	开始时间	20100919	结束时间	20100919
查询时间	开始时间	20100920	结束时间	20100923
渠道查询	所有渠道	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
分区查询	全服	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）
玩家最大等级		（最大等级为游戏设定英雄最大等级，后期等级变化后可调整）
玩家最小等级		（最小等级为1级）

英雄名称	50次以内	50-100	100-150	...
皮卡丘
妙蛙种子
…
"""
from apps.config import game_config
from apps.game_manager.util import dat_log_util


def get_table(search_start_date, search_end_date, server_id):
    # 获取搜索区间日志
    new_log_lst = dat_log_util.read_file_with_filename("MONSTER_RESET_INDIVIDUAL", search_start_date, search_end_date,
                                                       server_id, "tables")
    # print new_log_lst
    table_lst = []
    for new_log in new_log_lst:
        monster_config = game_config.get_monster_config(new_log[0])
        _name = monster_config['name']
        row_lst = [_name]
        row_lst.extend(new_log[1:])
        table_lst.append(row_lst)
    return table_lst
