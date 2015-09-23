# -*- coding:utf-8 -*-
import datetime

from django.template import RequestContext
from apps.game_manager.views.log import daily_log
from apps.utils import game_define
from apps.logs.gm.player_behevior import behevior
from apps.game_manager.models.game_manager import *
from django.http import HttpResponse, HttpResponseRedirect

def stage_player_behavior(request,dir_name):
    """
        玩家行为分析
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:
        event_list = []
        for i in game_define.EVENT_LOG_ACTION_DICT:
            event_list.append({'id':int(game_define.EVENT_LOG_ACTION_DICT[i].split('-')[0]),
                                'name':game_define.EVENT_LOG_ACTION_DICT[i].split('-')[1]
                                })
        head_lst = []

        server_list, platform_list = daily_log._get_server_list()
        if request.method == 'POST':
            uid = request.POST.get('search_player_id')
            event = request.POST.get('event_id')
            sreach_data = request.POST.get("sreach_data")
            server_id = int(request.POST.get('server_id'))
            search_player_id = request.POST.get('search_player_id')
            cur_event_id = int(event.split('-')[0])
            try:
                start_date_date = datetime.datetime.strptime(sreach_data, "%m/%d/%Y").date()
            except UnicodeEncodeError:
                return HttpResponseRedirect('/Tyranitar6/gm/stage_player_behavior/')
            except ValueError:
                return HttpResponseRedirect('/Tyranitar6/gm/stage_player_behavior/')
            head_lst,row_lst = behevior.get_table(uid,event,start_date_date,server_id,dir_name)

            return render_to_response("gm/stage_player_behevior.html", locals(), RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            sreach_data = now_date_str
            return render_to_response("gm/stage_player_behevior.html",locals(), RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')
