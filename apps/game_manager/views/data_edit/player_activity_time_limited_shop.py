# -*- coding:utf-8 -*-

import collections
import datetime
import time
import hashlib
from django.template import RequestContext
from apps.game_manager.views.log import daily_log
from django.shortcuts import render_to_response
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define
from apps.config import game_config
# 当前有用key
CUR_CON_STR_DIT = {
                    u"id": u' @___兑换商城事件ID： ',
                    u"stoneNeed": u' 使用钻石： ', u'idItemNeed': u' 使用物品 ：',
                    u"goldNeed": u' 使用金币： ',
                    u"stoneGet": u' 兑换——钻石： ', u"goldGet": u' 兑换——金币： ', u"equipmentId": u' 兑换——装备： ',
                    u"idItemGet": u' 兑换——物品： ',
                    u"freeDrawGet": u' 兑换——精灵球： ', u"leftTimes": u' 可兑换次数：',
                  }
# 特殊处理的key
SPECIAL_CON_STR_LST = {u'numItemNeed': u'idItemNeed',  u'idItemGet': u'numItemGet'}

# 商店购买次数所用列表 用来区分更改的商店购买次数
SHOP_BUY_NOT_ITEM_LST = {u"stoneGet": u'钻石',
                         u"goldGet": u'金币',
                         u"freeDrawGet": u'精灵球',
                        }


# templates player_activity_time_limited_shop.html
def get_player_activity_time_limited_shop_function(request, templates):
    """
        玩家运营数据编辑 假日商店
        source {'reward_end_date': datetime.date(2015, 8, 15),
                'num_dict': {2: 3, 3: 2, 5: 1, 7: 1},
                'version': u'20150716_22_09',
                'uid': '1000103005'}
        time_limited_shop_config
                {"goldGet": 0, "stoneGet": 0, "stoneNeed": 0, "idItemGet": 80048,
                "numItemGet": 10, "numItemNeed": 1, "idItemNeed": 82009, "leftTimes": 1,
                 "freeDrawGet": 0, "goldNeed": 0, "id": 12}}
    """
    # 以函数的指针方式传递函数并调用
    function_name = 'data_edit.player_activity_time_limited_shop.{function}'.format(function=set_player_activity_time_limited_shop_function.__name__)
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
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_ACTIVITY_TIME_LIMITED_SHOP_MODEL.format(user_id=user_uid))
                elif len(user_name):
                    name = hashlib.md5(user_name).hexdigest().upper()
                    key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                    user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    return_name = user_name
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_ACTIVITY_TIME_LIMITED_SHOP_MODEL.format(user_id=user_uid))
                elif len(user_openid):
                    result = memcache.get_cmem_val(cmem_url, model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    user_uid = result['uid']
                    return_openid = user_openid
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_ACTIVITY_TIME_LIMITED_SHOP_MODEL.format(user_id=user_uid))
                if source:
                    # print 'source', source
                    row_dict = collections.OrderedDict()  # 有序字典
                    # -----------------------------------不可改元素---------------------------------------------------------------#
                    # [[[0,1],[0,1]],[[0,1],[0,1]]] 三层[]
                    # ------------------------用户UID
                    uid = source.get('uid', 'None')
                    if uid != 'None':
                        uid_lst = [[u'用户UID', uid]]
                    else:
                        uid_lst = []
                    # ------------------运营活动奖励结束时间
                    try:
                        reward_end_date = source['reward_end_date'].strftime('%Y-%m-%d')   # 运营活动奖励结束时间
                        reward_end_date_lst = [[u'运营活动奖励结束时间', reward_end_date]]
                    except:
                        reward_end_date_lst = []
                    # ------------------运营活动当前版本
                    try:
                        version = source['version']   # 运营活动当前版本
                        version_lst = [[u'运营活动当前版本', version]]
                    except:
                        version_lst = []
                    # ---------------- 玩家已触发购买信息-------------------------------------
                    try:
                        completed_dic = source.get('num_dict', {})                # 已兑换信息表
                        reward_lst = []
                        for shop_even_id, get_item_num in completed_dic.items():  # 事件字典
                            reward_str = ''                                       # 字符串
                            if completed_dic:
                                cur_shop_even_id_config_dic = game_config.get_time_limited_shop_config_with_id(int(shop_even_id))  # 策划填的配置表中的一条
                                for key, each_int_value in cur_shop_even_id_config_dic.items():             # 遍历每个key 与 值
                                    if each_int_value:                                                      # 有值
                                        if key in CUR_CON_STR_DIT:                                          # 且在配置字典
                                            if key in SPECIAL_CON_STR_LST.keys():                           # 特殊处理key
                                                if u'idItemGet' == key:  # 商城兑换物品要加“兑换”字符串
                                                    each_item_str = u'兑换——'
                                                    each_item_str += game_config.get_item_config(each_int_value)['name']    # 取物品名
                                                    each_item_str += u"： "
                                                    each_item_val = cur_shop_even_id_config_dic[SPECIAL_CON_STR_LST[key]]  # 取数量
                                                else:
                                                    each_item_str = game_config.get_item_config(each_int_value)['name']    # 取物品名
                                                    each_item_str += u"： "
                                                    each_item_val = cur_shop_even_id_config_dic[SPECIAL_CON_STR_LST[key]]  # 取数量
                                            else:
                                                each_item_str = CUR_CON_STR_DIT[key]                         # 取物品名
                                                each_item_val = each_int_value                               # 取数量
                                            reward_str += each_item_str                                      # 字符串拼接名字
                                            reward_str += str(each_item_val) + ";   "                        # 字符串拼接值
                                        else:
                                            continue
                                    else:
                                        continue
                                reward_str += u'已经兑换次数：' + str(get_item_num)
                                reward_str += '-----------'

                            reward_lst.append([u'玩家已触发商城事件ID_'+str(shop_even_id),reward_str])
                            # print reward_lst
                    except:
                        completed_dic = {}
                    # ---------------- 玩家已触发购买信息-------------------------------------

                    # ------------------- 汇总 有就加入总表（三层列表 [[[],[]],[[],[]]]）
                    all_immutable_lst = []
                    if uid_lst:
                        all_immutable_lst.append(uid_lst)
                    if reward_end_date_lst:
                        all_immutable_lst.append(reward_end_date_lst)
                    if version_lst:
                        all_immutable_lst.append(version_lst)
                    if reward_lst:
                        all_immutable_lst.append(reward_lst)
                    # -------------------------------------------------------------------------------------------------------------------#

                    # -----------------------------------可改元素-------------------------------------------------------------------------#
                    # {key1:{'name':X,'num':X},key2:{'name':X,'num':X}}

                    # ---------------- 商城所有可购买次数修改-------------------------------------
                    player_completed_dic = source.get('num_dict', {})
                    # 假日商店购买次数
                    for each_eve_id, each_eve_dic in (game_config.get_all_time_limited_shop_config()).items():
                        _each_item_str = ""
                        # 1.已触发的购买事件 修改
                        if int(each_eve_id) in player_completed_dic.keys():     # 玩家已触发商城购买ID事件
                            for _each_key, _each_value in each_eve_dic.items():
                                if _each_value:
                                    if u"idItemGet" == _each_key:  # 物品
                                        _each_item_str += game_config.get_item_config(_each_value)['name']    # 取物品名
                                    elif _each_key in SHOP_BUY_NOT_ITEM_LST:  # 非物品
                                        _each_item_str = SHOP_BUY_NOT_ITEM_LST[_each_key]

                            row_dict[int(each_eve_id)] = {'name': u'假日商店事件__%s__<%s>__<购买次数上限%s>' % (str(each_eve_id), _each_item_str, each_eve_dic.get('leftTimes',-1)), 'num': player_completed_dic[int(each_eve_id)]}
                        # 2.未触发的购买事件 修改
                        else:                                                   # 玩家未触发商城购买ID事件 要显示未触发的所有
                            for _each_key, _each_value in each_eve_dic.items():
                                if _each_value:  # 物品
                                    if u"idItemGet" == _each_key:  # 物品
                                        _each_item_str += game_config.get_item_config(_each_value)['name']    # 取物品名
                                    elif _each_key in SHOP_BUY_NOT_ITEM_LST:  # 非物品
                                        _each_item_str = SHOP_BUY_NOT_ITEM_LST[_each_key]
                            row_dict[int(each_eve_id)] = {'name': u'假日商店事件__%s__<%s>__<购买次数上限%s>' % (str(each_eve_id), _each_item_str, each_eve_dic.get('leftTimes',-1)), 'num': 0}

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
def set_player_activity_time_limited_shop_function(value_dict):
    """
    修改memcache数据

    value_dict['tem_id'] u'2'$$'num_dict'
    value_dict['input_value'] int
    """
    cmem_url = server_define.CMEM_MAP[int(value_dict['server_id'])]
    if cmem_url:
        if len(value_dict['user_id']):
            source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_ACTIVITY_TIME_LIMITED_SHOP_MODEL.format(user_id=value_dict['user_id']))
            # print 'source__', source
            try:
                input_int_val = int(value_dict['input_value'])
                (second_key, first_key) = (value_dict['item_id']).split('$$')        # 要修改的key
                second_key = int(second_key)
                if input_int_val > 0 and second_key > 0:
                    if second_key in source[first_key].keys():
                        source[first_key][second_key] = input_int_val
                    else:
                        source[first_key].update({second_key: input_int_val})
                elif input_int_val == 0 and second_key > 0:
                    if second_key in source[first_key].keys():
                        source[first_key].pop(second_key)
                else:
                    return False
            except:
                return False
            # 传回 url  uid  以及数据 做外层检测
            result = memcache.put_cmem_val(cmem_url, model_define.PLAYER_ACTIVITY_TIME_LIMITED_SHOP_MODEL.format(user_id=value_dict['user_id']), source)
            return result