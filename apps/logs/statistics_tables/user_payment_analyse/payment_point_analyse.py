# -*- coding:utf-8 -*-

"""
付费点分析
注册时间	开始时间	20100919	结束时间	20100920
查询时间	开始时间	20100920	结束时间	20100923
游戏分区	总区服/一区/二区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道名称	所有	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）


"查询说明：
1.若输入注册时间，则查询表示查询注册玩家在查询时间段活跃用户的信息
2.若不输入注册时间，则查询表示查询在查询时间段的活跃用户信息"



付费点分析

档位	充值金额	人数	次数	金额占比	人数占比	次数占比
30元月卡
6元
50元
100元
200元
300元
648元
1998元
总数
"""
import datetime

from apps.game_manager.util import mysql_util
from apps.utils import game_define
from apps.config import game_config

def get_table(search_start_date, search_end_date, register_start_date=None, register_end_date=None, channel_id=-1, server_id=-1):
    """
        获取展示表格
        register_start_date 注册开始时间
        register_end_date 注册结束时间
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """
    row_lst = []
    # 获取商店数据表
    all_recharge_config = game_config.get_all_recharge_config()

    total_days = (search_end_date - search_start_date).days+1
    sum_recharge_money = 0
    sum_recharge_user_num = 0
    sum_recharge_num = 0
    # 把查询时间段内每天的数据相加求和
    for i in xrange(total_days):
        search_date = search_start_date + datetime.timedelta(days=i)
        date_str = "_"+search_date.strftime('%Y%m%d')
        recharge_money = mysql_util.get_spec_sum('add_rmb',search_date,search_date + datetime.timedelta(days=1),'shop_index=',-1,'EVENT_ACTION_RECHARGE_PLAYER'+str(date_str), game_define.EVENT_ACTION_RECHARGE_PLAYER, channel_id, server_id,register_start_date, register_end_date)
        recharge_user_num = mysql_util.get_spec_sum('uid',search_date,search_date + datetime.timedelta(days=1),'shop_index=',-1,'EVENT_ACTION_RECHARGE_PLAYER'+str(date_str), game_define.EVENT_ACTION_RECHARGE_PLAYER, channel_id, server_id,register_start_date, register_end_date)
        recharge_num = mysql_util.get_spec_sum('',search_date,search_date + datetime.timedelta(days=1),'shop_index=',-1,'EVENT_ACTION_RECHARGE_PLAYER'+str(date_str), game_define.EVENT_ACTION_RECHARGE_PLAYER, channel_id, server_id,register_start_date, register_end_date)
        sum_recharge_money += recharge_money
        sum_recharge_user_num += recharge_user_num
        sum_recharge_num += recharge_num

    for index, _config in enumerate(all_recharge_config):
        row = []
        sum_total_money = 0
        sum_total_user_num = 0
        sum_total_recharge_num = 0
        # 把查询时间段内每天的数据相加求和
        for i in xrange(total_days):
            search_date = search_start_date + datetime.timedelta(days=i)
            date_str = "_"+search_date.strftime('%Y%m%d')

            # 充值金额总数
            total_money = mysql_util.get_spec_sum('add_rmb',search_date,search_date + datetime.timedelta(days=1),'shop_index=', _config['id'],'EVENT_ACTION_RECHARGE_PLAYER'+str(date_str), game_define.EVENT_ACTION_RECHARGE_PLAYER, channel_id, server_id,register_start_date, register_end_date)
            sum_total_money += total_money

            # 人数
            total_user_num = mysql_util.get_spec_sum('uid',search_date,search_date + datetime.timedelta(days=1),'shop_index=', _config['id'],'EVENT_ACTION_RECHARGE_PLAYER'+str(date_str), game_define.EVENT_ACTION_RECHARGE_PLAYER, channel_id, server_id,register_start_date, register_end_date)
            sum_total_user_num += total_user_num

            # 次数
            total_recharge_num = mysql_util.get_spec_sum('',search_date,search_date + datetime.timedelta(days=1),'shop_index=', _config['id'],'EVENT_ACTION_RECHARGE_PLAYER'+str(date_str), game_define.EVENT_ACTION_RECHARGE_PLAYER, channel_id, server_id,register_start_date, register_end_date)
            sum_total_recharge_num += total_recharge_num

        # 档位
        money = _config['money']
        row.append(money)
        # 充值金额总数
        row.append(sum_total_money)
        # 人数
        row.append(sum_total_user_num)
        # 次数
        row.append(sum_total_recharge_num)

        # 金额比
        row.append(str(100*get_rate(sum_total_money,sum_recharge_money))+"%")
        # 人数比
        row.append(str(100*get_rate(sum_total_user_num,sum_recharge_user_num))+"%")
        # 次数比
        row.append(str(100*get_rate(sum_total_recharge_num,sum_recharge_num))+"%")
        row_lst.append(row)

    return row_lst

def get_rate(total_money,recharge_money):
    if recharge_money <= 0:
        return 0
    return round(float(total_money) / float(recharge_money), 4)











