# -*- coding:utf-8 -*-

import datetime
import collections
import hashlib
import json
from django.http import HttpResponse
from django.template import RequestContext
from apps.game_manager.views.log import daily_log
from django.shortcuts import render_to_response
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define
from apps.common.decorators.decorators import require_permission
from apps.config import game_config


@require_permission
def index(request, template):
    """  玩家宝物
    author ： 全勇男
    {'treasure_items': [
    {'tid': 20006, 'phase': 1, 'level': 43, 'uid': 4, 'level_exp': 1000},
    {'tid': 20005, 'phase': 0, 'level_exp': 0, 'uid': 15, 'level': 1},
    {'tid': 20001, 'phase': 0, 'level': 20, 'uid': 24, 'level_exp': 30400},
    {'tid': 20007, 'phase': 0, 'level': 1, 'uid': 46, 'level_exp': 0},
    {'tid': 20008, 'phase': 0, 'level_exp': 0, 'uid': 47, 'level': 1},
    {'tid': 20004, 'phase': 0, 'level': 1, 'uid': 50, 'level_exp': 0},
    {'tid': 20001, 'phase': 0, 'level': 1, 'uid': 52, 'level_exp': 0}],
    'uid': '1000000950', 'seq': 53}
    """
    add_item_function = 'data_edit.treasure_item_model.{function}'.format(function=add_item.__name__)
    function_name = 'data_edit.treasure_item_model.{function}'.format(function=set_memcache.__name__)
    del_item_function = 'data_edit.treasure_item_model.{function}'.format(function=del_item.__name__)
    server_list, platform_list = daily_log._get_server_list(None, None)
    server_list.remove(server_list[0])
    item_dict_name, item_lst_type = game_config.get_item_config_with_id_name()
    item_dict_name = { key:value for key, value in item_dict_name.items() if item_lst_type[key] == 6}

    if request.method == 'POST':
        user_uid = request.POST.get('user_uid')
        user_name = request.POST.get('user_name').encode('utf-8')
        user_openid = request.POST.get('user_openid')
        server_id = int(request.POST.get('server_id'))
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        try:
            if cmem_url:
                if len(user_uid):
                    source = memcache.get_cmem_val(cmem_url, model_define.TREASURE_ITEM_MODEL.format(user_id=user_uid))

                elif len(user_name):
                    name = hashlib.md5(user_name).hexdigest().upper()
                    key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                    user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    source = memcache.get_cmem_val(cmem_url, model_define.TREASURE_ITEM_MODEL.format(user_id=user_uid))
                elif len(user_openid):
                    result = memcache.get_cmem_val(cmem_url,
                                                   model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.TREASURE_ITEM_MODEL.format(user_id=result['uid']))
                    user_uid = user_id = result['uid']
                user_uid = source['uid']
                item_lst = source['treasure_items']

                return render_to_response(template, locals(), RequestContext(request))

        except UnicodeEncodeError:
            return render_to_response(template, locals(), RequestContext(request))

        except TypeError:
            return render_to_response(template, locals(), RequestContext(request))

        except UnboundLocalError:
            return render_to_response(template, locals(), RequestContext(request))

    else:
        row_dict = {}
        return render_to_response(template, locals(), RequestContext(request))



def set_memcache(value_dict):
    '''
    修改memcache数据
    '''
    cmem_url = server_define.CMEM_MAP[int(value_dict['server_id'])]
    if cmem_url:
        if len(value_dict['user_id']):
            if  0 > int(value_dict['input_value']) > 60800:
                return False
            source = memcache.get_cmem_val(cmem_url, model_define.TREASURE_ITEM_MODEL.format(user_id=value_dict['user_id']))
            for _dict in source['treasure_items']:
                if _dict['uid'] == int(value_dict['item_id']):
                    _dict['level_exp'] = int(value_dict['input_value'])
            result = memcache.put_cmem_val(cmem_url, model_define.TREASURE_ITEM_MODEL.format(user_id=value_dict['user_id']),
                                           source)
            return result


def add_item(value_dict):
    '''
    增加物品push memcache

    '''
    user_id = int(value_dict['user_id'])
    item_tid = int(value_dict['item_id'])
    server_id = int(value_dict['server_id'])
    cmem_url = server_define.CMEM_MAP[server_id]

    if cmem_url:
        if user_id:
            source = memcache.get_cmem_val(cmem_url, model_define.TREASURE_ITEM_MODEL.format(user_id=user_id))
            for _dict in source['treasure_items']:
                if item_tid == _dict['tid']:
                    print ' same'
                    return False
            print source
            source['treasure_items'].append(
                {'tid': item_tid,
                 'phase': 0,
                 'level': 1,
                 'uid': source['seq'],
                 'level_exp': 0}
            )
            source['seq'] += 1
            result = memcache.put_cmem_val(cmem_url, model_define.TREASURE_ITEM_MODEL.format(user_id=user_id),source)
            return result


def del_item(value_dict):
    '''
    删除物品
    '''
    user_id = int(value_dict['user_id'])
    item_tid = int(value_dict['item_id'])
    server_id = int(value_dict['server_id'])
    cmem_url = server_define.CMEM_MAP[server_id]
    if cmem_url:
        source = memcache.get_cmem_val(cmem_url, model_define.TREASURE_ITEM_MODEL.format(user_id=user_id))
        for _dict in source['treasure_items']:
            if item_tid == _dict['uid']:
                source['treasure_items'].remove(_dict)
        result = memcache.put_cmem_val(cmem_url, model_define.TREASURE_ITEM_MODEL.format(user_id=user_id),source)
        return result
    else:
        return False