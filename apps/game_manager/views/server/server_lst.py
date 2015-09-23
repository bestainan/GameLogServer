# -*- coding:utf-8 -*-


from apps.game_manager.models.game_manager import *

from apps.game_manager.mysql import server_list
from django.http import HttpResponseRedirect
from django.template import RequestContext

from apps.utils import game_define
from apps.game_manager import game_manage_define
import datetime
from apps.logs.output_action_gm import *

SERVER_HIDDEN_NAME_DICT={
    1: u'隐藏',
    0: u'显示',
}

head_lst = [
    {'width': 70, 'name': u'服务器ID'},
    {'width': 50, 'name': u'URL'},
    {'width': 55, 'name': u'服务器名'},
    {'width': 50, 'name': u'服务器状态'},
    {'width': 50, 'name': u'版本号'},
    {'width': 50, 'name': u'开服时间'},
    {'width': 50, 'name': u'客户端隐藏'},
    {'width': 50, 'name': u'操作'},
]
def server_lst(request):
    """
    服武器列表
    """
    data = {}
    table_list = []
    all_server_lst = server_list.get_all_server(True)
    for server in all_server_lst:
        temp_content = []
        temp_content.insert(0,str(server['id']))
        temp_content.insert(1,str(server['url']))
        temp_content.insert(2,str(server['name']))
        temp_content.insert(3,str(game_define.SERVER_STATE_NAME_DICT[server['state']]))
        temp_content.insert(4,str(server['version']))
        temp_content.insert(5,str(server['open_server_time'].strftime('%Y-%m-%d')))
        temp_content.insert(6,SERVER_HIDDEN_NAME_DICT[server['hidden']])
        table_list.append(temp_content)

    data['ser_info'] = table_list
    data['head_lst'] = head_lst
    return render_to_response("server_lst/server_lst.html", data, RequestContext(request))

def server_add(request):
    """
    添加服务器信息
    """
    data = dict()
    data['server_state_val'] = game_define.SERVER_STATE_NAME_DICT.values()
    data['server_hidden_val'] = SERVER_HIDDEN_NAME_DICT.values()
    return render_to_response("server_lst/server_add.html", data,RequestContext(request))

def server_edit(request):
    """
    编辑服务器信息
    """
    server_id = int(request.POST.get("id"))
    server = server_list.get_server(server_id)
    _server_dict = dict()
    _server_dict['id'] = server['id']
    _server_dict['url'] = server['url']
    _server_dict['name'] = server['name']
    _server_dict['state'] = server['state']
    _server_dict['hidden'] = server['hidden']
    _server_dict['version'] = server['version']
    _server_dict['open_server_time'] = str(server['open_server_time'].strftime('%m/%d/%Y'))

    data = dict()
    data['server_state_val'] = game_define.SERVER_STATE_NAME_DICT.items()
    data['server_hidden_val'] = SERVER_HIDDEN_NAME_DICT.items()
    data['server'] = _server_dict
    return render_to_response("server_lst/server_edit.html", data,RequestContext(request))

def server_update(request):
    """
    更新服务器
    """
    if request.method == 'POST':
        server_id = int(request.POST.get('server_id'))
        # print('server_id '+str(server_id))
        url = str(request.POST.get('url'))
        # print('url '+str(url))
        name = str(request.POST.get('name'))
        # print('name '+str(name))
        server_state = int(request.POST.get('server_state'))
        # print('server_state '+str(server_state))
        version = str(request.POST.get('version'))
        # print('version '+str(version))
        open_server_time = datetime.datetime.strptime(request.POST.get('open_server_time'),"%m/%d/%Y").date()
        # print('open_server_time '+str(open_server_time))
        server_hidden = int(request.POST.get('server_hidden'))
        # print('server_hidden '+str(server_hidden))
        result = server_list.update_server(server_id, url, name, server_state, server_hidden, version, open_server_time)

        # 操作日志记录
        manager = GameManager.get_by_request(request)
        if result:  # 更新服务器
            insert_action_update_server(manager, server_id, url, name, server_state, server_hidden, version, open_server_time)
        else:  # 插入服务器
            insert_action_insert_server(manager, server_id, url, name, server_state, server_hidden, version, open_server_time)

        return HttpResponseRedirect('/Tyranitar6/server/server_lst/')
    else:
        return render_to_response("server_lst/server_add.html",RequestContext(request))

def server_del_confirm(request):
    """
    删除服务器确认
    """
    if request.method == 'POST':
        server_id = int(request.POST.get("id"))
        server = server_list.get_server(server_id)
        _server_dict = dict()
        _server_dict['id'] = server['id']
        _server_dict['url'] = server['url']
        _server_dict['name'] = server['name']
        _server_dict['state'] = game_define.SERVER_STATE_NAME_DICT[server['state']]
        _server_dict['hidden'] = SERVER_HIDDEN_NAME_DICT[server['hidden']]
        _server_dict['version'] = server['version']
        _server_dict['open_server_time'] = str(server['open_server_time'].strftime('%Y-%m-%d'))

        return render_to_response("server_lst/server_del_confirm.html", {'server': _server_dict,'head_lst': head_lst}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/server/server_lst/')

def server_del(request):
    """
    删除服务器
    """
    if request.method == 'POST':
        server_id = int(request.POST.get('id'))
        server_list.delete_server(server_id)

        # 操作日志记录
        manager = GameManager.get_by_request(request)
        insert_action_delete_server(manager, server_id)
        return HttpResponseRedirect('/Tyranitar6/server/server_lst/')
    else:
        return render_to_response("server_lst/server_add.html",RequestContext(request))