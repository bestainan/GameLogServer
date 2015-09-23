# -*- coding:utf-8 -*-
import datetime
from apps.common.decorators.decorators import require_permission
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.logs.gm.recharge_manage import recharge_search as get_recharge_search
from apps.logs.gm.recharge_manage import cost_search as get_cost_search
from apps.game_manager.views.log import daily_log as server_config
from apps.game_manager.models.game_manager import *
from django.http import HttpResponse, HttpResponseRedirect

#充值管理 充值查询
@require_permission
def recharge_search(request):
    """
        GM充值查询
    """
    head_lst = [
        {'width': 50, 'name': u'充值时间'},
        {'width': 50, 'name': u'账号UID'},
        {'width': 50, 'name': u'充值金额'},
        {'width': 50, 'name': u'订单号'},
        {'width': 50, 'name': u'是否为首次充值'},
        {'width': 50, 'name': u'服务器'},
        {'width': 50, 'name': u'平台'},
    ]
    if request.method == 'POST':
        search_start_date = request.POST.get("search_start_date")
        search_end_date = request.POST.get("search_end_date")
        uid_id = request.POST.get("uid_id")
        start_date = datetime.datetime.strptime(search_start_date,"%m/%d/%Y").date()
        end_date = datetime.datetime.strptime(search_end_date,"%m/%d/%Y").date()
        server_id = int(request.POST.get("server_id"))
        # channel_id = int(request.POST.get("channel_id"))

        row_lst = get_recharge_search.get_table(start_date,end_date,server_id,uid_id)

        server_list, platform_list = server_config._get_server_list(None, None)
        return render_to_response("gm/recharge_search.html", locals(), RequestContext(request))
    else:
        row_lst = []
        now_date_str = datetime.date.today().strftime("%m/%d/%Y")
        search_start_date = now_date_str
        search_end_date = now_date_str
        server_list, platform_list = server_config._get_server_list()
        return render_to_response("gm/recharge_search.html", locals(), RequestContext(request))


#充值管理 消费查询
@require_permission
def cost_search(request):
    """
        GM消费查询
    """
    head_lst = [
        {'width':50,'name':u'消费时间'},
        {'width':50,'name':u'账号UID'},
        {'width':50,'name':u'消耗金币'},
        {'width':50,'name':u'消耗钻石'},
        {'width':50,'name':u'消耗物品'},
        {'width':50,'name':u'服务器ID'},
        {'width':50,'name':u'平台ID'},
    ]
    if request.method == 'POST':
        search_start_date = request.POST.get("search_start_date")
        search_end_date = request.POST.get("search_end_date")
        uid_id = request.POST.get("uid_id")
        start_date = datetime.datetime.strptime(search_start_date,"%m/%d/%Y").date()
        end_date = datetime.datetime.strptime(search_end_date,"%m/%d/%Y").date()
        server_id = int(request.POST.get("server_id"))
        # channel_id = int(request.POST.get("channel_id"))

        row_lst, head_lst = get_cost_search.get_table(start_date, end_date, server_id,  uid_id)

        server_list, platform_list = server_config._get_server_list()
        return render_to_response("gm/cost_search.html", locals(), RequestContext(request))
    else:
        row_lst = []
        now_date_str = datetime.date.today().strftime("%m/%d/%Y")
        search_start_date = now_date_str
        search_end_date = now_date_str
        server_list, platform_list = server_config._get_server_list()
        return render_to_response("gm/cost_search.html", locals(), RequestContext(request))

