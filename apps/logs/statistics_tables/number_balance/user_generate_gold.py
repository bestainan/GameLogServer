# -*- coding:utf-8 -*-

"""
金币产出（部分情况根据后期修改）
开始日期	20101101	结束日期	20101101
分区查询	总/1区/2区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道标示	UC/91	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

日期 总计 冒险 按摩 礼包&签到 问答 邮件收取 钻石兑换 产出 消耗 剧情副本 精英副本 恶梦副本 淘金币出售 世界boss
2013/11/20	100000	100040
2013/11/21	150000	110000
2013/11/22	130000	140000
2013/11/23	90000	100000
2013/11/24	100000	90000
2013/11/25	90000	100000
2013/11/26	100000	90000
2013/11/27	90000	100000
2013/11/28	100000	90000
2013/11/29	90000	100000
2013/11/30	100000	90000

"""

from apps.utils import game_define
from apps.game_manager.util import dat_log_util


def get_table(search_start_date, server_id):
    """
        获取表格
    """
    # 获取搜索区间日志
    new_log_dict = dat_log_util.read_file_dict_with_filename("USER_GENERATE_GOLD", search_start_date, server_id)
    total_generate = new_log_dict.get('total_generate', 0)  # 总产出
    total_cost = new_log_dict.get('total_cost', 0)  # 总消耗
    actions = new_log_dict.get('actions', set())

    row_generate = ["0总产出", str(total_generate), str(get_rate(total_generate, total_generate) * 100) + "%"]
    row_cost = ["0总消耗", str(total_cost), str(get_rate(total_cost, total_cost) * 100) + "%"]
    table_lst = [row_generate, row_cost]
    for action in actions:
        row_lst = []
        action_cost = new_log_dict.get(action, 0)
        row_lst.append(game_define.EVENT_LOG_ACTION_DICT[action])
        row_lst.append(str(action_cost))
        row_lst.append(str(get_rate(action_cost, total_generate) * 100) + "%")
        table_lst.append(row_lst)

    return table_lst


def get_rate(num1, num2):
    """
        获取比例
    """
    if num2 <= 0:
        return 0
    return round(float(num1) / float(num2), 4)
