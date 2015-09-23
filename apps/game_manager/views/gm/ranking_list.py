# -*- coding:utf-8 -*-
"""
    排行榜查询
"""
import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.game_manager.models.game_manager import *

from apps.logs.gm.rank_list import level_rank_list as level_rank_list_table
from apps.game_manager.views.log import daily_log
from apps.logs.statistics_tables.activity import default_get_table
from django.http import HttpResponse, HttpResponseRedirect
def sort_rmb_view(request,dir_name,file_name):
    """
    充值排行榜
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:
        server_list, platform_list = daily_log._get_server_list()
        head_lst = [
            {'width': 50, 'name': u'排名'},
            {'width': 50, 'name': u'UID'},
            {'width': 50, 'name': u'金额'},]
        if request.method == 'POST':
            search_date = request.POST.get("search_date")
            server_id = int(request.POST.get('server_id'))

            search_date_date = datetime.datetime.strptime(search_date, "%m/%d/%Y").date()
            row_lst = default_get_table.get_table(search_date_date,dir_name,file_name,server_id)
            return render_to_response("gm/sort_rmb.html", {'account':manager.account,'btn_lst':btn_lst,'server_id':server_id,'row_lst': row_lst,'head_lst': head_lst,'server_list':server_list, 'search_date': search_date}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            search_date = now_date_str
            return render_to_response("gm/sort_rmb.html",{'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst, 'head_lst': head_lst, 'search_date': search_date,'server_list':server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

def expense_sort_view(request,dir_name,file_name):
    """
    消费排行榜
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:
        server_list, platform_list = daily_log._get_server_list()
        head_lst = [
            {'width': 50, 'name': u'排名'},
            {'width': 50, 'name': u'UID'},
            {'width': 50, 'name': u'消耗钻石'},
            ]
        if request.method == 'POST':
            search_date = request.POST.get("search_date")
            server_id = int(request.POST.get('server_id'))
            search_date_date = datetime.datetime.strptime(search_date, "%m/%d/%Y").date()
            row_lst = default_get_table.get_table(search_date_date,dir_name,file_name,server_id)
            return render_to_response("gm/expense_sort.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst,'search_date': search_date,'server_list':server_list, 'server_id': server_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            search_date = now_date_str
            return render_to_response("gm/expense_sort.html",{'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst, 'head_lst': head_lst, 'search_date': search_date,'server_list':server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')


def level_rank_list(request):
    """
        等级排行榜
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:
        server_list, platform_list = daily_log._get_server_list()
        head_lst = [
        {'width': 50, 'name': u'排名'},
        {'width': 50, 'name': u'角色ID'},
        {'width': 50, 'name': u'等级'},
    ]
        if request.method == 'POST':
            start_date = request.POST.get("start_date")

            start_date_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").date()
            server_id = int(request.POST.get("server_id"))

            # 分表设置显示
            # 总表行
            row_lst =level_rank_list_table.get_table(start_date_date,server_id)

            # server_list, platform_list = daily_log._get_server_list()
            return render_to_response("gm/level_rank_list.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst, 'head_lst': head_lst, 'start_date': start_date,'server_list': server_list,'server_id': server_id }, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            # end_date = now_date_str
            # server_list, platform_list = daily_log._get_server_list()
            return render_to_response("gm/level_rank_list.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst, 'head_lst': head_lst, 'start_date': start_date, 'server_list': server_list}, RequestContext(request))

    else:
        return HttpResponseRedirect('/Tyranitar6/login/')



