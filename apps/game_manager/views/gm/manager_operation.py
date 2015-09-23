# -*- coding:utf-8 -*-
import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.utils import game_define
from apps.game_manager.models.game_manager import *
from django.http import HttpResponse, HttpResponseRedirect

from apps.game_manager import game_manage_define
from apps.logs.gm.gm_operation import manager_operation
from apps.game_manager.mysql import mysql_game_manager


def get_manager_operation(request):
    """
        管理员操作查询
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:
        manager_list = mysql_game_manager.get_manager_account_name()
        # for i in game_manage_define.GM_LOG_ACTION_DICT:
        #     event_list.append(
        #         {
        #             'id': i,
        #             'name': game_manage_define.GM_LOG_ACTION_DICT[i]
        #         }
        #     )
        head_lst = []

        if request.method == 'POST':
            account = request.POST.get('account')
            search_date = request.POST.get("search_date")
            cur_account = account
            search_date_date = datetime.datetime.strptime(search_date, "%m/%d/%Y").date()
            print account, search_date
            try:
                head_lst, row_lst = manager_operation.get_table(account, search_date_date)
            except:
                return render_to_response("gm/manager_operation.html", locals(), RequestContext(request))

            return render_to_response("gm/manager_operation.html", locals(), RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            search_date = now_date_str
            return render_to_response("gm/manager_operation.html", locals(), RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')
