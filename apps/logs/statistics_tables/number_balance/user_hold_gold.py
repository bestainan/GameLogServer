# -*- coding:utf-8 -*-

"""
    玩家金币持有（活跃用户）
开始时间	20100920	结束时间	20100923
渠道查询	所有渠道	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
分区查询	全服	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）
玩家最大等级		（最大等级为游戏设定英雄最大等级，后期等级变化后可调整）
玩家最小等级		（最小等级为1级）

表格说明：以下情况会根据《我爱皮卡丘》产出进行调整，具体调整情况须与cp协商
时间	持有数量	玩家数量	活跃玩家总数
20101919
20101919
20101919
PS：本表玩家数量均取角色数
"""

from apps.game_manager.util import dat_log_util

def get_table(search_start_date, server_id):
    # 获取搜索区间日志
    new_log_dict = dat_log_util.read_file_dict_with_filename("USER_HOLD_GOLD", search_start_date, server_id, 'tables')
    total_gold = str(new_log_dict.get('total_gold',0))
    total_user = str(new_log_dict.get('total_user',0))
    active_user = str(new_log_dict.get('active_user',0))

    row_lst = [[search_start_date.strftime('%m/%d/%Y'), total_gold, total_user, active_user]]
    return row_lst



