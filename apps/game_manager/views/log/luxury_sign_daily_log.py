# -*- coding:utf-8 -*-
import datetime
from django.template import RequestContext
from apps.game_manager.views.log import daily_log as server_config
from apps.logs.statistics_tables.luxury_sign import sign_count as sign_count_py
from apps.game_manager.models.game_manager import *
from django.http import HttpResponse, HttpResponseRedirect
from apps.common.decorators.decorators import require_permission

@require_permission
def sign_count_function(request):
    """
        豪华签到 次数统计
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width':50,'name':u'时间'},
            {'width':50,'name':u'签到次数'},
            {'width':50,'name':u'到达人数要求'},
            {'width':50,'name':u'领取率'},
            {'width':50,'name':u'服务器ID'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            end_date = request.POST.get("search_end_date")
            start_date_date = datetime.datetime.strptime(start_date,"%m/%d/%Y").date()
            end_date_date = datetime.datetime.strptime(end_date,"%m/%d/%Y").date()
            server_id = int(request.POST.get("server_id"))

            row_lst = sign_count_py.get_table(start_date_date,end_date_date,server_id)#uid)
            server_list, platform_list = server_config._get_server_list()
            return render_to_response("log/sign_count.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst,  'search_start_date': start_date, 'search_end_date': end_date, 'server_list': server_list,'cur_server_id':server_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = server_config._get_server_list()
            return render_to_response("log/sign_count.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst, 'head_lst': head_lst,  'search_start_date': start_date, 'search_end_date': end_date, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def sign_create_function(request):
    """
        日志豪华签到产出统计
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width':50,'name':u'我是产出统计！！！！'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            end_date = request.POST.get("search_end_date")
            # uid = request.POST.get("uid_id")
            start_date_date = datetime.datetime.strptime(start_date,"%m/%d/%Y").date()
            end_date_date = datetime.datetime.strptime(end_date,"%m/%d/%Y").date()
            server_id = int(request.POST.get("server_id"))
            channel_id = int(request.POST.get("channel_id"))

            # row_lst, head_lst = sign_create_py.get_table(start_date_date, end_date_date, server_id, channel_id)# uid)
            row_lst,head_lst = []
            server_list, platform_list = server_config._get_server_list()
            return render_to_response("gm/cost_search.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst, 'head_lst': head_lst,  'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list,'cur_server_id':server_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = server_config._get_server_list()
            return render_to_response("gm/cost_search.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst, 'head_lst': head_lst,  'search_start_date': start_date, 'search_end_date': end_date,'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')
