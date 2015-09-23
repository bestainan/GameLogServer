# -*- coding:utf-8 -*-


from apps.game_manager.models.game_manager import *

from apps.game_manager.mysql import server_notice
from django.http import HttpResponseRedirect
from django.template import RequestContext
from apps.logs.output_action_gm import *
from apps.utils import game_define



head_lst = [
    {'width': 70, 'name': u'版本号'},
    {'width': 50, 'name': u'公告内容'},
    {'width': 50, 'name': u'操作'},
]
def version_notice_lst(request):
    """
    公告列表
    """
    data = {}
    table_list = []
    all_server_notice_dict = server_notice.get_all_notice()
    for val in all_server_notice_dict:
        temp_content = []
        temp_content.insert(0,str(val['version']))
        version_notice_utf = val['notice'].encode('utf-8')
        if version_notice_utf:
            temp_content.insert(1,str(version_notice_utf))
        else:
            temp_content.insert(1,str(u''))
        table_list.append(temp_content)

    data['version_notice_lst'] = table_list
    data['head_lst'] = head_lst
    return render_to_response("version_notice/version_notice_lst.html", data, RequestContext(request))

def version_notice_add(request):
    """
    添加公告信息
    """
    return render_to_response("version_notice/version_notice_add.html", RequestContext(request))

def version_notice_edit(request):
    """
    编辑公告信息
    """
    version = str(request.POST.get('version'))
    server_notice_dat = server_notice.get_version_notice(version)
    print server_notice_dat
    _server_notice_dict = dict()
    _server_notice_dict['version'] = version
    _server_notice_dict['notice'] = server_notice_dat['notice']

    data = dict()
    data['server_notice'] = _server_notice_dict
    return render_to_response("version_notice/version_notice_edit.html", data,RequestContext(request))

def version_notice_update(request):
    """
    更新公告
    """
    if request.method == 'POST':
        version = str(request.POST.get('version'))
        notice = request.POST.get('notice')
        result = server_notice.update_version_notice(notice.encode('utf-8'), version)

        # 操作日志记录
        manager = GameManager.get_by_request(request)
        if result:
            insert_action_update_version_notice(manager, version, notice.encode('utf-8'))
        else:
            insert_action_insert_version_notice(manager, version, notice.encode('utf-8'))
        return HttpResponseRedirect('/Tyranitar6/server/version_notice_lst/')
    else:
        return render_to_response("version_notice/version_notice_add.html",RequestContext(request))

def version_notice_del_confirm(request):
    """
    删除公告确认
    """
    if request.method == 'POST':
        version = str(request.POST.get('version'))
        server_notice_dat = server_notice.get_version_notice(version)
        _server_notice_dict = dict()
        _server_notice_dict['version'] = version
        _server_notice_dict['notice'] = server_notice_dat['notice']
        return render_to_response("version_notice/version_notice_del_confirm.html", {'server_notice': _server_notice_dict,'head_lst': head_lst}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/server/version_notice_lst/')

def version_notice_del(request):
    """
    删除公告
    """
    if request.method == 'POST':
        version = str(request.POST.get('version'))
        server_notice.delete_version_notice(version)

        # 操作日志记录
        manager = GameManager.get_by_request(request)
        insert_action_delete_version_notice(manager, version)
        return HttpResponseRedirect('/Tyranitar6/server/version_notice_lst/')
    else:
        return render_to_response("version_notice/version_notice_add.html",RequestContext(request))