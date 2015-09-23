# -*- coding:utf-8 -*-


"""
用户首次消费点分析
查询时间	开始时间	20100920	结束时间	20100923
分区查询	总/1区/2区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道标示	UC/91	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

首次钻石消费点								首次金币消费点

消费点	钻石数	人数	人数比率	钻石比率				消费点	金币数	人数	人数比率	钻石比率
十连抽								升级
单抽								进化
猜拳								猜拳
洗练								洗练
购买体力								购买体力
购买金币								购买金币
…								…
总数								总数
PS：本表人数均取角色数

"""


from apps.logs import daily_log_dat
from apps.utils import game_define
from apps.game_manager.util import dat_log_util

def get_cost_stone_table(search_start_date, server_id):
    """
        获取表格
    """
    table_lst = []
    # 获取首次消耗钻石的日志列表
    first_cost_stone_log_lst = dat_log_util.read_file_with_filename("USER_FIRST_STONE_CONSUME",search_start_date,search_start_date, server_id)

    for _log in first_cost_stone_log_lst:
        # print("_log:"+str(_log))
        _action = _log['action']
        action_name = game_define.EVENT_LOG_ACTION_DICT[_action]
        action_total_cost_stone = _log['stone_num']
        user_num = _log['user_num']
        cur_user_num_rate = _log['user_rate']
        first_cost_stone_rate = _log['stone_rate']
        row = [action_name, action_total_cost_stone, user_num, str(cur_user_num_rate * 100)+"%", str(first_cost_stone_rate * 100)+"%"]
        table_lst.append(row)

    return table_lst

def get_cost_gold_table(search_start_date, server_id):
    """
        获取表格
    """
    table_lst = []
    # 获取首次消耗钻石的日志列表
    first_cost_gold_log_lst = dat_log_util.read_file_with_filename("USER_FIRST_GOLD_CONSUME",search_start_date,search_start_date, server_id)

    for _log in first_cost_gold_log_lst:
        _action = _log['action']
        action_name = game_define.EVENT_LOG_ACTION_DICT[_action]
        action_total_cost_gold = _log['gold_num']
        user_num = _log['user_num']
        cur_user_num_rate = _log['user_rate']
        first_cost_gold_rate = _log['gold_rate']

        row = [action_name, action_total_cost_gold, user_num, str(cur_user_num_rate * 100)+"%", str(first_cost_gold_rate * 100)+"%"]
        table_lst.append(row)

    return table_lst