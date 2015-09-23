# -*- coding:utf-8 -*-

"""
玩家金币消耗
开始时间	20100920	结束时间	20100923
渠道查询	所有渠道	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
分区查询	全服	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）
玩家最大等级		（最大等级为游戏设定英雄最大等级，后期等级变化后可调整）
玩家最小等级		（最小等级为1级）

观察不同用户人群的钻石流向
消耗类型	充值用户消耗人数	充值用户消耗次数	非充值用户消耗人数	非充值用户消耗次数	消耗钻石数量 消耗金额	消耗人数	消耗金额	消耗人数	消耗金额	消耗人数
商店道具购买
商定刷新
技能点购买
体力购买
金币购买
精英管卡重置
武斗榜次数购买
豪华签到
旅行商人
黑市商人
钻石扫荡
PS：本表玩家数量均取角色数

"""

from apps.utils import game_define
from apps.game_manager.util import dat_log_util

def get_table(search_start_date, server_id):
    # 获取搜索区间日志
    new_log_lst = dat_log_util.read_file_with_filename("USER_COST_GOLD_WITH_VIP",search_start_date,search_start_date ,server_id , 'tables')
    print new_log_lst
    table_lst = []
    # 遍历所有事件
    for new_log_dict in new_log_lst:
        action = new_log_dict.get('action',0)
        # 事件名称
        action_name = game_define.EVENT_LOG_ACTION_DICT[action]
        # 充值用户消耗人数
        recharge_user_num = str(new_log_dict.get('recharge_user_num',0))
        # 充值用户消耗次数
        recharge_user_log_num = str(new_log_dict.get('recharge_user_log_num',0))
        # 非充值用户的人数
        vip0_user_num = str(new_log_dict.get('vip0_user_num',0))
        # 非充值用户消耗次数
        vip0_user_log_num = str(new_log_dict.get('vip0_user_log_num',0))
        # vip0 消耗钻石
        vip0_cost_gold_num = str(-new_log_dict.get('vip0_cost_gold_num',0))
        # 消耗钻石数量
        total_cost_gold_num = str(-new_log_dict.get('total_cost_gold_num',0))

        #事件名称 充值用户消耗人数	充值用户消耗次数	非充值用户消耗人数	非充值用户消耗次数	消耗钻石数量  VIP0消耗金额	VIP0消耗人数
        row_lst = [action_name, recharge_user_num, recharge_user_log_num, vip0_user_num, vip0_user_log_num, total_cost_gold_num, vip0_cost_gold_num, vip0_user_num]
        # 遍历VIP
        for i in xrange(1, 13):
            vip_x_cost_gold_num = str(-new_log_dict.get('vip_%s_cost_gold_num'%i,0))
            vip_x_cost_gold_user_num = str(new_log_dict.get('vip_%s_cost_gold_user_num'%i,0))
            row_lst.append(vip_x_cost_gold_num)
            row_lst.append(vip_x_cost_gold_user_num)
        table_lst.append(row_lst)
    return table_lst
