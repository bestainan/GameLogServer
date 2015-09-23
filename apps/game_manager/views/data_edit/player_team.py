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


# templates == player_team.html
def get_player_team_function(request, templates):
    """
        玩家队伍数据编辑
        source {
        'team_equips': [[182, 94, 1430, 524, 1723], [190, 1344, 1353, 370, 488], [114, 1716, 1715, 461, 489], [113, 1343, 1352, 193, 487], [497, 1342, 1354, 523, 0]],
        'team_treasure_2': [[52, 4], [0, 50], [0, 0], [0, 0], [24, 0]],
        'team_monsters': [6536, 448, 0, 0, 7747],
        'active_band_id_lst': [],
        'uid': '1000000950'
        }
    """
    # 以函数的指针方式传递函数并调用
    function_name = 'data_edit.player_team.{function}'.format(function=set_player_team_function.__name__)
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
            {'name': u'队伍位置'},
            {'name': u'宠物'},
            {'name': u'装备1'},
            {'name': u'装备2'},
            {'name': u'装备3'},
            {'name': u'装备4'},
            {'name': u'装备5'},
            {'name': u'宝石1'},
            {'name': u'宝石2'},
        ]
        if cmem_url:
            try:
                source = dict()
                if len(user_uid):
                    source = memcache.get_cmem_val(cmem_url, model_define.TEAM_MODEL.format(user_id=user_uid))
                elif len(user_name):
                    name = hashlib.md5(user_name).hexdigest().upper()
                    key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                    user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    return_name = user_name
                    source = memcache.get_cmem_val(cmem_url, model_define.TEAM_MODEL.format(user_id=user_uid))
                elif len(user_openid):
                    result = memcache.get_cmem_val(cmem_url, model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    user_uid = result['uid']
                    return_openid = user_openid
                    source = memcache.get_cmem_val(cmem_url, model_define.TEAM_MODEL.format(user_id=user_uid))
                if source:
                    print 'source', source
                    row_dict = collections.OrderedDict()  # 有序字典
                    # -----------------------------------可改元素-------------------------------------------------------------------------#
                    # 只修改队伍装备 队伍宝石 宠物
                    # 队伍位置信息 五个位置
                    for i in xrange(5):
                        try:
                            row_dict[i] = {'name': u'队伍位置' + '_' + str(i + 1),                         # 位置i
                                                  'monsters': source['team_monsters'][i],                 # 宠物i
                                                  'equips_1': source['team_equips'][i][0],                # 装备1
                                                  'equips_2': source['team_equips'][i][1],                # 装备2
                                                  'equips_3': source['team_equips'][i][2],                # 装备3
                                                  'equips_4': source['team_equips'][i][3],                # 装备4
                                                  'equips_5': source['team_equips'][i][4],                # 装备5
                                                  'treasures_1': source['team_treasure_2'][i][0],         # 宝石1
                                                  'treasures_2': source['team_treasure_2'][i][1],         # 宝石2
                                          }
                        except:
                            print i

                    # 取玩家现有宠物表 装备表 宝石表
                    # ------------宠物表
                    # monsters_id_name_dict = {}
                    # monsters_source = memcache.get_cmem_val(cmem_url, model_define.MONSTER_MODEL.format(user_id=user_uid))
                    # print 'monsters_source', monsters_source

                    # ------------装备表
                    equips_id_name_dict = {}
                    equips_source = memcache.get_cmem_val(cmem_url, model_define.EQUIP_MODEL.format(user_id=user_uid))
                    # print 'equips_source_start', equips_source, 'equips_source_end'
                    # diec = collections.OrderedDict()
                    # for each_euqip_dict in equips_source['equips']:
                    #         diec[each_euqip_dict['uid']] = {
                    #             each_euqip_dict['tid'],
                    #             each_euqip_dict['type'],
                    #
                    #         }
                    # print diec

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
def set_player_team_function(value_dict):
    """
    修改memcache数据
                        key2$$key1$$key3(>=0才有)
    value_dict['tem_id'] 0$$team_monsters$$None
    value_dict['tem_id'] 0$$team_equips$$0
    value_dict['input_value'] int
    """
    print "PWPIASD"
    cmem_url = server_define.CMEM_MAP[int(value_dict['server_id'])]
    if cmem_url:
        if len(value_dict['user_id']):
            source = memcache.get_cmem_val(cmem_url, model_define.TEAM_MODEL.format(user_id=value_dict['user_id']))

            try:
                (second_key, first_key, three_key) = value_dict['item_id'].split('$$')
                input_value = int(value_dict['input_value'])
                print first_key, second_key, three_key, input_value, "A"
                first_key, second_key, three_key = str(first_key), int(second_key), int(three_key)
                print first_key, second_key, three_key, input_value, "B"
                print "PWPIASD111114"
                if 0 <= second_key and 0 <= input_value:
                    if 0 <= three_key:                                      # 装备宝石 二维数组
                        if input_value not in source[first_key][second_key] and 0 < input_value:    # 重复UID检测
                            print "PWPIASD111116"
                            source[first_key][second_key][three_key] = input_value
                            print "PWPIASD111117"
                        elif 0 == input_value:
                            source[first_key][second_key][three_key] = input_value
                        else:
                            print 'repetition'
                            return False
                    else:                                                   # 宠物 一维数组
                        """注：宠物tid uid 都不能重复"""
                        if input_value not in source[first_key] and 0 < input_value:            # 重复 UID 检测
                            print "PWPIASD11111511"
                    #     if three_key <= 0:
                            source[first_key][second_key] = input_value
                            print "PWPIASD111115"
                        elif 0 == input_value:
                            source[first_key][second_key] = input_value
                        else:
                            print 'repetition'
                            return False
                else:
                        print "PWPIASD111113"
                        return False
                print "PWPIASD111111"

            except:
                print "PWPIASD111112"
                return False
            # 传回 url  uid  以及数据 做外层检测
            result = memcache.put_cmem_val(cmem_url, model_define.TEAM_MODEL.format(user_id=value_dict['user_id']), source)
            return result