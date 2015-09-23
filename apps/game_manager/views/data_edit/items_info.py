# -*- coding:utf-8 -*-

import datetime
import collections
import hashlib
import collections
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
from apps.logs.output_action_gm import *


@require_permission
def index(request, template):
    """  类型看格式
    {'data_version': '3',
    'uid': '1000105733',
    #循环取出物品中文名字在前台显示。
    'items': {
    81025: 2,
    80008: 21,
    80009: 31,
    80010: 4,
    80011: 2,
    80012: 1,
    80013: 1,
    80014: 0,
    80015: 0,
    81056: 13,
    80302: 198,
    80303: 1087,
    80048: 125,
    80306: 297,
    81086: 16,
    81098: 10,
    82006: 11,
    82007: 20,
    82008: 20,
    81113: 9,
    80101: 3,
    80102: 5,
    80103: 0,
    81010: 11
    }}
    """
    item_lst = collections.OrderedDict()
    item_dict_name, item_lst_type = game_config.get_item_config_with_id_name()
    add_item_function = 'data_edit.items_info.{function}'.format(function=add_item.__name__)
    function_name = 'data_edit.items_info.{function}'.format(function=set_memcache.__name__)
    del_item_function = 'data_edit.items_info.{function}'.format(function=del_item.__name__)
    server_list, platform_list = daily_log._get_server_list(None, None)
    server_list.remove(server_list[0])
    if request.method == 'POST':
        user_uid = request.POST.get('user_uid')
        user_name = request.POST.get('user_name').encode('utf-8')
        user_openid = request.POST.get('user_openid')
        server_id = int(request.POST.get('server_id'))
        cmem_url = server_define.CMEM_MAP[int(server_id)]

        if cmem_url:
            try:
                if len(user_uid):
                    source = memcache.get_cmem_val(cmem_url, model_define.ITEM_MODEL.format(user_id=user_uid))
                elif len(user_name):
                    name = hashlib.md5(user_name).hexdigest().upper()
                    key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                    user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    source = memcache.get_cmem_val(cmem_url, model_define.ITEM_MODEL.format(user_id=user_uid))
                elif len(user_openid):
                    result = memcache.get_cmem_val(cmem_url,
                                                   model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.ITEM_MODEL.format(user_id=result['uid']))
                    user_uid = user_id = result['uid']
                row_dict = collections.OrderedDict()

                for _key, _value in source['items'].items():
                    row_dict[_key] = {'name': game_config.get_item_config(_key)['name'],
                                      'num': _value}

                return render_to_response(template, locals(), RequestContext(request))

            except UnicodeEncodeError:
                return render_to_response(template, locals(), RequestContext(request))

            except TypeError:
                return render_to_response(template, locals(), RequestContext(request))
            except UnboundLocalError:
                return render_to_response(template, locals(), RequestContext(request))
    else:
        row_list = []

    return render_to_response(template, locals(), RequestContext(request))


def set_memcache(value_dict):
    '''
    修改memcache数据
    '''
    cmem_url = server_define.CMEM_MAP[int(value_dict['server_id'])]
    if cmem_url:
        if len(value_dict['user_id']):
            if int(value_dict['input_value']) < 0:
                return False
            source = memcache.get_cmem_val(cmem_url, model_define.ITEM_MODEL.format(user_id=value_dict['user_id']))
            old_value = source['items'][int(value_dict['item_id'])]
            source['items'][int(value_dict['item_id'])] = int(value_dict['input_value'])
            result = memcache.put_cmem_val(cmem_url, model_define.ITEM_MODEL.format(user_id=value_dict['user_id']),
                                           source)
            # 操作日志记录
            insert_action_change_item(value_dict['manager'], str(value_dict['server_id']), str(value_dict['user_id']), value_dict['item_id'], old_value, value_dict['input_value'])

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
            source = memcache.get_cmem_val(cmem_url, model_define.ITEM_MODEL.format(user_id=user_id))
            if item_tid in source['items']:
                return False
            else:
                source['items'][item_tid] = 0
                result = memcache.put_cmem_val(cmem_url, model_define.ITEM_MODEL.format(user_id=user_id),source)
                # 操作日志记录
                insert_action_add_item(value_dict['manager'], str(server_id), str(user_id), item_tid, 0)

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
        if user_id and item_tid:
            source = memcache.get_cmem_val(cmem_url, model_define.ITEM_MODEL.format(user_id=user_id))
            if item_tid in source['items']:
                print item_tid
                del_num = source['items'][item_tid]
                source['items'].pop(item_tid)
                result = memcache.put_cmem_val(cmem_url, model_define.ITEM_MODEL.format(user_id=user_id),source)
                # 操作日志记录
                insert_action_delete_item(value_dict['manager'], str(server_id), str(user_id), item_tid, del_num)
                return result
            else:
                return False