# -*- coding:utf-8 -*-
import datetime
import json
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from apps.common.decorators.decorators import require_permission
from apps.game_manager.mysql import mysql_game_manager
from apps.game_manager.models.game_manager import GameManager
from apps.game_manager import game_manage_define
from apps.logs.output_action_gm import *


"""
Tyranitar6
"""


def index(request):
    """
        index
    """
    super_manager = mysql_game_manager.get_super_manager()
    if not super_manager:
        return HttpResponseRedirect(game_manage_define.MAIN_URL + "/register/")
    else:
        return HttpResponseRedirect(game_manage_define.MAIN_URL + "/login/")


def register(request):
    """
        超级管理员注册
    """
    super_manager = mysql_game_manager.get_super_manager()
    if not super_manager:
        if request.method == "POST":
            account = request.POST.get('account')
            password = request.POST.get('password')
            re_password = request.POST.get('re_password')
            name = request.POST.get('name')
            description = request.POST.get('description')

            if password != re_password:
                return render_to_response("auth/register.html", {'status': 1}, RequestContext(request))
            else:
                _gm = GameManager()
                _gm.account = account
                _gm.password = password
                _gm.name = name
                _gm.description = description
                _gm.permissions = 'Super'
                mysql_game_manager.insert_game_manager(_gm)
                # 操作日志记录
                insert_action_super_manager_register(_gm)
                return HttpResponseRedirect(game_manage_define.MAIN_URL)
        else:
            return render_to_response("auth/register.html", {}, RequestContext(request))
    else:
        return HttpResponseRedirect(game_manage_define.MAIN_URL + "/login/")


def login(request):
    """
        登录
    """
    if request.method == "POST":
        account = request.POST.get("account")
        password = request.POST.get("password")
        if not account:
            return render_to_response("auth/login.html", {"status": 1}, RequestContext(request))

        # 获取对应账号
        _gm = mysql_game_manager.get_game_manager(account)
        if _gm is None:
            return render_to_response("auth/login.html", {"status": 2}, RequestContext(request))
        if _gm.check_password(password):
            response = HttpResponseRedirect("/Tyranitar6/main/")
            # 记录登录信息
            _gm.login(datetime.datetime.now(), request.META["REMOTE_ADDR"], response)
            # 操作日志记录
            insert_action_manager_login(_gm)
            return response
        else:
            return render_to_response("auth/login.html", {"status": 3}, RequestContext(request))
    else:
        return render_to_response("auth/login.html", {}, RequestContext(request))


@require_permission
def main(request):
    """
        主页
    """

    return render_to_response("base/base.html", {}, RequestContext(request))

@require_permission
def view_index(request):
    _gm = GameManager.get_by_request(request)
    if _gm:
        return render_to_response('auth/change_admin_password.html', {'id': _gm.uid})
    else:
        return HttpResponseRedirect('login/')

@require_permission
def updata_admin_password(request):
    """
        修改管理员密码
    """
    passwd = request.POST.get('password')
    re_passwd = request.POST.get('re_password')
    uid = request.POST.get('id')
    if request.method == 'POST':
        if passwd != re_passwd:
            # 2次密码不对 返回页面重新输入
            return render_to_response("auth/change_admin_password.html", {'erro': u'2次密码不一致，请重新输入'},
                                      RequestContext(request))
        else:
            # 2次密码正确 扔数据库
            _gm = GameManager()
            _gm.password = passwd
            _gm.uid = uid
            mysql_game_manager.update_admin_password(_gm)
            # 操作日志记录
            insert_action_update_password(_gm)
            return HttpResponseRedirect('/Tyranitar6/login/')
    else:
        return render_to_response("auth/super_manage.html", {}, RequestContext(request))


@require_permission
def accept_post(request):
    from apps.game_manager.views import data_edit
    '''
    处理 JQ AJAX Post请求
    data_edit
    视图包 处理函数 不能删哦。
    '''
    value_dict = {}

    if request.is_ajax():
        value_dict['user_id'] = request.POST.get('user_id')
        value_dict['item_id'] = request.POST.get('item_id')
        value_dict['server_id'] = request.POST.get('server_id')
        value_dict['value'] = request.POST.get('value')
        value_dict['input_value'] = request.POST.get('input_value')
        value_dict['function_name'] = request.POST.get('function_name')
        value_dict['manager'] = GameManager.get_by_request(request)
        result = eval(value_dict['function_name'])(value_dict)
        if result :
            json_data = {
                'value': value_dict['input_value'],
            }
        else:
            json_data = {
                'value': value_dict['value'],
            }
        return HttpResponse(json.dumps(json_data), content_type='application/json')
