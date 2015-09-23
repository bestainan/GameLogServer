# -*- coding:utf-8 -*-
import datetime
from django.template import RequestContext
from django.conf import settings as _settings
from apps.game_manager.views.log import daily_log
from apps.logs.statistics_tables.activity import default_get_table
from apps.game_manager.models.game_manager import *
from django.http import HttpResponse, HttpResponseRedirect
from apps.common.decorators.decorators import require_permission

OUTPUT_PATH = _settings.MEDIA_ROOT + '/log_dump/'
OUTPUT_FILE_NAME = "log_module_event"

@require_permission
def activity_view(request, template, dir_name, file_name):
    """
        7天冲级
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:
        if file_name == 'SEVEN_DAYS_LV':
            head_lst = [
                {'width': 50, 'name': u'时间'},
                {'width': 50, 'name': u'Lv30领取次数'},
                {'width': 50, 'name': u'Lv40领取次数'},
                {'width': 50, 'name': u'Lv50领取次数'},
                {'width': 50, 'name': u'Lv60领取次数'},
                ]

        #七天战力
        elif file_name == 'SEVENT_DAY_FIGHT':
            head_lst = [
                {'width': 50, 'name': u'时间'},
                {'width': 50, 'name': u'3万战力领取次数'},
                {'width': 50, 'name': u'5万战力领取次数'},
                {'width': 50, 'name': u'8万战力领取次数'},
                {'width': 50, 'name': u'10万战力领取次数'},
                ]

        #满额福利
        elif file_name == 'MAX_WILL':
            head_lst = [
                {'width': 50, 'name': u'时间'},
                {'width': 50, 'name': u'充值30元档充值次数'},
                {'width': 50, 'name': u'充值100元档领取次数'},
                {'width': 50, 'name': u'充值300元档领取次数'},
                {'width': 50, 'name': u'充值600元档领取次数'},
                ]
        #消费有礼
        elif file_name == 'GIVE_ME_GIVE_YOU':
            head_lst = [
                {'width': 50, 'name': u'时间'},
                {'width': 50, 'name': u'消费1000钻领取次数'},
                {'width': 50, 'name': u'消费3000钻领取次数'},
                {'width': 50, 'name': u'消费5000钻领取次数'},
                {'width': 50, 'name': u'消费8000钻领取次数'},
                {'width': 50, 'name': u'消费10000钻领取次数'},
                {'width': 50, 'name': u'消费15000钻领取次数'},
                {'width': 50, 'name': u'消费24000钻领取次数'},
                ]
        #友好商店
        elif file_name == 'FRIENDLY_SHOP':
            head_lst = [
                {'width': 50, 'name': u'兑换物品'},
                {'width': 50, 'name': u'兑换次数'},
                {'width': 50, 'name': u'兑换人数'},
                {'width': 50, 'name': u'参与率'},
                {'width': 50, 'name': u'人数占比'},
                ]

        #微信分享
        elif file_name == 'WEI_CHAT_SHARE':
            head_lst = [
                {'width': 50, 'name': u'达到30级'},
                {'width': 50, 'name': u'战力达到10万'},
                {'width': 50, 'name': u'通关普通副本第八章'},
                {'width': 50, 'name': u'道馆挑战30星'},
                {'width': 50, 'name': u'达到50级'},
                ]

        server_list, platform_list = daily_log._get_server_list()

        if request.method == 'POST':
            search_date = request.POST.get("search_data")
            server_id = int(request.POST.get('server_id'))
            start_date_date = datetime.datetime.strptime(search_date, "%m/%d/%Y").date()
            if file_name == 'MAX_WILL' or file_name == 'FRIENDLY_SHOP':
                row_lst = default_get_table.get_table_one_list(start_date_date,dir_name,file_name,server_id)
            else:
                row_lst = default_get_table.get_table(start_date_date,dir_name,file_name,server_id)
            return render_to_response(template, {'row_lst': row_lst,
                                                 'head_lst': head_lst,
                                                 'server_list':server_list,
                                                 'search_data': search_date,
                                                 'server_id':server_id,
                                                 'btn_lst':btn_lst,
                                                 'account':manager.account,},RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            search_date = now_date_str
            return render_to_response(template,{'server_list':server_list,
                                                'row_lst': row_lst,
                                                'head_lst': head_lst,
                                                'search_data':search_date,
                                                'btn_lst':btn_lst,
                                                'account':manager.account,}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')


