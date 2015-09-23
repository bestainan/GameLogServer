# -*- coding:utf-8 -*-

"""
日常消费点分布
注册时间	开始时间	20100919	结束时间	20100920					"查询说明：
1.若输入注册时间，则查询表示查询注册玩家在查询时间段活跃用户的信息
2.若不输入注册时间，则查询表示查询在查询时间段的活跃用户信息"
查询时间	开始时间	20100920	结束时间	20100923
游戏分区	总区服/一区/二区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道名称	所有	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

钻石消费点分布								金币消费点分布

消费点	钻石数	人数	次数	参与率	钻石消耗占比	人数占比		消费点	金币数	人数	次数	参与率	金币消耗占比	人数占比
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
from apps.game_manager.util import mysql_util
def get_cost_stone_table(search_start_date, server_id):
    """
        获取展示表格
        register_start_date 注册开始时间
        register_end_date 注册结束时间
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """
    # 获取搜索区间日志
    new_log_dict = dat_log_util.read_file_dict_with_filename("DAILY_CONSUME_DISTRIBUTED_STONE",search_start_date, server_id)
    # print new_log_dict
    # 今天登录设备数
    date_str = "_"+search_start_date.strftime('%Y%m%d')
    today_device_num = mysql_util.get_today_num('dev_id','EVENT_ACTION_ROLE_LOGIN'+str(date_str),search_start_date,game_define.EVENT_ACTION_ROLE_LOGIN)
    actions = new_log_dict.get("actions", set())
    table_lst =[]
    for _action in actions:
        action_name = game_define.EVENT_LOG_ACTION_DICT[_action]
        action_generate_stone = -new_log_dict.get('action_%s_stone' % _action, 0)
        user_num = new_log_dict.get('action_%s_user_num' % _action, 0)
        action_cost_num = new_log_dict.get('action_%s_log_num'% _action, 0)
        action_stone_rate = -new_log_dict.get('action_%s_stone_rate'% _action, 0)
        cur_user_num_rate = new_log_dict.get('action_%s_user_rate' % _action, 0)
        take_part_rate = _get_rate(user_num, today_device_num)

        row = [action_name, action_generate_stone, user_num, action_cost_num, str(take_part_rate * 100)+"%", str(action_stone_rate* 100)+"%", str(cur_user_num_rate* 100)+"%"]
        table_lst.append(row)
    return table_lst

    # 获取比率
def _get_rate(cost, total):
    """
        获取ltv值
    """
    if total <= 0:
        return 0
    return round(float(cost) / float(total), 2)


def get_cost_gold_table(search_start_date, server_id):
    """
        获取展示表格
        register_start_date 注册开始时间
        register_end_date 注册结束时间
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """
    # 获取搜索区间日志
    new_log_dict = dat_log_util.read_file_dict_with_filename("DAILY_CONSUME_DISTRIBUTED_GOLD",search_start_date, server_id)
    # 今天登录设备数
    date_str = "_"+search_start_date.strftime('%Y%m%d')
    today_device_num = mysql_util.get_today_num('dev_id','EVENT_ACTION_ROLE_LOGIN'+str(date_str),search_start_date,game_define.EVENT_ACTION_ROLE_LOGIN)
    actions = new_log_dict.get("actions", set())
    table_lst =[]
    for _action in actions:
        action_name = game_define.EVENT_LOG_ACTION_DICT[_action]
        action_generate_stone = -new_log_dict.get('action_%s_gold' % _action, 0)
        user_num = new_log_dict.get('action_%s_user_num' % _action, 0)
        action_cost_num = new_log_dict.get('action_%s_log_num'% _action, 0)
        action_stone_rate = -new_log_dict.get('action_%s_gold_rate'% _action, 0)
        cur_user_num_rate = new_log_dict.get('action_%s_user_rate' % _action, 0)
        take_part_rate = _get_rate(user_num, today_device_num)

        row = [action_name, action_generate_stone, user_num, action_cost_num, str(take_part_rate * 100)+"%", str(action_stone_rate * 100)+"%", str(cur_user_num_rate * 100)+"%"]
        table_lst.append(row)
    return table_lst






