# -*- coding:utf-8 -*-
import datetime
from django.template import RequestContext
from apps.logs.statistics_tables.union import union_hall_log as union_hall_modes
from apps.game_manager.models.game_manager import *
from django.http import HttpResponse, HttpResponseRedirect
from apps.game_manager.mysql import server_list
from apps.common.decorators.decorators import require_permission

@require_permission
def union_count_function(request):
    """
       联盟统计
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()

    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'时间'},
            {'width': 50, 'name': u'创建联盟人数'},
            {'width': 50, 'name': u'创建联盟消耗钻石'},
            {'width': 50, 'name': u'申请联盟次数'},
            {'width': 50, 'name': u'申请联盟成功人数'},
            {'width': 50, 'name': u'申请联盟成功率'},
            {'width': 50, 'name': u'联盟功能开启人数'},
            {'width': 50, 'name': u'进入联盟人数占比'},
        ]
        if request.method == 'POST' :
            start_date = request.POST.get("search_start_date")
            end_date = request.POST.get("search_end_date")
            server_id = int(request.POST.get("server_id"))
            try:
                start_date_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").date()
            except:
                start_date_date = datetime.datetime.now().date()
            try:
                end_date_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").date()
            except:
                end_date_date=start_date_date

            server_list_dat = server_list.get_server_list_dat()

            from apps.logs.statistics_tables.union.union_count_log import get_table
            row_lst =get_table(start_date_date, end_date_date,server_id)
            print row_lst

            return render_to_response("log/union_count.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date, 'server_list': server_list_dat,'cur_server_id':server_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list_dat = server_list.get_server_list_dat()
            #some_list=cost_item_dict.keys()
            return render_to_response("log/union_count.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date,  'server_list': server_list_dat}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def union_buy_reward_function(request):

    """
       联盟奖励信息
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()

    if btn_lst:

        from apps.logs.statistics_tables.union.union_buy_reward_log import get_table
        head_lst = [
            {'width': 50, 'name': u'购买物品'},
            {'width': 50, 'name': u'奖励购买次数'},
            #{'width': 50, 'name': u'各奖励到达到要求人数'},
            {'width': 50, 'name': u'各奖励购买率'},
            {'width': 50, 'name': u'奖励购买消耗联盟币'},
            {'width': 50, 'name': u'奖励购买产出'},
        ]
        if request.method == 'POST' :
            start_date = request.POST.get("search_start_date")
            # end_date = request.POST.get("search_end_date")
            server_id = int(request.POST.get("server_id"))
            #user_id=str(request.POST.get("user_id"))
            #platform_id=(request.POST.get('platform_id'))
            try:
                start_date_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").date()
            except:
                start_date_date = datetime.datetime.now().date()
            # end_date_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").date()
            server_list_dat = server_list.get_server_list_dat()
            row_lst =get_table(start_date_date,server_id)
            return render_to_response("log/union_buy_reward.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date,'server_list': server_list_dat,'cur_server_id':server_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list_dat = server_list.get_server_list_dat()
            #some_list=cost_item_dict.keys()
            return render_to_response("log/union_buy_reward.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date,  'server_list': server_list_dat}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def union_sign_function(request):
    """
       联盟签到信息
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        from apps.logs.statistics_tables.union.union_sign_log import get_table
        head_lst = [
            {'width': 50, 'name': u'时间'},
            {'width': 50, 'name': u'普通签到人数'},
            {'width': 50, 'name': u'高级签到人数'},
            {'width': 50, 'name': u'豪华签到人数'},
            {'width': 50, 'name': u'普通签到消耗金币'},
            {'width': 50, 'name': u'高级签到消耗钻石'},
            {'width': 50, 'name': u'豪华签到消耗钻石'},
            {'width': 50, 'name': u'签到产出联盟币数'},
            {'width': 50, 'name': u'进度礼包产出金色精华数'},
            {'width': 50, 'name': u'进度礼包产出金币数'},
            {'width': 50, 'name': u'进度礼包产出联盟币数'},
            {'width': 50, 'name': u'进度礼包产出钻石数'},
        ]
        if request.method == 'POST' :
            start_date = request.POST.get("search_start_date")
            end_date = request.POST.get("search_end_date")
            server_id = int(request.POST.get("server_id"))
            #user_id=str(request.POST.get("user_id"))
            #platform_id=(request.POST.get('platform_id'))
            try:
                start_date_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").date()
            except:
                start_date_date = datetime.datetime.now().date()
            try:
                end_date_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").date()
            except:
                end_date_date=start_date_date
            server_list_dat = server_list.get_server_list_dat()
            row_lst =get_table(start_date_date, end_date_date,server_id)
            return render_to_response("log/union_sign.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date, 'server_list': server_list_dat,'cur_server_id':server_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list_dat = server_list.get_server_list_dat()
            #some_list=cost_item_dict.keys()
            return render_to_response("log/union_sign.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date,  'server_list': server_list_dat}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def union_stage_function(request):
    """
       联盟副本信息
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()

    if btn_lst:

        from apps.logs.statistics_tables.union.union_stage_log import  get_table
        head_lst = [
            {'width': 50, 'name': u'副本名称'},
            {'width': 50, 'name': u'副本开启次数'},
            {'width': 50, 'name': u'副本开启率'},
            {'width': 50, 'name': u'副本通关次数'},
            {'width': 50, 'name': u'副本通关率'},
            {'width': 50, 'name': u'关卡名称'},
            {'width': 50, 'name': u'参与次数'},
            {'width': 50, 'name': u'参与人数'},
            {'width': 50, 'name': u'关卡通关次数'}
        ]
        if request.method == 'POST' :
            start_date = request.POST.get("search_start_date")
            #end_date = request.POST.get("search_end_date")
            server_id = int(request.POST.get("server_id"))
            #user_id=str(request.POST.get("user_id"))
            #platform_id=(request.POST.get('platform_id'))
            try:
                start_date_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").date()
            except:
                start_date_date = datetime.datetime.now().date()
            #end_date_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").date()
            server_list_dat = server_list.get_server_list_dat()
            row_lst =get_table(start_date_date,server_id)
            return render_to_response("log/union_stage.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date,  'server_list': server_list_dat,'cur_server_id':server_id,}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            #end_date = now_date_str
            server_list_dat = server_list.get_server_list_dat()
            #some_list=cost_item_dict.keys()
            return render_to_response("log/union_stage.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date,  'server_list': server_list_dat}, RequestContext(request))

    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def union_shop_function(request):


    """
       联盟商店
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()

    if btn_lst:

        from apps.logs.statistics_tables.union.union_shop_log import get_table
        head_lst = [
            {'width': 50, 'name': u'购买物品'},
            {'width': 50, 'name': u'联盟币消耗'},
            {'width': 50, 'name': u'购买人数'},
            {'width': 50, 'name': u'购买次数'},
            {'width': 50, 'name': u'参与率'},
            {'width': 50, 'name': u'联盟币消耗占比'},
            {'width': 50, 'name': u'人数占比'},
        ]
        if request.method == 'POST' :
            start_date = request.POST.get("search_start_date")
            # end_date = request.POST.get("search_end_date")
            server_id = int(request.POST.get("server_id"))
            #user_id=str(request.POST.get("user_id"))
            #platform_id=(request.POST.get('platform_id'))
            try:
                start_date_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").date()
            except:
                start_date_date = datetime.datetime.now().date()
            # end_date_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").date()
            server_list_dat = server_list.get_server_list_dat()
            row_lst =get_table(start_date_date,server_id)
            return render_to_response("log/union_shop.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date, 'server_list': server_list_dat,'cur_server_id':server_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list_dat = server_list.get_server_list_dat()
            #some_list=cost_item_dict.keys()
            return render_to_response("log/union_shop.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date,  'server_list': server_list_dat}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def union_hall_function(request):
    """
       联盟殿堂
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'联盟等级'},
            {'width': 50, 'name': u'联盟数量'},
            {'width': 50, 'name': u'联盟成员数量'},
            {'width': 50, 'name': u'解散联盟数量'},
            {'width': 50, 'name': u'联盟占比'},
            {'width': 50, 'name': u'联盟成员占比'},
            {'width': 50, 'name': u'服务器ID'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            server_id = int(request.POST.get("server_id"))
            try:
                start_date_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").date()
            except:
                start_date_date = datetime.datetime.now().date()

            row_lst = union_hall_modes.get_table(start_date_date, server_id)

            server_list_dat = server_list.get_server_list_dat()
            return render_to_response("log/union_hall.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'server_list': server_list_dat,'cur_server_id':server_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            server_list_dat = server_list.get_server_list_dat()
            return render_to_response("log/union_hall.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'server_list': server_list_dat}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

