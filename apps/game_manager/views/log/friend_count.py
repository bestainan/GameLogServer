
# -*- coding:utf-8 -*-
import datetime
from django.template import RequestContext
from apps.game_manager.views.log import daily_log
from apps.game_manager.models.game_manager import *
from django.http import HttpResponse, HttpResponseRedirect
from apps.common.decorators.decorators import require_permission
from apps.game_manager.mysql import server_list

@require_permission
def friend_count_function(request):
    """
    好友统计
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'时间'},
            {'width': 50, 'name': u'添加好友次数'},
            {'width': 50, 'name': u'通过申请好友数'},
            {'width': 50, 'name': u'通过申请好友占比'},
        ]
        if request.method == 'POST' :
            start_date = request.POST.get("search_start_date")
            end_date = request.POST.get("search_end_date")
            server_id = int(request.POST.get("server_id"))
            user_id=str(request.POST.get("user_id"))
            platform_id=request.POST.get('platform_id')
            start_date_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").date()
            end_date_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").date()

            server_list_dat=  server_list.get_server_list_dat()
            if user_id <> '':
                from apps.logs.statistics_tables.friend_count.friend_count_log import get_table
                row_lst =get_table(start_date_date, end_date_date, server_id)
                #     print server_list
                return render_to_response("log/friend_count.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date, 'server_list': server_list_dat,'platform_id':platform_id,'cur_server_id':server_id }, RequestContext(request))

        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list_dat =server_list.get_server_list_dat()
            return render_to_response("log/friend_count.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date,  'server_list': server_list_dat,'platform_id':'None'}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

#
# def _get_server_list():
#     """
#         获取游戏服务器列表
#     """
#     from apps.game_manager.mysql import server_list
#     all_server_list = server_list.get_all_server(True)
#     server_list = []
#     server_list.append({'id': -1, 'name': u'通服务器'},)
#     for item in all_server_list:
#         server_id = item['id']
#         server_name = item['name'] + '_' + str(item['id'])
#         server_dict = {'id': server_id, 'name': server_name}
#         server_list.append(server_dict)
#     platform_list = [
#         {'id': -1, 'name': u'通平台'},
#         {'id': 0, 'name': u'测试'},
#         {'id': 800003, 'name': u'海马'},
#         {'id': 800004, 'name': u'飞流'},
#         # {'id': 2, 'name': u'anysdk'},
#         {'id': 500001, 'name':  u'iOS-91手机助手'},
#         {'id': 500004, 'name':  u'iOS-iTools'},
#         {'id': 500015, 'name':  u'iOS-快用'},
#         {'id': 500017, 'name':  u'iOS-海马助手'},
#         {'id': 500020, 'name':  u'iOS-爱思助手'},
#         {'id': 500030, 'name':  u'iOS-XY助手'},
#         {'id': 500002, 'name':  u'同步推'},
#         {'id': 500003, 'name':  u'pp助手'},
#         {'id': 800006, 'name':  u'爱苹果'},
#         {'id': 500035, 'name':  u'叉叉助手'}
#     ]
#     return server_list, platform_list