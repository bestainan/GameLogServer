# -*- coding:utf-8 -*-

import collections
import datetime
import hashlib
from django.template import RequestContext
from apps.game_manager.views.log import daily_log
from django.shortcuts import render_to_response
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define
from apps.config import game_config


def get_player_catch_monster_function(request, player_catch_monster_edit):
    """
        玩家抓宠副本编辑
        source
        {'catch_monster_stage_id_lst': [40501, 40801, 40802],
         'catch_monster_stage_lst': [1, 6, 1],
          'last_refresh_date': datetime.date(2015, 7, 25),
           'uid': '1000101754'
            }
    """
    # 以函数的指针方式传递函数并调用
    function_name = 'data_edit.player_catch_monster.{function}'.format(function=set_player_catch_monster_function.__name__)
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
            {'name': u'副本名称'},
            {'name': u'攻打次数'},
        ]
        if cmem_url:
            try:
                source = dict()
                if len(user_uid):
                    source = memcache.get_cmem_val(cmem_url, model_define.CATCH_MONSTER_MODEL.format(user_id=user_uid))
                elif len(user_name):
                    name = hashlib.md5(user_name).hexdigest().upper()
                    key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                    user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    return_name = user_name
                    source = memcache.get_cmem_val(cmem_url, model_define.CATCH_MONSTER_MODEL.format(user_id=user_uid))
                elif len(user_openid):
                    result = memcache.get_cmem_val(cmem_url, model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    user_uid = result['uid']
                    return_openid = user_openid
                    source = memcache.get_cmem_val(cmem_url, model_define.CATCH_MONSTER_MODEL.format(user_id=user_uid))
                if source:
                    # print 'source', source

                    row_dict = collections.OrderedDict()  # 有序字典
                    return_uid = user_uid
                    last_refresh_date = source.get('last_refresh_date', datetime.date(0001, 01, 01)).strftime('%Y-%m-%d')
                    for stage_id, stage_count in zip(source['catch_monster_stage_id_lst'], source['catch_monster_stage_lst']):
                        stage_config = game_config.get_stages_config(int(stage_id))
                        try:
                            row_dict[stage_id] = {'name': stage_config['stageInfo'] + '_' + str(stage_config['id']),
                                                  'num': stage_count,
                                                  }
                        except:
                            print stage_id, stage_count
                else:
                    # 数据为空 返回空表
                    if user_uid:
                        return_uid = user_uid
                    else:
                        user_uid = "None"
                    last_refresh_date = 'None'
                    row_dict = {'name': 'None', 'num': 'None'}
                # print row_dict
                return render_to_response(player_catch_monster_edit, locals(), RequestContext(request))

            except UnboundLocalError:
                type_hidden = 'hidden'
                return render_to_response(player_catch_monster_edit, locals(), RequestContext(request))

            except TypeError:
                type_hidden = 'hidden'
                return render_to_response(player_catch_monster_edit, locals(), RequestContext(request))

    else:
        row_list = []
        type_hidden = 'hidden'
        return render_to_response(player_catch_monster_edit, locals(), RequestContext(request))


# @require_permission
def set_player_catch_monster_function(value_dict):
    """
    修改memcache数据

    tem_id 40801 value_dict['input_value'] num
    """
    cmem_url = server_define.CMEM_MAP[int(value_dict['server_id'])]
    if cmem_url:
        if len(value_dict['user_id']):
            source = memcache.get_cmem_val(cmem_url, model_define.CATCH_MONSTER_MODEL.format(user_id=value_dict['user_id']))
            try:
                stage_id = int(value_dict['item_id'])
                input_value = int(value_dict['input_value'])
                print stage_id, input_value

                if 0 <= input_value:
                    index_id = source['catch_monster_stage_id_lst'].index(stage_id)
                    source['catch_monster_stage_lst'][index_id] = input_value
                else:
                    return False
            except:
                return False
            # 传回 url  uid  以及数据 做外层检测
            result = memcache.put_cmem_val(cmem_url, model_define.CATCH_MONSTER_MODEL.format(user_id=value_dict['user_id']), source)
            return result