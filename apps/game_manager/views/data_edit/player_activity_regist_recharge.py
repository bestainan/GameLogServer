# -*- coding:utf-8 -*-

import collections
import datetime
import time
import string
import hashlib
from django.template import RequestContext
from apps.game_manager.views.log import daily_log
from django.shortcuts import render_to_response
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define
from apps.config import game_config
# 当前有用key
CUR_CON_STR_DIT = {u"itemId": u'获得物品：', u"stone": u'获得钻石：', u"gold": u'获得金币：',
                   u"freeDrop": u'获得精灵球：', u"id": u'已领取的充值奖励ID:'}
# 特殊处理的key
SPECIAL_CON_STR_LST = {u'itemId': u'itemNum'}


# templates player_activity_regist_recharge.html
def get_player_activity_regist_recharge_function(request, templates):
    """
        玩家运营数据编辑 豪华充值(签到)
        source {'uid': '1000099479',
                'complete_id': 20,
                'recharge_date': None,
                'has_reward_lst': [3, 13, 16, 22, 12, 17],
                'reward_end_date': datetime.date(2015, 8, 3),
                'active_id': 21
                }
        regist_recharge_config
        {"itemId": 81373, "stone": 0, "gold": 0, "freeDrop": 0, "itemNum": 10, "id": 30}
    """
    # 以函数的指针方式传递函数并调用
    function_name = 'data_edit.player_activity_regist_recharge.{function}'.format(function=set_player_activity_regist_recharge_function.__name__)
    print 'function_name', function_name
    server_list, platform_list = daily_log._get_server_list(None, None)
    try:
        server_list.remove(server_list[0])
    except:
        pass

    return_uid = '请输入uid'
    return_openid = "请输入openid"
    return_name = "请输入玩家昵称"
    if request.method == 'POST':
        user_uid = request.POST.get('user_uid')
        user_name = request.POST.get('user_name').encode('utf-8')
        user_openid = request.POST.get('user_openid')
        server_id = int(request.POST.get('server_id'))
        type_hidden = 'visible'
        cmem_url = server_define.CMEM_MAP[int(server_id)]

        head_lst = [
            {'name': u'名称'},
            {'name': u'数量'},
        ]

        if cmem_url:
            try:
                source = dict()
                if len(user_uid):
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_ACTIVITY_REGIST_RECHARGE_MODEL.format(user_id=user_uid))
                elif len(user_name):
                    name = hashlib.md5(user_name).hexdigest().upper()
                    key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                    user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    return_name = user_name
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_ACTIVITY_REGIST_RECHARGE_MODEL.format(user_id=user_uid))
                elif len(user_openid):
                    result = memcache.get_cmem_val(cmem_url, model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    user_uid = result['uid']
                    return_openid = user_openid
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_ACTIVITY_REGIST_RECHARGE_MODEL.format(user_id=user_uid))
                if source:
                    print 'source', source
                    # -----------------------------------不可改元素---------------------------------------------------------------#
                    # [[[0,1],[0,1]],[[0,1],[0,1]]] 三层[]
                    # ------------------------用户UID
                    uid = source.get('uid', 'None')
                    if uid != 'None':
                        uid_lst = [[u'用户UID', uid]]
                    else:
                        uid_lst = []
                    # ------------------奖励可领取最后时间
                    try:
                        reward_end_date = source['reward_end_date'].strftime('%Y-%m-%d')   # 运营活动奖励结束时间
                        reward_end_date_lst = [[u'玩家最后奖励领取时间', reward_end_date]]
                    except:
                        reward_end_date_lst = []
                    # ------------------运营活动当前版本recharge_date
                    try:
                        recharge_date = source['recharge_date'].strftime('%Y-%m-%d')   # 运营活动奖励结束时间
                        recharge_date_lst = [[u'今天充值时间', reward_end_date]]
                    except:
                        reward_end_date_lst = []
                    # ---------------- 玩家奖励信息
                    try:
                        reward_lst = source.get('has_reward_lst', [])                   # [1,2,3,4,5]
                        reward_str = ''                                                                 # 字符串
                        cur_reward_config_lst = game_config.get_all_regist_recharge_config()  # 策划填的配置表
                        if reward_lst:
                            for reward_id in reward_lst:
                                each_conf_lst = cur_reward_config_lst[str(reward_id)]       # 取出每条配置表
                                for key, each_int_value in each_conf_lst.items():           # 遍历每个key 值
                                    if each_int_value:                                      # 有值
                                        if key in CUR_CON_STR_DIT:                          # 且在配置字典
                                            if key in SPECIAL_CON_STR_LST.keys():           # 是特殊处理key
                                                each_item_str = game_config.get_item_config(each_int_value)['name']  # 取物品名
                                                each_item_str += u"： "
                                                each_item_val = each_conf_lst[SPECIAL_CON_STR_LST[key]]              # 取数量
                                            else:
                                                each_item_str = CUR_CON_STR_DIT[key]                         # 取物品名
                                                each_item_val = each_int_value                               # 取数量
                                            reward_str += each_item_str                                      # 字符串拼接名字
                                            reward_str += str(each_item_val) + ";   "                        # 字符串拼接值
                                        else:
                                            continue
                                    else:
                                        continue
                                reward_str += '-----------'
                            reward_lst = [[u'玩家奖励信息',reward_str]]
                            # print reward_lst
                    except:
                        reward_lst = []
                    # ------------------- 汇总 有就加入总表（三层列表 [[[],[]],[[],[]]]）
                    all_immutable_lst = []
                    if uid_lst:
                        all_immutable_lst.append(uid_lst)
                    if reward_end_date_lst:
                        all_immutable_lst.append(reward_end_date_lst)
                    if recharge_date_lst:
                        all_immutable_lst.append(recharge_date_lst)
                    if reward_lst:
                        all_immutable_lst.append(reward_lst)
                    # -----------------------------------可改元素-------------------------------------------------------------------------#
                    # {key1:{'name':X,'num':X},key2:{'name':X,'num':X}}
                    row_dict = collections.OrderedDict()  # 有序字典
                    # has_reward_lst complete_id  active_id ==>> 奖励表 充值到哪天 可领奖到哪天
                    # 单笔充值 可改元素 完成未交任务表 完成并交任务表
                    _has_reward_lst = source.get('has_reward_lst', [])
                    _complete_id = source.get('complete_id', 0)
                    _active_id = source.get('active_id', 0)
                    cur_reward_config_lst = game_config.get_all_regist_recharge_config()        # 策划填的配置表

                    key_str = string.join(['complete_id', '-1'], '$$')
                    row_dict[key_str] = {'name': u'签到已完成充值到第几天','num': _complete_id}
                    key_str = string.join(['active_id', '-1'], '$$')
                    row_dict[key_str] = {'name': u'签到可领取奖励到第几天','num': _active_id}
                    # key1 ==> "has_reward_lst$$1"
                    for i in xrange(1, len(cur_reward_config_lst)+1):
                        key_str = string.join(['has_reward_lst', str(i)], '$$')
                        if i >= 10:
                            if i in _has_reward_lst:
                                row_dict[key_str] = {'name': u'签到第__%s__天奖励状态(1/0:已领/未领)'%(str(i)), 'num': 1}
                            else:
                                row_dict[key_str] = {'name': u'签到第__%s__天奖励状态(1/0:已领/未领)'%(str(i)), 'num': 0}
                        else:
                            if i in _has_reward_lst:
                                row_dict[key_str] = {'name': u'签到第__0%s__天奖励状态(1/0:已领/未领)'%(str(i)), 'num': 1}
                            else:
                                row_dict[key_str] = {'name': u'签到第__0%s__天奖励状态(1/0:已领/未领)'%(str(i)), 'num': 0}
                    # -----------------------------------------------------------------------------------------------------------------------#
                else:
                    if user_uid:
                        return_uid = user_uid
                        if user_openid:
                            return_openid = user_openid
                        if user_name:
                            return_name = user_name

                return render_to_response(templates, locals(), RequestContext(request))

            except UnboundLocalError:
                type_hidden = 'hidden'
                return render_to_response(templates, locals(), RequestContext(request))

            except TypeError:
                type_hidden = 'hidden'
                return render_to_response(templates, locals(), RequestContext(request))

    else:
        row_list = []
        type_hidden = 'hidden'
        return render_to_response(templates, locals(), RequestContext(request))


# @require_permission
def set_player_activity_regist_recharge_function(value_dict):
    """
    修改memcache数据

    value_dict['tem_id'] has_reward_lst$$0 complete_id$$-1  active_id$$-1
    value_dict['input_value'] int
    """
    cmem_url = server_define.CMEM_MAP[int(value_dict['server_id'])]
    if cmem_url:
        if len(value_dict['user_id']):
            source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_ACTIVITY_REGIST_RECHARGE_MODEL.format(user_id=value_dict['user_id']))
            try:
                print 'this is source is: ', source
                # second_key 是int类型
                input_value = int(value_dict['input_value'])
                (first_key, second_key) = value_dict['item_id'].split('$$')
                second_key = int(second_key)
                if second_key >= 0:     # has_reward_lst
                    if input_value == 0:
                        source[first_key].remove(second_key)
                    elif input_value == 1:
                        source[first_key].append(second_key)
                    else:
                        return False
                elif second_key == -1:  # complete_id     active_id
                    source[first_key] = input_value
                else:
                    return False
            except:
                return False
            # source = {'uid': '1000103005', 'complete_id': 2, 'recharge_date': datetime.date(2015, 8, 1), 'has_reward_lst': [1], 'reward_end_date': datetime.date(2015, 7, 25), 'active_id': 4}
            # 传回 url  uid  以及数据 做外层检测
            result = memcache.put_cmem_val(cmem_url, model_define.PLAYER_ACTIVITY_REGIST_RECHARGE_MODEL.format(user_id=value_dict['user_id']), source)
            return result