# -*- coding:utf-8 -*-
import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.game_manager.models.game_manager import *
from django.http import HttpResponse, HttpResponseRedirect


cost_item_save_dict={
    'cost_gold':'USER_COST_GOLD',
    'cost_stone':'USER_COST_STONE',
    'cost_free_draw':'USER_COST_FREE_DRAW',
    'cost_gym_point':'USER_COST_GYM_POINT',
    'cost_consumption_point':'USER_COST_SONSUMPTION_POINT',
    'cost_arena_emblem':'USER_COST_ARENA_EMBLEM',
    'cost_world_boss_point':'USER_COST_WORLD_BOSS_POINT',
    'cost_universal_fragment':'USER_COST_UNIVERSAL_FRAGMENT',
}
# cost_item_dict={
#     'cost_gold':'金币消耗',
#     'cost_stone':'钻石消耗',
#     'cost_free_draw':'精灵球消耗',
#     'cost_gym_point':'道馆币消耗',
#     'cost_consumption_point':'积分消耗',
#     'cost_arena_emblem':'纹章消耗',
#     'cost_world_boss_point':'战魂消耗',
#     'cost_universal_fragment':'万能碎片消耗'
# }
cost_item_dict={
    'cost_gold':'金币',
    'cost_stone':'钻石',
    'cost_free_draw':'精灵球',
    'cost_gym_point':'道馆币',
    'cost_consumption_point':'积分',
    'cost_arena_emblem':'纹章',
    'cost_world_boss_point':'战魂',
    'cost_universal_fragment':'万能碎片'
}

def user_cost(request):
    """
       消耗统计
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()

    if btn_lst:
        head_lst = [
            {'width': 50, 'name': u'使用时间'},
            {'width': 50, 'name': u'角色名'},
            {'width': 50, 'name': u'物品名称'},
            {'width': 50, 'name': u'数量'},
            {'width': 50, 'name': u'事件'},
        ]
        if request.method == 'POST' :
            start_date = request.POST.get("search_start_date")
            #end_date = request.POST.get("search_end_date")
            server_id = int(request.POST.get("server_id"))
            user_id=str(request.POST.get("user_id"))
            platform_id=request.POST.get('platform_id')
            try:
                start_date_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").date()
            except:
                start_date_date = datetime.datetime.now().date()
            #end_date_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").date()

            server_list, platform_list = _get_server_list()
            #return render_to_response("gm/user_data_search.html", {'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date,  'server_list': server_list,'platform_id':'None'}, RequestContext(request))

            #print server_list
            #分表设置显示
            if user_id<>'':
                from apps.logs.gm.user_data_search.user_cost_log import get_table
                row_lst =get_table(start_date_date,  user_id,server_id)
                #     print server_list
                print row_lst
                return render_to_response("gm/user_cost.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date,  'server_list': server_list,'platform_id':platform_id, 'cur_server_id': server_id,'user_id':user_id}, RequestContext(request))
            else:
                row_lst = []
                now_date_str = datetime.date.today().strftime("%m/%d/%Y")
                start_date = now_date_str
                end_date = now_date_str
                server_list, platform_list = _get_server_list()
                #some_list=cost_item_dict.keys()
                return render_to_response("gm/user_cost.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date,   'server_list': server_list,'platform_id':'None', 'cur_server_id': server_id}, RequestContext(request))

        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list()
            #some_list=cost_item_dict.keys()
            return render_to_response("gm/user_cost.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date,   'server_list': server_list,'platform_id':'None'}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')


def user_get(request):
    """
       消耗统计
    """
    head_lst = [
        {'width': 50, 'name': u'使用时间'},
        {'width': 50, 'name': u'角色名'},
        {'width': 50, 'name': u'物品名称'},
        {'width': 50, 'name': u'数量'},
        {'width': 50, 'name': u'事件'},
    ]
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        if request.method == 'POST' :
            start_date = request.POST.get("search_start_date")
            #end_date = request.POST.get("search_end_date")
            server_id = int(request.POST.get("server_id"))
            user_id=str(request.POST.get("user_id"))
            platform_id=request.POST.get('platform_id')
            try:
                start_date_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").date()
            except:
                start_date_date = datetime.datetime.now().date()
            #end_date_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").date()

            server_list, platform_list = _get_server_list()
            #return render_to_response("gm/user_data_search.html", {'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date,  'server_list': server_list,'platform_id':'None'}, RequestContext(request))

            #print server_list
            #分表设置显示
            if user_id<>'':
                from apps.logs.gm.user_data_search.user_get_log import get_table
                row_lst =get_table(start_date_date,  user_id,server_id)
                #     print server_list
                #  print row_lst
                return render_to_response("gm/user_get.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date,  'server_list': server_list,'platform_id':platform_id, 'cur_server_id': server_id,'user_id':user_id}, RequestContext(request))
            else:
                row_lst = []
                now_date_str = datetime.date.today().strftime("%m/%d/%Y")
                start_date = now_date_str
                end_date = now_date_str
                server_list, platform_list = _get_server_list()
                #some_list=cost_item_dict.keys()
                return render_to_response("gm/user_get.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date,   'server_list': server_list,'platform_id':'None', 'cur_server_id': server_id}, RequestContext(request))

        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list()
            #some_list=cost_item_dict.keys()
            return render_to_response("gm/user_get.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date,   'server_list': server_list,'platform_id':'None'}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')


def equipment_strengthening_record(request):
    """
        装备强化记录
    """
    head_lst = [
    {'width': 50, 'name': u'操作时间'},
    {'width': 50, 'name': u'角色名'},
    {'width': 50, 'name': u'用户事件'},
    {'width': 50, 'name': u'消耗金币'},
    {'width': 50, 'name': u'消耗强化石'},
    ]
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:
        if request.method == 'POST':
            start_date = request.POST.get("start_date")
            # end_date = request.POST.get("end_date")
            # start_date = request.POST.get("search_start_date")
            try:
                start_date_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").date()
            except:
                start_date_date = datetime.datetime.now().date()
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))




            # start_date_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").date()
            # end_date_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").date()
            # 分表设置显示
            # 总表行
            from apps.logs.gm.user_data_search.equipment_strengthening_record import get_table
            row_lst =get_table(start_date_date,server_id)
            print row_lst
            server_list, platform_list = _get_server_list()
            return render_to_response("gm/equipment_strengthening_record.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst, 'head_lst': head_lst, 'start_date': start_date,'end_date': start_date_date, 'server_list': server_list, 'cur_server_id': server_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("gm/equipment_strengthening_record.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst, 'head_lst': head_lst, 'start_date': start_date, 'end_date': start_date, 'server_list': server_list}, RequestContext(request))

    else:
        return HttpResponseRedirect('/Tyranitar6/login/')




def _get_server_list():
    """
        获取游戏服务器列表
    """
    from apps.game_manager.mysql import server_list
    all_server_list = server_list.get_all_server(True)
    server_list = []
    #server_list.append({'id': -1, 'name': u'通服务器'},)
    for item in all_server_list:
        server_id = item['id']
        server_name = item['name'] + '_' + str(item['id'])
        server_dict = {'id': server_id, 'name': server_name}
        server_list.append(server_dict)
    platform_list = [
        {'id': -1, 'name': u'通平台'},
        {'id': 0, 'name': u'测试'},
        {'id': 800003, 'name': u'海马'},
        {'id': 800004, 'name': u'飞流'},
        # {'id': 2, 'name': u'anysdk'},
        {'id': 500001, 'name':  u'iOS-91手机助手'},
        {'id': 500004, 'name':  u'iOS-iTools'},
        {'id': 500015, 'name':  u'iOS-快用'},
        {'id': 500017, 'name':  u'iOS-海马助手'},
        {'id': 500020, 'name':  u'iOS-爱思助手'},
        {'id': 500030, 'name':  u'iOS-XY助手'},
        {'id': 500002, 'name':  u'同步推'},
        {'id': 500003, 'name':  u'pp助手'},
        {'id': 800006, 'name':  u'爱苹果'},
        {'id': 500035, 'name':  u'叉叉助手'}
    ]
    return server_list, platform_list