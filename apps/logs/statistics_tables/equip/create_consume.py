# -*- coding:utf-8 -*-

"""
英雄产出、消耗统计（日新增英雄情况）

注册时间	开始时间	20100919	结束时间	20100919			"查询说明：
1.若输入注册时间，则查询表示查询注册玩家在查询时间段活跃用户的信息
2.若不输入注册时间，则查询表示查询在查询时间段的活跃玩家信息
3.查询玩家等级区间可以调整，最小等级1级无法调整"

查询时间	开始时间	20100920	结束时间	20100923

渠道查询	所有渠道	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
分区查询	全服	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）
玩家最大等级		（最大等级为游戏设定英雄最大等级，后期等级变化后可调整）
玩家最小等级		（最小等级为1级）
英雄名称		产出							消耗	收邮件	礼包	GM指令
种类	星级	手工激活	钻石单抽	钻石十连抽	普通副本产出	精英副本产出	抓宠	创建角色	转化
皮卡丘	1星
皮卡丘	2星
…	…
妙蛙种子	1星
妙蛙种子	2星
…	…

"""

from apps.utils import game_define
from apps.config import game_config
from apps.game_manager.util import dat_log_util
import math
def get_create_table(search_start_date, search_end_date, server_id):
    #获取搜索区间日志
    new_log_lst = dat_log_util.read_file_with_filename("CREATE_EQUIP",search_start_date,search_end_date,server_id,'tables')
    search_monster_log_list = []
    create_monster_action = set()
    head_name_lst = []

    for monster_log in new_log_lst:
        search_monster_log_list.append(monster_log)
        for action,num in monster_log[1].items():
            create_monster_action.add(action)

    for _act in create_monster_action:
        head_name_lst.append(game_define.EVENT_LOG_ACTION_DICT[_act])

    table_lst = []
    for create_monster_log in search_monster_log_list:
        item_config = game_config.get_item_config(create_monster_log[0])
        _name = item_config['name']
        row_lst = [
            _name,
        ]
        for _act in create_monster_action:
            row_lst.append(str(create_monster_log[1].get(_act, 0)))
        table_lst.append(row_lst)
    return table_lst, head_name_lst

def get_consume_table(search_start_date, search_end_date,server_id):
    #获取搜索区间日志
    new_log_lst = dat_log_util.read_file_with_filename("CONSUME_EQUIP",search_start_date,search_end_date,server_id,'tables')
    search_monster_log_list = []
    create_monster_action = set()
    head_name_lst = []
    for monster_log in new_log_lst:
        search_monster_log_list.append(monster_log)
        for action,num in monster_log[1].items():
            create_monster_action.add(action)

    for _act in create_monster_action:
        head_name_lst.append(game_define.EVENT_LOG_ACTION_DICT[_act])

    table_lst = []
    for create_monster_log in search_monster_log_list:
        item_config = game_config.get_item_config(create_monster_log[0])
        _name = item_config['name']
        row_lst = [
            _name,
        ]
        for _act in create_monster_action:
            row_lst.append(int(math.fabs(create_monster_log[1].get(_act, 0))))
        table_lst.append(row_lst)
    return table_lst, head_name_lst

