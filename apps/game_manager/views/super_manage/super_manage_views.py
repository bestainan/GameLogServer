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
from apps.common.decorators.decorators import require_permission
from apps.logs.output_action_gm import *

OUTPUT_PATH = _settings.MEDIA_ROOT + '/log_dump/'
OUTPUT_FILE_NAME = "log_module_event"


@require_permission
def select_account(request):
    """
        超级管理员授权管理
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 20, 'name': u'ID'},
            {'width': 50, 'name': u'帐号'},
            {'width': 50, 'name': u'名字'},
            {'width': 50, 'name': u'权限'},
            {'width': 50, 'name': u'最后登录IP'},
            {'width': 50, 'name': u'最后登录时间'},
            {'width': 50, 'name': u'描述'},
            {'width': 50, 'name': u'操作'},
            ]

        if request.method == 'POST':
            return render_to_response('auth/super_manage.html', {'account':manager.account,'btn_lst':btn_lst,'head_lst': head_lst},RequestContext(request))
        else:
            row_lst = administrators_information.get_table()
            return render_to_response('auth/super_manage.html',{'account':manager.account,'btn_lst':btn_lst,'head_lst': head_lst,'row_lst':row_lst}, RequestContext(request))
    else:
        return HttpResponseRedirect('login/')


@require_permission
def register_user(request):
    """
        返回一个页面
    """
    #回传一个权限列表
    permission_list = game_manage_define.MANAGER_PERMISSION[1:]

    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:
        return render_to_response('auth/register_user.html',{'account':manager.account,'btn_lst':btn_lst,'permission_list':permission_list})
    else:
        return HttpResponseRedirect('login/')


@require_permission
def add_admin(request):
    """
        管理员注册
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    permission_list = game_manage_define.MANAGER_PERMISSION[1:]
    if btn_lst:
        if request.method == "POST":
            account = request.POST.get('account')
            password = request.POST.get('password')
            re_password = request.POST.get('re_password')
            name = request.POST.get('name')
            description = request.POST.get('description')
            permission = request.POST.get('permission')

            if password != re_password:

                return render_to_response("auth/register_user.html", {'btn_lst':btn_lst,'permission_list':permission_list}, RequestContext(request))
            else:
                _gm = GameManager()
                _gm.account = account
                _gm.password = password
                _gm.name = name
                _gm.permissions = permission
                _gm.description = description
                mysql_game_manager.insert_game_manager(_gm)
                # 操作日志记录
                insert_action_manager_register(_gm)
                return HttpResponseRedirect('/Tyranitar6/super_man/select_account/')
    else:
        return HttpResponseRedirect('login/')


@require_permission
def delete_user(request):
    """
        删除一个管理员
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()

    if btn_lst:
        if request.method == 'POST':
            del_id = request.POST.get('id')
            mysql_game_manager.del_admin_by_id(del_id)
            # 操作日志记录
            insert_action_delete_manager(manager, del_id)
            return HttpResponseRedirect('/Tyranitar6/super_man/select_account/')
        else:
            return HttpResponseRedirect('/Tyranitar6/super_man/select_account/')
    else:
        return HttpResponseRedirect('login/')


@require_permission
def update_user(request):
    """
        修改信息页面
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()

    #接收 修改的数据
    #帐号  名字  权限 描述
    if btn_lst:
        account = request.POST.get('account')
        name = request.POST.get('name')
        permission_name = request.POST.get('permission')
        description = request.POST.get('description')
        permission_list = game_manage_define.MANAGER_PERMISSION[1:]
        return render_to_response("auth/change_admin_info.html", {'btn_lst':btn_lst,
                                                                  'account':account,
                                                                  'name':name,
                                                                  'permission_name':permission_name,
                                                                  'description':description,
                                                                  'permission_list':permission_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('login/')


@require_permission
def update_data(request):
    """
        更新admin信息
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    permission_list = game_manage_define.MANAGER_PERMISSION[1:]
    account = request.POST.get('account')
    name = request.POST.get('name')
    permission_name = request.POST.get('permission')
    description = request.POST.get('description')
    if btn_lst:
        if request.method == 'POST':
            #2次密码正确 扔数据库
            _gm = GameManager()
            _gm.account = account
            _gm.name = name
            _gm.permissions = permission_name
            _gm.description = description
            mysql_game_manager.update_game_infomation(_gm)
            # 操作日志记录
            insert_action_update_manager_info(manager, account, name, permission_name, description)
            return HttpResponseRedirect('/Tyranitar6/super_man/select_account/')
        else:
            return render_to_response("auth/super_manage.html", {'btn_lst':btn_lst}, RequestContext(request))
    else:
        return HttpResponseRedirect('login/')

@require_permission
def updata_password(request):
    #更新admin密码
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    passwd = request.POST.get('password')
    re_passwd = request.POST.get('re_password')

    if btn_lst:

        if request.method == 'POST':
            if passwd != re_passwd:
                #2次密码不对 返回页面重新输入
                return render_to_response("auth/change_admin_info.html", {'erro':u'2次密码不一致，请重新输入'}, RequestContext(request))
            else:
                #2次密码正确 扔数据库
                _gm = GameManager()
                _gm.password = passwd
                mysql_game_manager.update_admin_password(_gm)
                # 操作日志记录
                insert_action_update_password(_gm)
                return HttpResponseRedirect('Tyranitar6/updata_password/')
        else:
            return render_to_response("base/base.html", {'account':manager.account,'btn_lst':btn_lst}, RequestContext(request))
    else:
        return HttpResponseRedirect('login/')