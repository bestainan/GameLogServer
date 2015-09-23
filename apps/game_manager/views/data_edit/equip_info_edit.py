# -*- coding:utf-8 -*-
"""
    总体思路：
        跳转过程： 3个html 与 1个python文件(④个函数)

                            /—————change_equip()函数—————change_equip.html——————index()函数的2.
    从equip_info_edithtml页面——————add_equip()函数   —————change_equip.html——————index()函数的4.
                            \—————delete_equip()函数—————delete_equip.html——————index()函数的3.
"""

# import sys
import collections
import hashlib
from django.template import RequestContext

from apps.game_manager.views.log import daily_log
from django.shortcuts import render_to_response
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define, game_define
# from apps.common.decorators.decorators import require_permission
from apps.config import game_config
from apps.game_manager.models.game_manager import GameManager
from apps.logs.output_action_gm import *


# @require_permission
def index(request, equip_info_edit):
    """
        ①
        玩家装备数据
        此函数功能：1.显示最新数据 2.修改装备 3.删除装备 4.添加装备
    """
    # 获取当前管理员
    # 1.公用代码部分 即每次修改 删除 添加 数据后 显示最新数据
    manager = GameManager.get_by_request(request)
    server_list, platform_list = daily_log._get_server_list(None, None)
    server_list.remove(server_list[0])
    if request.method == 'POST':

        user_uid = request.POST.get("user_uid")
        user_name = request.POST.get("user_name")
        user_openid = request.POST.get("user_openid")
        server_id = int(request.POST.get("server_id"))

        type_hidden = 'visible'
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        if cmem_url:
            print 'cmem_url', cmem_url
            try:
                source = {}
                if len(user_uid):
                    source = memcache.get_cmem_val(cmem_url, model_define.EQUIP_MODEL.format(user_id=user_uid))
                    # print source
                elif len(user_name):
                    name = hashlib.md5(user_name.encode('utf-8')).hexdigest().upper()
                    key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                    user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    source = memcache.get_cmem_val(cmem_url, model_define.EQUIP_MODEL.format(user_id=user_uid))
                    # print source
                elif len(user_openid):
                    result = memcache.get_cmem_val(cmem_url,model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    user_uid = result['uid']
                    source = memcache.get_cmem_val(cmem_url, model_define.EQUIP_MODEL.format(user_id=user_uid))
                    # print source
                if source:
                    """以上是公用部分，以下是修改 删除 添加"""
                    # 2.修改装备
                    try:
                        old_edit_data = eval(request.POST.get("old_edit_data"))
                        old_edit_data.pop('name')                                       # 得到编辑的源数据
                        will_edit_tid = request.POST.get("will_edit_tid")               # 要改成装备tid
                        will_edit_tid_level = request.POST.get("will_edit_tid_level")   # 要改的装备的等级
                        result = edit_function(cmem_url, source, old_edit_data, int(will_edit_tid), int(will_edit_tid_level))
                        if result:
                            # 操作日志记录
                            insert_action_change_equip(manager, str(server_id), str(source['uid']), old_edit_data['uid'], old_edit_data['tid'], will_edit_tid, old_edit_data['level'], will_edit_tid_level)
                    except:
                        # 不是编辑 或 数据不对 跳过
                        pass

                    # 3.删除装备 删除比较简单不单写函数
                    try:
                        delete_data = eval(request.POST.get('delete_data'))
                        delete_data.pop('name')
                        if delete_data:
                            # 操作日志记录
                            insert_action_delete_equip(manager, str(server_id), str(user_uid), delete_data['uid'], delete_data['tid'], delete_data['level'])

                            source['equips'].remove(delete_data)
                            result = memcache.put_cmem_val(cmem_url, model_define.EQUIP_MODEL.format(user_id=int(user_uid)), source)
                    except:
                        # 不是删除 或 数据不对 跳过
                        pass

                    # 4.添加装备 添加比较简单不单写函数
                    try:
                        add_data = eval(request.POST.get('add_data'))
                        if add_data:
                            will_edit_tid = request.POST.get("will_edit_tid")
                            will_edit_tid_level = request.POST.get("will_edit_tid_level")
                            if will_edit_tid and will_edit_tid_level:
                                equip_config = game_config.get_equipment_config(int(will_edit_tid))
                                source['equips'].append({
                                    'uid': int(add_data),
                                    'tid': int(will_edit_tid),
                                    'level': int(will_edit_tid_level),
                                    'type': int(equip_config['type'])
                                    })
                                # 下个装备序列计数加1
                                source['seq_id'] = int(add_data) + 1
                                result = memcache.put_cmem_val(cmem_url,model_define.EQUIP_MODEL.format(user_id=int(user_uid)), source)
                                # 操作日志记录
                                insert_action_add_equip(manager, str(server_id), str(user_uid), add_data, will_edit_tid, will_edit_tid_level)
                                print "Finish"
                    except:
                        # 不是添加 或 数据不对 跳过
                        pass

                """以下是公用部分，以上是修改 删除 添加"""
                if source:
                    row_list = source['equips']
                    for each_value in row_list:
                        equip_config = game_config.get_item_config(each_value['tid'])
                        each_value['name'] = equip_config['name']

                return render_to_response(equip_info_edit, locals(), RequestContext(request))
            except UnboundLocalError:
                type_hidden = 'hidden'
                return render_to_response(equip_info_edit, locals(), RequestContext(request))
            except TypeError:
                type_hidden = 'hidden'
                return render_to_response(equip_info_edit, locals(), RequestContext(request))

    else:
        row_list = []
        type_hidden = 'hidden'
        row_dict = {}
        return render_to_response(equip_info_edit, locals(), RequestContext(request))


# @require_permission
def change_equip_to_html(request,equip_edit):
    """
        ②
        编辑装备信息
    """
    if request.method == 'POST':
        user_openid = request.POST.get("user_openid")
        server_id = request.POST.get("server_id")
        user_uid = request.POST.get("user_uid")
        user_name = request.POST.get("user_name")
        edit_data = eval(request.POST.get("edit_data"))
        will_edit_tid_level = edit_data['level']
        will_edit_tid = int(edit_data['tid'])
        old_edit_data = edit_data
        server_list, platform_list = daily_log._get_server_list(None, None)
        server_list.remove(server_list[0])

        item_id_name, item_id_type = game_config.get_item_config_with_id_name()
        monster_id_name = game_config.get_monster_config_with_id_name()
        item_tid_name_lst = []
        for (tid, name) in item_id_name.items():
            item_type = item_id_type[tid]
            if item_type == game_define.ITEM_TYPE_EQUIP:
                content = dict()
                content['tid'] = tid
                content['name'] = name
                item_tid_name_lst.append(content)

    return render_to_response(equip_edit,locals(),RequestContext(request))


# @require_permission
def delete_equip_to_html(request, equip_del):
    """
        ☂ (3)
        删除装备
    """
    if request.method == 'POST':
        user_openid = request.POST.get("user_openid")
        server_id = request.POST.get("server_id")
        user_uid = request.POST.get("user_uid")
        user_name = request.POST.get("user_name")
        edit_data = eval(request.POST.get("edit_data"))
        delete_data = edit_data
        server_list, platform_list = daily_log._get_server_list(None, None)
        server_list.remove(server_list[0])
        cmem_url = server_define.CMEM_MAP[int(server_id)]

        return render_to_response(equip_del,locals(),RequestContext(request))


def add_equip_to_html(request,equip_add):
    """
        ④
        添加装备
    """
    if request.method == 'POST':
        user_openid = request.POST.get("user_openid")
        server_id = request.POST.get("server_id")
        user_uid = request.POST.get("user_uid")
        user_name = request.POST.get("user_name")
        edit_data = eval(request.POST.get("edit_data"))
        will_edit_tid_level = edit_data['level']
        will_edit_tid = int(edit_data['tid'])
        server_list, platform_list = daily_log._get_server_list(None, None)
        server_list.remove(server_list[0])

        item_id_name, item_id_type = game_config.get_item_config_with_id_name()
        monster_id_name = game_config.get_monster_config_with_id_name()
        item_tid_name_lst = []
        for (tid, name) in item_id_name.items():
            item_type = item_id_type[tid]
            if item_type == game_define.ITEM_TYPE_EQUIP:
                content = dict()
                content['tid'] = tid
                content['name'] = name
                item_tid_name_lst.append(content)
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        source = memcache.get_cmem_val(cmem_url, model_define.EQUIP_MODEL.format(user_id=int(user_uid)))
        add_data = source['seq_id']
        return render_to_response(equip_add,locals(),RequestContext(request))


# 修改数据
def edit_function(_cmem_url, _source, _will_edit_data, _will_edit_tid, _will_edit_tid_level,):
    try:
        # 如果有数据 求要修改数据的下标 修改数据
        if _cmem_url and _source and _will_edit_data and _will_edit_tid and _will_edit_tid_level:
            equip_data = _source['equips']
            # 求list下标
            index = equip_data.index(_will_edit_data)
            # 修改装备tid
            equip_data[index]['tid'] = _will_edit_tid
            # 修改等级
            equip_data[index]['level'] = _will_edit_tid_level
            # 修改装备类型
            equip_config = game_config.get_equipment_config(int(_will_edit_tid))
            equip_data[index]['type'] = equip_config['type']
            # 外层检测 返回TRUE FALSE
            result = memcache.put_cmem_val(_cmem_url, model_define.EQUIP_MODEL.format(user_id=int(_source['uid'])), _source)
            return result
        else:
            return False
    except:
        return False