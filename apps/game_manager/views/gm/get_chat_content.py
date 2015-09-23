# -*- coding:utf-8 -*-

import pickle
from apps.game_manager.models.game_manager import *
from apps.utils.encryption import decrypt
from apps.game_manager.util import memcache
from apps.utils import server_define
from apps.utils import model_define
from apps.game_manager.mysql import server_list
from django.http import HttpResponseRedirect
from django.template import RequestContext
from apps.utils.game_define import USER_STATE_FREEZE
from apps.common.decorators.decorators import require_permission

@require_permission
def get_chat_content(request):
    """
    聊天信息统计
    """

    head_lst = [
        {'width': 70, 'name': u'日期'},
        {'width': 50, 'name': u'UID'},
        {'width': 55, 'name': u'昵称'},
        {'width': 50, 'name': u'等级'},
        {'width': 50, 'name': u'VIP等级'},
        {'width': 50, 'name': u'聊天内容'},
        {'width': 50, 'name': u'服务器ID'},
        {'width': 50, 'name': u'封禁'},
    ]
    server_list_dat = server_list.get_server_list_dat()
    if request.method == 'POST':
        server_id = request.POST.get('server_id')
        row_lst = _get_chat_content(server_id)
        for i in range(len(row_lst)):
            row_lst[i-1].append(server_id)
        return render_to_response("gm/get_chat_content.html",
                                  {'row_lst': row_lst,
                                   'head_lst': head_lst, 'server_list': server_list_dat,'cur_server_id':server_id}, RequestContext(request))
    else:
        return render_to_response("gm/get_chat_content.html",
                                  {'row_lst': [],
                                   'head_lst': head_lst, 'server_list': server_list_dat}, RequestContext(request))


@require_permission
def get_union_chat_content(request):
    head_lst = [
        {'width': 70, 'name': u'日期'},
        {'width': 50, 'name': u'联盟ID'},
        {'width': 50, 'name': u'联盟名称'},
        {'width': 50, 'name': u'UID'},
        {'width': 55, 'name': u'昵称'},
        {'width': 50, 'name': u'等级'},
        {'width': 50, 'name': u'VIP等级'},
        {'width': 50, 'name': u'聊天内容'},
        {'width': 50, 'name': u'服务器ID'},
    ]
    server_list_dat = server_list.get_server_list_dat()

    if request.method == 'POST':
        server_id = request.POST.get('server_id')
        union_id=request.POST.get('union_id')
        if union_id == '':
            union_id=request.POST.get('union_name')
        union_name_list=_get_union_name(server_list_dat)
        row_lst=_get_union_chat_content(server_id,union_id,server_list_dat)
        return render_to_response("gm/get_union_chat_content.html",
                                  {'row_lst': row_lst,
                                   'head_lst': head_lst, 'server_list': server_list_dat,'cur_server_id':server_id,'union_name_list':union_name_list,}, RequestContext(request))
    else:
        union_name_list=_get_union_name(server_list_dat)
        return render_to_response("gm/get_union_chat_content.html",
                                  {'row_lst': [],
                                   'head_lst': head_lst, 'server_list': server_list_dat,'union_name_list':union_name_list}, RequestContext(request))


@require_permission
def body_forbiden(request):
    server_id =  request.POST.get('server_id')
    # manager = GameManager.get_by_request(request)
    # btn_lst = manager.check_admin_permission()
    # if btn_lst:
    head_lst = [
        {'width': 70, 'name': u'日期'},
        {'width': 50, 'name': u'UID'},
        {'width': 55, 'name': u'昵称'},
        {'width': 50, 'name': u'等级'},
        {'width': 50, 'name': u'VIP等级'},
        {'width': 50, 'name': u'聊天内容'},
        {'width': 50, 'name': u'服务器ID'},
        {'width': 50, 'name': u'封禁'},
    ]
    server_list_dat = server_list.get_server_list_dat()
    if request.method == 'POST':
        server_id =  request.POST.get('server')
        user_id = request.POST.get('user_id')
        cmem_url=server_define.CMEM_MAP[int(server_id)]
        row_lst = _get_chat_content(server_id)
        for i in range(len(row_lst)):
            row_lst[i-1].append(server_id)
        if cmem_url:
            try:
                source=memcache.get_cmem_val(cmem_url,model_define.USER_MODEL.format(user_id=user_id))
                source['state']=USER_STATE_FREEZE
                memcache.put_cmem_val(cmem_url,model_define.USER_MODEL.format(user_id=user_id),source)
            except:
                print 'Error: not Forzen'
        return render_to_response("gm/get_chat_content.html",
                                  # {'account': manager.account, 'btn_lst': btn_lst,
                                   {'row_lst': row_lst,
                                   'head_lst': head_lst, 'server_list': server_list_dat,'cur_server_id':server_id}, RequestContext(request))
    else:
        server_id =  request.POST.get('server')
        row_lst = _get_chat_content(server_id)
        for i in range(len(row_lst)):
            row_lst[i-1].append(server_id)
        return render_to_response("gm/get_chat_content.html",
                                  # {'account': manager.account, 'btn_lst': btn_lst,
                                   {
                                      'row_lst': row_lst,
                                   'head_lst': head_lst, 'server_list': server_list_dat,'cur_server_id':server_id,}, RequestContext(request))

def _get_chat_content(server_id):
    """
         获取聊天信息
    """
    server_id = int(server_id)
    result = []
    cmem_url = server_define.CMEM_MAP[server_id]
    #print cmem_url
    if cmem_url:
        data = memcache.get_cmem_val(cmem_url, model_define.CHAT_MODEL)
        #print data
        for _log_line in data['chat_list']:
            result.append([time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(_log_line['time'])), _log_line['uid'],
                           _log_line['name'].decode('utf-8'), _log_line['lv'], _log_line['vip_level'],
                           decrypt(_log_line['content'], 159)])
    return result


def _get_union_chat_content(server_id,union_id,server_list_dat):
    server_id=int(server_id)
    result=[]
    cmem_url=server_define.CMEM_MAP[server_id]
    union_name_dict = _get_union_name_dict(server_list_dat)
    if cmem_url:
        data=memcache.get_cmem_val(cmem_url,model_define.UNION_CHAT_MODEL.format(union_id=union_id))
        if data is not None:
            for _log_line in data['chat_list']:
                union_name=union_name_dict[union_id]
                result.append([time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(_log_line['time'])),union_id,union_name,_log_line['uid'],
                              _log_line['name'].decode('utf-8'),_log_line['lv'],_log_line['vip_level'],
                              decrypt(_log_line['content'],159),server_id])
    return result


def _get_union_name(server_list_dat):
    result=[]
    for server_id in server_list_dat:
        cmem_url=server_define.CMEM_MAP[server_id['id']]
        if cmem_url :
            data=memcache.get_cmem_val(cmem_url,model_define.UNION_SEARCH_MODEL)
            data=data.values()
            for i in data[0].values():
                result.append({'id':i['u'],'name':i['n'],'server_id':server_id})
    return result

def _get_union_name_dict(server_list_dat):
    result={}
    for server_id in server_list_dat:
        cmem_url=server_define.CMEM_MAP[server_id['id']]
        if cmem_url:
            data=memcache.get_cmem_val(cmem_url,model_define.UNION_SEARCH_MODEL)
            data=data.values()
            for i in data[0].values():
                result[i['u']]=i['n']
    return result



