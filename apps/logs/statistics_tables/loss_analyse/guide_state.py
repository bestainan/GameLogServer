# -*- coding:utf-8 -*-


"""
    新手引导完成度（需要根据新手引导具体情况进行修订）
查询日期	20101101
分区查询	总/1区/2区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道标示	UC/91	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）


新手引导完成度	选取用户在新手引导中的每一步操作，新手引导机制需要与研发确认是否有记录请求

项目编号	项目名称	到达人数	完成人数	分步完成率	累积完成率
1	启动客户端
2	登入请求
3	创建角色请求
4	开场动画1
……	开场动画2
……
30
引导结束总计
PS：本表人数均取角色数

"""

from apps.logs import daily_log_dat
from apps.utils import game_define
from apps.game_manager.util import dat_log_util

def get_table(search_date, channel_id=-1, cur_server=-1):

    # new_log_lst = daily_log_dat.get_new_log_lst(search_date, search_date)
    # #获取全部新手引导日志
    # all_guide_log_lst = daily_log_dat.filter_logs(new_log_lst, action=game_define.EVENT_ACTION_FINISH_GUIDE)
    all_guide_log_lst = dat_log_util.read_file(game_define.EVENT_ACTION_FINISH_GUIDE, search_date, search_date, cur_server)
    # print all_guide_log_lst
    if channel_id >= 0:
        all_guide_log_lst = daily_log_dat.filter_logs(all_guide_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if cur_server >= 0:
        all_guide_log_lst = daily_log_dat.filter_logs(all_guide_log_lst, function=lambda x: x['server_id'] == cur_server)

    # 总共5个引导步骤 （1-6）
    total_user = daily_log_dat.get_set_num_with_key(all_guide_log_lst, 'uid')
    complete_user_dict = dict()
    guide_name = [u'宠物升级突破_4级开启', u'宠物升星_17级开启', u'宠物进化_10级开启', u'宠物技能升级_13级开启', u'宠物洗练_30级开启', u'宠物装备强化_23级开启', u'新队伍位置_6级开启']

    # 引导步骤按解锁等级排序
    unlock_order = [1, 7, 6, 3, 4, 2, 5]
    for i in xrange(1, 8):
        # 当前引导的所有日志
        guide_index_log_lst = daily_log_dat.filter_logs(all_guide_log_lst, function=lambda x: x['guide_id'] == i)
        complete_user_num = daily_log_dat.get_set_num_with_key(guide_index_log_lst, 'uid')
        complete_user_dict[i] = complete_user_num

    table_result = []
    for i in unlock_order:
        next_num = complete_user_dict.get(i+1,0)
        row = [
            search_date.strftime('%Y-%m-%d'),
            i,
            guide_name[i-1],
            complete_user_dict[i],  # 完成人数
        ]
        table_result.append(row)

    return table_result


# 获取比率
def _get_next_num_rate(next_num, complete_user_dict_i):
    """

    """
    if complete_user_dict_i <= 0:
        return 0
    return round(float(next_num) / float(complete_user_dict_i), 2)


# 获取比率
def _get_complete_user_dict_rate(complete_user_dict_i, total_user):
    """

    """
    if total_user <= 0:
        return 0
    return round(float(complete_user_dict_i) / float(total_user), 2)





