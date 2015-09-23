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

def get_player_treasure_function(request, player_treasure_edit):
    """
        玩家夺宝数据编辑
        source {
        'grab_msg_lst': [{'id': 100001, 'name': '\xe8\xbd\xbb\xe7\xa6\xbb', 'time': 1435990209.13243}, {'id': 100002, 'name': '400501g', 'time': 1436947184.663864}],
        'last_refresh_time': 1437884014.024381,
        'reset_treasure_date': datetime.date(2015, 7, 26),
        'uid': '1000000950',
        'open_synthesize_set': set([20001, 20004, 20005]),

        'treasure_point': 8,
        'reset_treasure_count': 0,
        'treasure_fragment_dict': {100001: 0, 100002: 1, 100003: 2, 100014: 2, 100015: 1, 83001: 1, 100026: 0, 83003: 1, 100028: 0, 100029: 0, 100030: 0, 100031: 0, 100032: 0, 100033: 0, 100034: 0, 100035: 0, 100036: 0, 100037: 2, 100038: 0, 100039: 2, 100040: 0, 100041: 0, 100042: 1, 100043: 0, 100044: 0, 100045: 0, 100046: 0, 100047: 0, 100048: 0, 100025: 0, 100027: 0}}
    """
    # 以函数的指针方式传递函数并调用
    function_name = 'data_edit.player_treasure.{function}'.format(function=set_player_treasure_function.__name__)
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
                    source = memcache.get_cmem_val(cmem_url, model_define.TREASURE_MODEL.format(user_id=user_uid))
                elif len(user_name):
                    name = hashlib.md5(user_name).hexdigest().upper()
                    key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                    user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    return_name = user_name
                    source = memcache.get_cmem_val(cmem_url, model_define.TREASURE_MODEL.format(user_id=user_uid))
                elif len(user_openid):
                    result = memcache.get_cmem_val(cmem_url, model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    user_uid = result['uid']
                    return_openid = user_openid
                    source = memcache.get_cmem_val(cmem_url, model_define.TREASURE_MODEL.format(user_id=user_uid))
                if source:
                    # print 'source', source
                    row_dict = collections.OrderedDict()  # 有序字典
                    treasure_lst = []
                    # -----------------------------------不可改元素---------------------------------------------------------------#
                    # [[[0,1],[0,1]],[[0,1],[0,1]]] 三层[]
                    # ------------------------用户UID
                    uid = source.get('uid', 'None')
                    if uid != 'None':
                        uid_lst = [[u'用户UID', uid]]
                    else:
                        uid_lst = []
                    # ----------------- 已合成宝石 注：没有数目
                    open_synthesize_set = source.get('open_synthesize_set', [])
                    for treasure_id in open_synthesize_set:
                        treasure_lst.append(game_config.get_item_config(treasure_id)['name'])
                    treasure_lst = [[u'已合成宝石', u' '.join(treasure_lst)]]
                    # ------------------重置夺宝时间
                    try:
                        reset_treasure_date = source['reset_treasure_date'].strftime('%Y-%m-%d')   # 重置夺宝时间
                        reset_treasure_date_lst = [[u'重置夺宝时间', reset_treasure_date]]
                    except:
                        reset_treasure_date_lst = []
                    # ------------------最后刷新时间
                    try:
                        last_refresh_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(source['last_refresh_time']))  # 最后刷新时间
                        last_refresh_time_lst = [[u'最后刷新时间', last_refresh_time]]
                    except:
                        last_refresh_time_lst = []

                    # ---------------- 被抢夺信息
                    try:
                        grab_msg_lst = source.get('grab_msg_lst', [])   # 被抢夺信息 [{'id':x,name:'','time':3}{}]
                        _tmp_grab_lst = []
                        num = 0
                        for each_msg_dict in grab_msg_lst:
                            num += 1
                            # 字符串拼接 例如：“在时间：2015-07-04 14:10:09 被玩家：轻离 掠夺物品：100001一个”
                            _tmp_grab_lst.append([u'被抢夺信息0'+str(num), '在时间：'+str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(each_msg_dict['time'])))+' 被玩家：'+each_msg_dict['name']+' 掠夺物品：'+str(each_msg_dict['id']) + '一个'])
                        new_grab_msg_lst = [_tmp_grab_lst]
                    except:
                        new_grab_msg_lst = []
                    # ------------------- 汇总 有就加入总表（三层列表 [[[],[]],[[],[]]]）
                    all_immutable_lst = []
                    if uid_lst:
                        all_immutable_lst.append(uid_lst)
                    if treasure_lst:
                        all_immutable_lst.append(treasure_lst)
                    if reset_treasure_date_lst:
                        all_immutable_lst.append(reset_treasure_date_lst)
                    if last_refresh_time_lst:
                        all_immutable_lst.append(last_refresh_time_lst)
                    if new_grab_msg_lst:
                        all_immutable_lst.extend(new_grab_msg_lst)

                    # -------------------------------------------------------------------------------------------------------------------#
                    # -----------------------------------可改元素-------------------------------------------------------------------------#
                    # {key1:{'name':X,'num':X},key2:{'name':X,'num':X}}
                    treasure_point = source.get('treasure_point', 0)  # 夺宝次数
                    reset_treasure_count = source.get('reset_treasure_count', 0)  # 夺宝刷新次数
                    # 宝石碎片id + num
                    treasure_fragment_dict = source.get('treasure_fragment_dict', {})  # 夺宝宝石碎片字典 暂时没有物品名字列表 TODO 加上宝石碎片物品列表
                    if treasure_fragment_dict:
                        for treasure_debris_id, _value in treasure_fragment_dict.items():
                            row_dict[treasure_debris_id] = {'name': '宝石碎片_' + str(treasure_debris_id), 'num': _value}
                    # 夺宝剩余次数
                    row_dict['treasure_point'] = {'name': u'夺宝剩余次数', 'num': treasure_point}
                    # 夺宝刷新次数
                    row_dict['reset_treasure_count'] = {'name': u'夺宝刷新次数', 'num': reset_treasure_count}
                    # -----------------------------------------------------------------------------------------------------------------------#
                else:
                    if user_uid:
                        return_uid = user_uid
                        if user_openid:
                            return_openid = user_openid
                        if user_name:
                            return_name = user_name

                return render_to_response(player_treasure_edit, locals(), RequestContext(request))

            except UnboundLocalError:
                type_hidden = 'hidden'
                return render_to_response(player_treasure_edit, locals(), RequestContext(request))

            except TypeError:
                type_hidden = 'hidden'
                return render_to_response(player_treasure_edit, locals(), RequestContext(request))

    else:
        row_list = []
        type_hidden = 'hidden'
        return render_to_response(player_treasure_edit, locals(), RequestContext(request))


# @require_permission
def set_player_treasure_function(value_dict):
    """
    修改memcache数据

    value_dict['tem_id'] 100001 or 'treasure_point' or  'reset_treasure_count'
    """
    cmem_url = server_define.CMEM_MAP[int(value_dict['server_id'])]
    if cmem_url:
        if len(value_dict['user_id']):
            source = memcache.get_cmem_val(cmem_url, model_define.TREASURE_MODEL.format(user_id=value_dict['user_id']))
            try:
                treasure_debris_id = int(value_dict['item_id'])
                if int(value_dict['input_value']) >= 0:
                    source['treasure_fragment_dict'][treasure_debris_id] = int(value_dict['input_value'])
                else:
                    return False
            except:
                try:
                    key = str(value_dict['item_id'])
                    if isinstance(source[key], int):
                        if int(value_dict['input_value']) >= 0:
                            source[key] = int(value_dict['input_value'])
                    else:
                        return False
                except:
                    return False
            # 传回 url  uid  以及数据 做外层检测
            result = memcache.put_cmem_val(cmem_url, model_define.TREASURE_MODEL.format(user_id=value_dict['user_id']), source)
            return result