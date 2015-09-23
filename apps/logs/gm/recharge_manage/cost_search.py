# -*- coding:utf-8 -*-
"""
    消费查询 解析只解析了钻石 金币 和 物品 修改可在GameLogParse中 special_keyword_prase文件中增删
"""
import datetime
from apps.game_manager.util import dat_log_util

READ_FILE_FLODER = 'gm_cost_search'
"""以上是五六七三个月的分别函数模块 调用时根据时间调用模块  注意：july七月需要传参 server_id 与 folder"""
def get_table(search_start_date, search_end_date, server_id=-1, uid=-1):
    if 'li' == uid:
        temp_lst = []
        new_log_lst = []
        #用户uid表 测试使用
        new_log_lst = dat_log_util.read_file_with_filename('GM_COST_SEARCH_LST', search_start_date, search_end_date, server_id, READ_FILE_FLODER)
        if new_log_lst:
            log_lst = set(new_log_lst)
            result = [[elem] for elem in log_lst]
            temp_lst.extend(result)
        new_log_head = [
            {'width': 50 ,'name': u'存在消费的用户UID'},
        ]
        return temp_lst, new_log_head
    elif uid:
        new_log_lst, new_log_head = dat_log_util.read_file_double_lst(str(uid), search_start_date, search_end_date, server_id, READ_FILE_FLODER)
        max_lst_len = 0
        max_lst = []
        for each_lst in new_log_head:
            if len(each_lst) > max_lst_len:
                max_lst = each_lst
                max_lst_len = len(each_lst)

        return new_log_lst, max_lst
    else:
        head_lst = [
            {'width':50,'name':u'消费时间'},
            {'width':50,'name':u'账号UID'},
            {'width':50,'name':u'服务器ID'},
            {'width':50,'name':u'平台ID'},
            {'width':50,'name':u'用户事件'},
            {'width':50,'name':u'消耗金币'},
            {'width':50,'name':u'消耗钻石'},
        ]
        temp_lst = [[u'请输入uid',u'请输入uid',u'请输入uid',u'请输入uid',u'请输入uid',u'请输入uid',u'请输入uid']]
        return temp_lst, head_lst

# import datetime
# get_table(datetime.date(2015,05,21),datetime.date(2015,05,21),-1,-1,-1)
# if datetime.date(2015,05,21) < datetime.date(2015,05,22):
#     print "ok"