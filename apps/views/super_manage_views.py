# -*- coding:utf-8 -*-
import datetime

from django.conf import settings as _settings
from apps.logs.administrators import administrators_information
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from apps.game_manager.mysql import mysql_game_manager
from apps.game_manager.models.game_manager import GameManager
from apps.game_manager import game_manage_define


OUTPUT_PATH = _settings.MEDIA_ROOT + '/log_dump/'
OUTPUT_FILE_NAME = "log_module_event"



def select_account(request):
    '''
    超级管理员授权管理
    '''
    #七天冲级
    head_lst = [
        {'width': 50, 'name': u'ID'},
        {'width': 50, 'name': u'帐号'},
        {'width': 50, 'name': u'名字'},
        {'width': 50, 'name': u'权限'},
        {'width': 50, 'name': u'最后登录IP'},
        {'width': 50, 'name': u'最后登录时间'},
        {'width': 50, 'name': u'描述'},
        {'width': 50, 'name': u'操作'},
        ]
    if request.method == 'POST':
        return render_to_response('auth/super_manage.html', {'head_lst': head_lst},RequestContext(request))
    else:
        row_lst = administrators_information.get_table()
        print row_lst
        return render_to_response('auth/super_manage.html',{'head_lst': head_lst,'row_lst':row_lst}, RequestContext(request))

def register_user(request):
    """
    增加管理员
    """
    #回传一个权限列表
    permission_list = game_manage_define.MANAGER_PERMISSION[1:]
    return render_to_response('auth/register_user.html',{'permission_list':permission_list})


