# -*- coding:utf-8 -*-

"""
玩家充值情况
查询时间	开始时间	20100920	结束时间	20100923
渠道查询	所有渠道	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
分区查询	全服	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）
玩家最大等级		（最大等级为游戏设定英雄最大等级，后期等级变化后可调整）
玩家最小等级		（最小等级为1级）


日期	6月人数	30元人数	98元人数	198元人数	328元人数	488元人数	2000元人数
20101010
20101010
20101010
20101010
20101010
PS：本表人数均取角色数
"""

import datetime
from apps.game_manager.util import mysql_util


def get_table(search_start_date, search_end_date, channel_id=-1, server_id=-1):
    table_result = []
    total_days = (search_end_date-search_start_date).days + 1
    for _day in xrange(total_days):
        row = []
        # 每行的日期
        row_date = search_start_date + datetime.timedelta(days=_day)
        date_str = '_' + row_date.strftime('%Y%m%d')
        # 插入数据
        row.append(row_date.strftime('%Y-%m-%d'))
        # 充值档
        for shop_id in xrange(1, 9):
            user_num = mysql_util.get_recharge_shop_index_uid_num('uid', 'EVENT_ACTION_RECHARGE_PLAYER'+str(date_str), row_date, 'shop_index', shop_id, channel_id, server_id)
            # 插入数据
            row.append(user_num)
        table_result.append(row)

    return table_result
