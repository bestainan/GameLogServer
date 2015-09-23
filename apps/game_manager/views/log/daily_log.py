# -*- coding:utf-8 -*-
import datetime
from django.template import RequestContext
from django.conf import settings as _settings
from apps.utils import game_define

from apps.logs.statistics_tables.product_daily_situation import statistics_total as statistics_total_table
from apps.logs.statistics_tables.product_daily_situation import user_retain as user_retain_table
from apps.logs.statistics_tables.product_daily_situation import amount_analyse as amount_analyse_table
from apps.logs.statistics_tables.product_daily_situation import online_time as online_time_table
from apps.logs.statistics_tables.product_daily_situation import online_time_user_num as online_time_user_num_table

from apps.logs.statistics_tables.user_payment_analyse import new_k_days_income as new_k_days_income_table
from apps.logs.statistics_tables.user_payment_analyse import payment_level_analyse as payment_level_analyse_table
from apps.logs.statistics_tables.user_payment_analyse import player_first_recharge_level as player_first_recharge_level_table
from apps.logs.statistics_tables.user_payment_analyse import recharge_cycle as recharge_cycle_table
from apps.logs.statistics_tables.user_payment_analyse import user_life_time_value as user_life_time_value_table
from apps.logs.statistics_tables.user_payment_analyse import payment_point_analyse as payment_point_analyse_table
from apps.logs.statistics_tables.user_statistic import vip_distributed as vip_distributed_table
from apps.logs.statistics_tables.user_statistic import user_first_recharge as user_first_recharge_table
from apps.logs.statistics_tables.user_statistic import user_recharge_state as user_recharge_state_table
from apps.logs.statistics_tables.loss_analyse import newbie_state as newbie_state_table
from apps.logs.statistics_tables.loss_analyse import guide_state as guide_state_table
from apps.logs.statistics_tables.loss_analyse import user_level_lost_state as user_level_lost_state_table
from apps.logs.statistics_tables.loss_analyse import user_level_state as user_level_state_table
from apps.logs.statistics_tables.loss_analyse import user_life_cycle as user_life_cycle_table
from apps.logs.statistics_tables.loss_analyse import user_structure as user_structure_table
from apps.logs.statistics_tables.past_experience import first_play_time as first_play_time_table
from apps.logs.statistics_tables.consume_point_analyse import daily_consume_distributed as daily_consume_distributed_table
from apps.logs.statistics_tables.consume_point_analyse import user_first_cost_stone_gold as user_first_cost_stone_table
from apps.logs.statistics_tables.consume_point_analyse import user_level_consume_gold_state as user_level_consume_gold_state_table
from apps.logs.statistics_tables.consume_point_analyse import user_level_consume_stone_state as user_level_consume_stone_state_table
from apps.logs.statistics_tables.consume_point_analyse import user_stone_shop as user_stone_shop_table

from apps.logs.statistics_tables.number_balance import user_cost_gold as user_cost_gold_table
from apps.logs.statistics_tables.number_balance import user_generate_gold as user_generate_gold_table
from apps.logs.statistics_tables.number_balance import user_generate_stone as user_generate_stone_table
from apps.logs.statistics_tables.number_balance import user_cost_gold_with_vip as user_cost_gold_with_vip_table
from apps.logs.statistics_tables.number_balance import user_cost_stone as user_cost_stone_table
from apps.logs.statistics_tables.number_balance import user_cost_stone_with_vip as user_cost_stone_with_vip_table
from apps.logs.statistics_tables.number_balance import user_hold_gold as user_hold_gold_table
from apps.logs.statistics_tables.number_balance import user_hold_stone as user_hold_stone_table

from apps.logs.statistics_tables.active_model import fishing as fishing_table
from apps.logs.statistics_tables.active_model import finger_guess as finger_guess_table
from apps.logs.statistics_tables.active_model import question as question_table
from apps.logs.statistics_tables.active_model import tonic as tonic_table
from apps.logs.statistics_tables.active_model import massage as massage_table

from apps.logs.statistics_tables.monster import create_consume as monster_create_consume_table
from apps.logs.statistics_tables.monster import reset_individual as reset_individual_table

from apps.logs.statistics_tables.equip import create_consume as equip_create_consume_table
from apps.logs.statistics_tables.item import create_consume as item_create_consume_table
from apps.logs.statistics_tables.item import cost_stamina as cost_stamina_table

from apps.logs.statistics_tables.stage import normal_stage_challenge as normal_stage_challenge_table
from apps.logs.statistics_tables.stage import hard_stage_challenge as hard_stage_challenge_table
from apps.logs.statistics_tables.stage import exp_stage_challenge as exp_stage_challenge_table
from apps.logs.statistics_tables.stage import gold_stage_challenge as gold_stage_challenge_table
from apps.logs.statistics_tables.stage import trial_stage_challenge as trial_stage_challenge_table
from apps.logs.statistics_tables.stage import gym_stage_challenge as gym_stage_challenge_table
from apps.logs.statistics_tables.stage import world_boss_stage_challenge as world_boss_stage_challenge_table
from apps.logs.statistics_tables.stage import catch_monster_stage_challenge as catch_monster_stage_challenge_table
from apps.logs.statistics_tables.stage import treasure_battle_stage_challenge as treasure_battle_stage_challenge_table
from apps.game_manager.models.game_manager import *
from django.http import HttpResponse, HttpResponseRedirect
from apps.common.decorators.decorators import require_permission
from apps.utils.logs_out_path_of_server import get_serverid_lst
from apps.logs.statistics_tables.activity import default_get_table

OUTPUT_PATH = _settings.MEDIA_ROOT + '/log_dump/'
OUTPUT_FILE_NAME = "log_module_event"


def _get_server_list(from_date=datetime.date.today(), to_date=datetime.date.today()):
    """
        获取游戏服务器列表
    :rtype : object
    """

    _serverid_lst = get_serverid_lst(from_date, to_date)
    from apps.game_manager.mysql import server_list
    all_server_list = server_list.get_all_server(True)
    return_ser_lst = []
    if -1 in _serverid_lst:
        return_ser_lst.extend([{'id': -1, 'name': u'通服务器'}])
    for item in all_server_list:
        server_id = item['id']
        if server_id in _serverid_lst:
            server_name = item['name'] + '_' + str(item['id'])
            server_dict = {'id': server_id, 'name': server_name}
            return_ser_lst.append(server_dict)
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
    return return_ser_lst, platform_list

def _date_charge(start_date,end_date=0):
    # 判断输出日期是否正正确
    try:
        start_date_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").date()
    except:
        start_date_date = datetime.datetime.now().date()
    try:
        end_date_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").date()
    except:
        end_date_date=start_date_date
    return start_date_date,end_date_date
# --------------------------------------------------产品每日概况------------------------------------------------------

@require_permission
def statistics_total(request):
    """
        统计总表
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:
        head_lst = [
        {'width': 50, 'name': u'时间'},
        {'width': 50, 'name': u'活跃设备数'},
        {'width': 50, 'name': u'活跃角色数'},
        {'width': 50, 'name': u'新增注册设备数'},
        {'width': 50, 'name': u'新增注册用户数'},
        {'width': 50, 'name': u'登陆设备'},
        {'width': 50, 'name': u'登陆角色'},
        {'width': 50, 'name': u'活跃账户数'},
        {'width': 50, 'name': u'新增账户数'},
        {'width': 50, 'name': u'充值人数'},
        {'width': 50, 'name': u'新增充值人数'},
        {'width': 50, 'name': u'充值金额'},
        {'width': 50, 'name': u'新增首充金额'},
        {'width': 50, 'name': u'付费率'},
        {'width': 50, 'name': u'付费arppu'},
        {'width': 50, 'name': u'登录arpu'},
        # {'width': 50, 'name': u'ACU'},
        # {'width': 50, 'name': u'PCU'},
        # {'width': 50, 'name': u'平均在线时长（分）'},
        {'width': 50, 'name': u'人均登入次数'},
    ]
        if request.method == 'POST':
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))

            start_date_date,end_date_date=_date_charge(start_date,end_date)

            # 分表设置显示
            # 总表行
            channel_id =-1
            row_lst = statistics_total_table.get_table(start_date_date, end_date_date, channel_id, server_id)

            server_list, platform_list = _get_server_list('ying', 'fang')

            return render_to_response("log/game_log.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id, 'cur_channel_id': channel_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list('ying', 'fang')
            return render_to_response("log/game_log.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def user_retain(request):
    """
        用户留存
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
        {'width': 50, 'name': u'时间'},
        ]
        for i in xrange(1, 31):
            head_lst.append({'width': 50, 'name': u'%d日留存' % i})
        if request.method == 'POST':
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))

            start_date_date,end_date_date=_date_charge(start_date,end_date)

            # 分表设置显示
            # 总表行
            channel_id =-1
            row_lst = user_retain_table.get_table(start_date_date, end_date_date, channel_id, server_id)

            server_list, platform_list = _get_server_list('ying', 'fang')

            return render_to_response("log/user_retain.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id, 'cur_channel_id': channel_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list('ying', 'fang')
            return render_to_response("log/user_retain.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def online_time(request):
    """
        用户在线时长统计
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'时间'},
            {'width': 50, 'name': u'今日总登录用户数'},
            {'width': 50, 'name': u'当前实时在线'},
            {'width': 50, 'name': u'当日峰值在线'},
            {'width': 50, 'name': u'5分钟以内'},
            {'width': 50, 'name': u'5-10分钟'},
            {'width': 50, 'name': u'10-15分钟'},
            {'width': 50, 'name': u'15-20分钟'},
            {'width': 50, 'name': u'20-25分钟'},
            {'width': 50, 'name': u'25-30分钟'},
            {'width': 50, 'name': u'30-35分钟'},
            {'width': 50, 'name': u'35-40分钟'},
            {'width': 50, 'name': u'40-45分钟'},
            {'width': 50, 'name': u'45-50分钟'},
            {'width': 50, 'name': u'50-55分钟'},
            {'width': 50, 'name': u'55-60分钟'},
            {'width': 50, 'name': u'60-90分钟'},
            {'width': 50, 'name': u'90-120分钟'},
            {'width': 50, 'name': u'120分钟以上'},
        ]

        if request.method == 'POST':
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            start_date_date,end_date_date=_date_charge(start_date,end_date)

            # 跟日志分析类赋值



            # 分表设置显示
            # 总表行
            channel_id =-1
            row_lst = online_time_table.get_table(start_date_date, end_date_date, channel_id, server_id)

            server_list, platform_list = _get_server_list(start_date_date, end_date_date)

            return render_to_response("log/online_time.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id, 'cur_channel_id': channel_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/online_time.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def amount_analyse(request):
    """
        刷量分析
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'单设备对应账号数'},
            {'width': 50, 'name': u'占比'},
            {'width': 50, 'name': u'单ip对应设备数'},
            {'width': 50, 'name': u'占比'},
        ]

        if request.method == 'POST':
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            start_date_date,end_date_date=_date_charge(start_date,end_date)

            # 跟日志分析类赋值


            # 分表设置显示
            # 总表行
            channel_id =-1
            row_lst = amount_analyse_table.get_table(start_date_date, end_date_date, channel_id, server_id)

            server_list, platform_list = _get_server_list(None, None)

            return render_to_response("log/game_log_amount_analyse.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id, 'cur_channel_id': channel_id}, RequestContext(request))

        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/game_log_amount_analyse.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def online_time_user_num(request):
    """
        用户在线数据
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'时间'},
            {'width': 50, 'name': u'人数'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            start_date_date,end_date_date=_date_charge(start_date,end_date)

            # 分表设置显示
            # 总表行
            channel_id =-1
            row_lst = online_time_user_num_table.get_table(start_date_date, end_date_date, channel_id, server_id)

            server_list, platform_list = _get_server_list(None, None)

            return render_to_response("log/game_log_online_time_user_num.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id, 'cur_channel_id': channel_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/game_log_online_time_user_num.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

# ---------------------------------------------------玩家付费分析---------------------------------------------------

@require_permission
def payment_point_analyse(request):
    """
        付费点分析
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'档位'},
            {'width': 50, 'name': u'充值金额'},
            {'width': 50, 'name': u'人数'},
            {'width': 50, 'name': u'次数'},
            {'width': 50, 'name': u'金额占比'},
            {'width': 50, 'name': u'人数占比'},
            {'width': 50, 'name': u'次数占比'},
        ]
        if request.method == 'POST':
            register_start = request.POST.get("register_start_date")
            register_end = request.POST.get("register_end_date")
            start_date = request.POST.get("search_start_date")
            end_date = request.POST.get("search_end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            now_date = datetime.date.today()

            start_date_date,end_date_date=_date_charge(start_date,end_date)
            register_start_date = None
            register_end_date = None
            if register_start:
                register_start_date = datetime.datetime.strptime(register_start, "%m/%d/%Y").date()
            if register_end:
                register_end_date = datetime.datetime.strptime(register_end, "%m/%d/%Y").date()


            # 分表设置显示
            channel_id =-1
            row_lst = payment_point_analyse_table.get_table(start_date_date, end_date_date, register_start_date, register_end_date, channel_id, server_id)

            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/payment_point_analyse.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'register_start_date': register_start, 'register_end_date': register_end, 'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id, 'cur_channel_id': channel_id}, RequestContext(request))

        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            register_start = now_date_str
            register_end = now_date_str
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/payment_point_analyse.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'register_start_date': register_start, 'register_end_date': register_end, 'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def payment_level_analyse(request):
    """
        各等级充值情况
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'等级'},
            {'width': 50, 'name': u'停留人数'},
            {'width': 50, 'name': u'留存人数'},
            {'width': 50, 'name': u'流失人数'},
            {'width': 50, 'name': u'到达人数'},
            {'width': 50, 'name': u'充值金额'},
            {'width': 50, 'name': u'充值次数'},
            {'width': 50, 'name': u'充值人数'},
            {'width': 50, 'name': u'等级付费率'},
            {'width': 50, 'name': u'等级流失率'},
        ]
        if request.method == 'POST':
            register_start = request.POST.get("register_start_date")
            register_end = request.POST.get("register_end_date")
            start_date = request.POST.get("search_start_date")
            end_date = request.POST.get("search_end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))

            #end_date_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").date()
            start_date_date, end_date_date = _date_charge(start_date, end_date)
            register_start_date = None
            register_end_date = None
            if register_start:
                register_start_date = datetime.datetime.strptime(register_start, "%m/%d/%Y").date()
            if register_end:
                register_end_date = datetime.datetime.strptime(register_end, "%m/%d/%Y").date()

            # 分表设置显示
            channel_id =-1
            row_lst = payment_level_analyse_table.get_table(start_date_date, end_date_date, register_start_date, register_end_date, channel_id, server_id=server_id)

            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/game_log_payment_level_analyse.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'register_start_date': register_start, 'register_end_date': register_end,  'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id, 'cur_channel_id': channel_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            register_start = now_date_str
            register_end = now_date_str
            search_start = now_date_str
            search_end = now_date_str
            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/game_log_payment_level_analyse.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'register_start_date': register_start, 'register_end_date': register_end, 'search_start_date': search_start, 'search_end_date': search_end, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def player_first_recharge_level(request):
    """
        角色首次充值等级
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'等级'},
            {'width': 50, 'name': u'首次充值人数'},
            {'width': 50, 'name': u'首次充值金额'},
            {'width': 50, 'name': u'总体充值人数'},
            {'width': 50, 'name': u'总体充值金额'},
            {'width': 50, 'name': u'首次金额占比'},
            {'width': 50, 'name': u'首次人数占比'},
        ]
        if request.method == 'POST':
            end_date = request.POST.get("end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            now_date = datetime.date.today()
            start_date_date,end_date_date=_date_charge(0,end_date)

            # 跟日志分析类赋值


            # 分表设置显示
            channel_id =-1
            row_lst = player_first_recharge_level_table.get_table(end_date_date, channel_id, server_id)

            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/player_first_recharge_level.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id, 'cur_channel_id': channel_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            end_date = now_date_str
            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/player_first_recharge_level.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def recharge_cycle(request):
    """
        充值周期
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'天数'},
            {'width': 50, 'name': u'首次充值人数'},
            {'width': 50, 'name': u'首次充值金额'},
            {'width': 50, 'name': u'总体充值人数'},
            {'width': 50, 'name': u'总体充值金额'},
            {'width': 50, 'name': u'首次金额占比'},
            {'width': 50, 'name': u'首次人数占比'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            start_date_date,end_date_date=_date_charge(start_date,end_date)

            # 分表设置显示
            channel_id =-1
            row_lst = recharge_cycle_table.get_table(start_date_date, end_date_date, channel_id, server_id)

            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/recharge_cycle.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id, 'cur_channel_id': channel_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/recharge_cycle.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def new_k_days_income(request):
    """
        新增K日收益统计
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'日期'},
            {'width': 50, 'name': u'新增设备'},
            {'width': 50, 'name': u'第1天'},
            {'width': 50, 'name': u'第2天'},
            {'width': 50, 'name': u'第3天'},
            {'width': 50, 'name': u'第4天'},
            {'width': 50, 'name': u'第5天'},
            {'width': 50, 'name': u'第6天'},
            {'width': 50, 'name': u'第7天'},
            {'width': 50, 'name': u'第8~15日'},
            {'width': 50, 'name': u'第16~30日'},
            {'width': 50, 'name': u'30日以上'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            start_date_date,end_date_date=_date_charge(start_date,end_date)



            # 分表设置显示

            row_lst = new_k_days_income_table.get_table(start_date_date, end_date_date, server_id=server_id)
            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/new_k_days_income.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/new_k_days_income.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def user_life_time_value(request):
    """
        用户终身价值
    """

    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    head_lst = [
        {'width': 50, 'name': u'日期'},
        {'width': 50, 'name': u'新增登录用户'},
        {'width': 50, 'name': u'LTV-1'},
        {'width': 50, 'name': u'LTV-2'},
        {'width': 50, 'name': u'LTV-3'},
        {'width': 50, 'name': u'LTV-4'},
        {'width': 50, 'name': u'LTV-5'},
        {'width': 50, 'name': u'LTV-6'},
        {'width': 50, 'name': u'LTV-7'},
        {'width': 50, 'name': u'LTV-8'},
        {'width': 50, 'name': u'LTV-9'},
        {'width': 50, 'name': u'LTV-10'},
        {'width': 50, 'name': u'LTV-15'},
        {'width': 50, 'name': u'LTV-30'},
        {'width': 50, 'name': u'LTV-60'},

    ]
    if request.method == 'POST':
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        server_id = int(request.POST.get("server_id"))
        start_date_date,end_date_date=_date_charge(start_date,end_date)

        # 分表设置显示
        channel_id =-1
        row_lst = user_life_time_value_table.get_table(start_date_date, end_date_date, channel_id, server_id)

        server_list, platform_list = _get_server_list(None, None)
        return render_to_response("log/user_life_time_value.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id, 'cur_channel_id': channel_id}, RequestContext(request))
    else:
        row_lst = []
        now_date_str = datetime.date.today().strftime("%m/%d/%Y")
        start_date = now_date_str
        end_date = now_date_str
        server_list, platform_list = _get_server_list(None, None)
        return render_to_response("log/user_life_time_value.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))

# -----------------------------------------------------用户统计-----------------------------------------------

@require_permission
def vip_distributed(request):
    """
        vip分布
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'日期'},
            {'width': 50, 'name': u'条件'},
            {'width': 50, 'name': u'首冲'},
            {'width': 50, 'name': u'月卡'},
            {'width': 50, 'name': u'vip0'},
            {'width': 50, 'name': u'vip1'},
            {'width': 50, 'name': u'vip2'},
            {'width': 50, 'name': u'vip3'},
            {'width': 50, 'name': u'vip4'},
            {'width': 50, 'name': u'vip5'},
            {'width': 50, 'name': u'vip6'},
            {'width': 50, 'name': u'vip7'},
            {'width': 50, 'name': u'vip8'},
            {'width': 50, 'name': u'vip9'},
            {'width': 50, 'name': u'vip10'},
            {'width': 50, 'name': u'vip11'},
            {'width': 50, 'name': u'vip12'},
        ]
        if request.method == 'POST':
            register_start_date = request.POST.get("register_start_date")
            register_end_date = request.POST.get("register_end_date")
            search_start_date = request.POST.get("search_start_date")
            search_end_date = request.POST.get("search_end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))

            register_start = None
            register_end = None
            if register_start_date:
                register_start = datetime.datetime.strptime(register_start_date, "%m/%d/%Y").date()
            if register_end_date:
                register_end = datetime.datetime.strptime(register_end_date, "%m/%d/%Y").date()

            search_start = datetime.datetime.strptime(search_start_date, "%m/%d/%Y").date()
            search_end = datetime.datetime.strptime(search_end_date, "%m/%d/%Y").date()

            # 分表设置显示
            row_lst = vip_distributed_table.get_table(search_start, search_end, server_id, register_start, register_end)

            server_list, platform_list = _get_server_list(search_start, search_end)
            return render_to_response("log/vip_distributed.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'register_start_date': register_start_date, 'register_end_date': register_end_date, 'search_start_date': search_start_date, 'search_end_date':search_end_date, 'server_list': server_list, 'cur_server_id': server_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            register_start_date = now_date_str
            register_end_date = now_date_str
            search_start_date = now_date_str
            search_end_date = now_date_str
            server_list, platform_list= _get_server_list()
            return render_to_response("log/vip_distributed.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'register_start_date': register_start_date, 'register_end_date': register_end_date, 'search_start_date': search_start_date, 'search_end_date':search_end_date, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def user_first_recharge(request):
    """
        玩家首冲情况
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'日期'},
            {'width': 50, 'name': u'月卡人数'},
            {'width': 50, 'name': u'6元人数'},
            {'width': 50, 'name': u'50元人数'},
            {'width': 50, 'name': u'100元人数'},
            {'width': 50, 'name': u'200元人数'},
            {'width': 50, 'name': u'300元人数'},
            {'width': 50, 'name': u'648元人数'},
            {'width': 50, 'name': u'1998元人数'},
        ]

        if request.method == 'POST':
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            start_date_date,end_date_date=_date_charge(start_date,end_date)
            channel_id = -1

            # 分表设置显示
            row_lst = user_first_recharge_table.get_table(start_date_date, end_date_date, channel_id, server_id)

            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/user_first_recharge.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id, 'cur_channel_id': channel_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/user_first_recharge.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def user_recharge_state(request):
    """
        玩家充值情况
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'日期'},
            {'width': 50, 'name': u'月卡人数'},
            {'width': 50, 'name': u'6元人数'},
            {'width': 50, 'name': u'50元人数'},
            {'width': 50, 'name': u'100元人数'},
            {'width': 50, 'name': u'200元人数'},
            {'width': 50, 'name': u'300元人数'},
            {'width': 50, 'name': u'648元人数'},
            {'width': 50, 'name': u'1998元人数'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            start_date_date,end_date_date=_date_charge(start_date,end_date)
            channel_id = -1
            # 分表设置显示
            row_lst = user_recharge_state_table.get_table(start_date_date, end_date_date, channel_id, server_id)

            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/user_recharge_state.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id, 'cur_channel_id': channel_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/user_recharge_state.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')
# ---------------------------------------------------流失分析-------------------------------------------------

@require_permission
def newbie_state(request):
    """
        新手完成度
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'新手引导编号'},
            {'width': 50, 'name': u'名称'},
            {'width': 50, 'name': u'完成人数'},
        ]
        if request.method == 'POST':
            end_date = request.POST.get("end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            start_date_date,end_date_date=_date_charge(0,end_date)# 跟日志分析类赋值

            # 分表设置显示
            channel_id =-1
            row_lst = newbie_state_table.get_table(end_date_date, channel_id, cur_server=server_id)

            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/newbie_state.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'end_date': end_date, 'channel_list': platform_list, 'cur_channel_id': channel_id, 'server_list': server_list, 'cur_server_id': server_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            end_date = now_date_str
            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/newbie_state.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def guide_state(request):
    """
        新手引导完成度
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'日期'},
            {'width': 50, 'name': u'引导编号'},
            {'width': 50, 'name': u'名称'},
            {'width': 50, 'name': u'完成人数'},
        ]
        if request.method == 'POST':
            end_date = request.POST.get("end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            start_date_date,end_date_date=_date_charge(0,end_date)# 跟日志分析类赋值

            # 分表设置显示
            channel_id =-1
            row_lst = guide_state_table.get_table(end_date_date, channel_id, cur_server=server_id)

            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/guide_state.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'end_date': end_date, 'channel_list': platform_list, 'cur_channel_id': channel_id, 'server_list': server_list, 'cur_server_id': server_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            end_date = now_date_str
            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/guide_state.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def user_level_lost_state(request):
    """
        整体用户等级流失情况
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'等级'},
            {'width': 50, 'name': u'停留人数'},
            {'width': 50, 'name': u'留存人数'},
            {'width': 50, 'name': u'流失人数'},
            {'width': 50, 'name': u'到达人数'},
            {'width': 50, 'name': u'等级流失率'},
        ]
        print("user_level_lost_state")
        if request.method == 'POST':
            register_start = request.POST.get("register_start_date")
            register_end = request.POST.get("register_end_date")
            # start_date = request.POST.get("search_start_date")
            end_date = request.POST.get("search_end_date")
            server_id = int(request.POST.get("server_id"))

            end_date_date, start_date_date = _date_charge(end_date)

            register_start_date = None
            if register_start:
                register_start_date = datetime.datetime.strptime(register_start, "%m/%d/%Y").date()
            register_end_date = None
            if register_end:
                register_end_date = datetime.datetime.strptime(register_end, "%m/%d/%Y").date()

            # 分表设置显示
            row_lst = user_level_lost_state_table.get_table(end_date_date, register_start_date, register_end_date, server_id)

            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/user_level_lost_state.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'register_start_date': register_start, 'register_end_date': register_end, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id}, RequestContext(request))

        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            register_start = now_date_str
            register_end = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/user_level_lost_state.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'register_start_date': register_start, 'register_end_date': register_end, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def user_level_state(request):
    """
        每日玩家等级表现
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        if request.method == 'POST':
            register_start_date = request.POST.get("register_start_date")
            register_end_date = request.POST.get("register_end_date")
            start_date = request.POST.get("search_start_date")
            end_date = request.POST.get("search_end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            player_min_lv = int(request.POST.get("min_lv"))
            player_max_lv = int(request.POST.get("max_lv"))

            head_lst = [
                {'width': 50, 'name': u'时间'},
                {'width': 50, 'name': u'总用户数'},
                {'width': 50, 'name': u'登陆用户数'},
                {'width': 50, 'name': u'新增用户数'},
            ]
            for i in xrange(player_min_lv, player_max_lv + 1):
                head_lst.append({'width': 50, 'name': u'%d' % i})

            start_date_date,end_date_date=_date_charge(start_date,end_date)

            register_start = None
            register_end = None
            if register_start_date:
                register_start = datetime.datetime.strptime(register_start_date, "%m/%d/%Y").date()
            if register_end_date:
                register_end = datetime.datetime.strptime(register_end_date, "%m/%d/%Y").date()

            # 分表设置显示
            row_lst = user_level_state_table.get_table(start_date_date, end_date_date, player_min_lv, player_max_lv, register_start, register_end, cur_server=server_id)
            server_list, platform_list = _get_server_list(start_date_date, end_date_date)

            return render_to_response("log/user_level_state.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'cur_server_id': server_id, 'row_lst': row_lst,'head_lst': head_lst,  'search_start_date': start_date, 'search_end_date': end_date, 'max_lv':player_max_lv, 'min_lv': player_min_lv, 'register_start_date': register_start_date, 'register_end_date': register_end_date}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")

            start_date = now_date_str
            end_date = now_date_str
            register_start = now_date_str
            register_end = now_date_str

            head_lst = [
                {'width': 50, 'name': u'时间'},
                {'width': 50, 'name': u'登陆用户数'},
                {'width': 50, 'name': u'新增用户数'},
            ]
            for i in xrange(1, 20 + 1):
                head_lst.append({'width': 50, 'name': u'%d' % i})

            server_list, platform_list = _get_server_list()
            return render_to_response("log/user_level_state.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date, 'max_lv':21, 'min_lv':1, 'register_start_date': register_start, 'register_end_date': register_end}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def user_structure(request):
    """
        用户构成
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'日期'},
            {'width': 50, 'name': u'登录用户'},
            {'width': 50, 'name': u'活跃用户'},
            {'width': 50, 'name': u'用户流失'},
            {'width': 50, 'name': u'回流用户'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))

            start_date_date,end_date_date=_date_charge(start_date,end_date)

            # 分表设置显示
            channel_id =-1
            row_lst = user_structure_table.get_table(start_date_date, end_date_date, channel_id, server_id)

            server_list, platform_list = _get_server_list(None, None)

            return render_to_response("log/user_structure.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id, 'cur_channel_id': channel_id}, RequestContext(request))

        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/user_structure.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'start_date': start_date, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def user_life_cycle(request):
    """
        生命周期
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
        {'width': 50, 'name': u'日期'},
        {'width': 50, 'name': u'次日流失'},
        {'width': 50, 'name': u'2-3日流失'},
        {'width': 50, 'name': u'4-7日流失'},
        {'width': 50, 'name': u'8-14日流失'},
        {'width': 50, 'name': u'15-30日流失'},
        {'width': 50, 'name': u'31-90日流失'},
        {'width': 50, 'name': u'90-180日流失'},
        {'width': 50, 'name': u'181-1日流失'},
        {'width': 50, 'name': u'1年+'},
    ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            end_date = request.POST.get("search_end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            start_date_date,end_date_date=_date_charge(start_date,end_date)



            # 分表设置显示
            channel_id =-1
            row_lst = user_life_cycle_table.get_table(start_date_date, end_date_date,  channel_id, server_id)

            server_list, platform_list = _get_server_list(None, None)

            return render_to_response("log/user_life_cycle.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id, 'cur_channel_id': channel_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/user_life_cycle.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

# --------------------------------------------------首日体验------------------------------------------------------
@require_permission
def user_first_play_level(request):
    """
        用户首日等级留存
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'等级'},
            {'width': 50, 'name': u'人数'},
            {'width': 50, 'name': u'等级比率'},
            {'width': 50, 'name': u'次日留存率'},
        ]
        if request.method == 'POST':
            end_date = request.POST.get("end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            start_date_date,end_date_date=_date_charge(0,end_date)

            # 分表设置显示
            channel_id =-1
            #todo:(search_date,dir_name,file_name,server_id):
            row_lst = default_get_table.get_table(end_date_date,'tables','USER_FIRST_DAY_KEEP_PLAY',server_id)

            server_list, platform_list = _get_server_list()
            return render_to_response("log/user_first_play_level.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id, 'cur_channel_id': channel_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            end_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/user_first_play_level.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def first_play_time(request):
    """
        首次游戏时长
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'游戏时长'},
            {'width': 50, 'name': u'人数'},
            {'width': 50, 'name': u'占比'},
        ]
        if request.method == 'POST':
            end_date = request.POST.get("end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            start_date_date,end_date_date=_date_charge(0,end_date)

            # 分表设置显示
            channel_id =-1
            row_lst = first_play_time_table.get_table(end_date_date, channel_id, server_id)

            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/first_play_time.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id, 'cur_channel_id': channel_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            end_date = now_date_str
            server_list, platform_list = _get_server_list(None, None)
            return render_to_response("log/first_play_time.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')
# -------------------------------------------------消费点分析------------------------------------------------------
@require_permission
def user_first_cost_stone(request):
    """
        用户首次消费点分析——钻石
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        stone_head_lst = [
            {'width': 50, 'name': u'消费点'},
            {'width': 50, 'name': u'钻石数 '},
            {'width': 50, 'name': u'人数'},
            {'width': 50, 'name': u'人数比率'},
            {'width': 50, 'name': u'钻石比率'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("start_date")
            start_date_date,end_date_date=_date_charge(start_date)
            server_id = int(request.POST.get("server_id"))
            # 分表设置显示
            stone_row_lst = user_first_cost_stone_table.get_cost_stone_table(start_date_date, server_id)
            server_list, platform_list = _get_server_list(start_date_date, start_date_date)
            return render_to_response("log/user_first_cost_stone.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'cur_server_id': server_id,'stone_row_lst': stone_row_lst,'stone_head_lst': stone_head_lst, 'start_date': start_date}, RequestContext(request))
        else:
            stone_row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/user_first_cost_stone.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'stone_row_lst': stone_row_lst,'stone_head_lst': stone_head_lst, 'start_date': start_date}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def user_first_cost_gold(request):
    """
        用户首次消费点分析——金币
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        gold_head_lst = [
            {'width': 50, 'name': u'消费点'},
            {'width': 50, 'name': u'金币数 '},
            {'width': 50, 'name': u'人数'},
            {'width': 50, 'name': u'人数比率'},
            {'width': 50, 'name': u'金币比率'},
        ]

        if request.method == 'POST':
            start_date = request.POST.get("start_date")
            start_date_date,end_date_date=_date_charge(start_date)
            server_id = int(request.POST.get("server_id"))
            # 分表设置显示
            gold_row_lst = user_first_cost_stone_table.get_cost_gold_table(start_date_date, server_id)
            server_list, platform_list = _get_server_list(start_date_date, start_date_date)
            return render_to_response("log/user_first_cost_gold.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'cur_server_id': server_id,'gold_row_lst': gold_row_lst,'gold_head_lst':gold_head_lst, 'start_date': start_date}, RequestContext(request))
        else:
            gold_row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/user_first_cost_gold.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'gold_row_lst': gold_row_lst,'gold_head_lst':gold_head_lst, 'start_date': start_date}, RequestContext(request))

    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def daily_consume_distributed_stone(request):
    """
        日常钻石消费点分布
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'消费点'},
            {'width': 50, 'name': u'钻石数'},
            {'width': 50, 'name': u'人数'},
            {'width': 50, 'name': u'次数'},
            {'width': 50, 'name': u'参与率'},
            {'width': 50, 'name': u'钻石消耗占比'},
            {'width': 50, 'name': u'人数占比'},
        ]

        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            start_date_date,end_date_date=_date_charge(start_date)
            server_id = int(request.POST.get("server_id"))

            # 分表设置显示
            row_lst = daily_consume_distributed_table.get_cost_stone_table(start_date_date, server_id)

            server_list, platform_list = _get_server_list(start_date_date, start_date_date)
            return render_to_response("log/daily_consume_distributed_stone.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'cur_server_id': server_id,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date}, RequestContext(request))

        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/daily_consume_distributed_stone.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date}, RequestContext(request))

    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def daily_consume_distributed_gold(request):
    """
        日常金币消费点分布
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'消费点'},
            {'width': 50, 'name': u'金币数'},
            {'width': 50, 'name': u'人数'},
            {'width': 50, 'name': u'次数'},
            {'width': 50, 'name': u'参与率'},
            {'width': 50, 'name': u'金币消耗占比'},
            {'width': 50, 'name': u'人数占比'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            start_date_date,end_date_date=_date_charge(start_date)
            server_id = int(request.POST.get("server_id"))
            # 分表设置显示
            row_lst = daily_consume_distributed_table.get_cost_gold_table(start_date_date, server_id)
            server_list, platform_list = _get_server_list(start_date_date, start_date_date)
            return render_to_response("log/daily_consume_distributed_gold.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'cur_server_id': server_id,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date}, RequestContext(request))

        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/daily_consume_distributed_gold.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'row_lst': row_lst,'head_lst': head_lst,'search_start_date': start_date}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def user_level_consume_stone_state(request):
    """
        钻石等级消耗
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'等级'},
            {'width': 50, 'name': u'消耗人数'},
            {'width': 50, 'name': u'消耗数量'},
            {'width': 50, 'name': u'到达人数'},
            {'width': 50, 'name': u'等级消耗ARPPU'},
            {'width': 50, 'name': u'等级消耗率'},
        ]

        if request.method == 'POST':
            # register_start = request.POST.get("register_start_date")
            # register_end = request.POST.get("register_end_date")
            start_date = request.POST.get("search_start_date")
            # end_date = request.POST.get("search_end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            start_date_date,end_date_date=_date_charge(start_date)
            # end_date_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").date()
            #
            # register_start_date = None
            # if register_start:
            #     register_start_date = datetime.datetime.strptime(register_start, "%m/%d/%Y").date()
            # register_end_date = None
            # if register_end:
            #     register_end_date = datetime.datetime.strptime(register_end, "%m/%d/%Y").date()

            # 分表设置显示
            row_lst = user_level_consume_stone_state_table.get_table(start_date_date, server_id)
            # print(row_lst)
            server_list, platform_list = _get_server_list(start_date_date,start_date_date)
            return render_to_response("log/user_level_consume_stone_state.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'cur_server_id': server_id,'row_lst': row_lst,'head_lst': head_lst,  'search_start_date': start_date}, RequestContext(request))

        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            register_start = now_date_str
            register_end = now_date_str
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/user_level_consume_stone_state.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'row_lst': row_lst,'head_lst': head_lst, 'register_start_date': register_start, 'register_end_date': register_end, 'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, }, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def user_level_consume_gold_state(request):
    """
        金币等级消耗
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'等级'},
            {'width': 50, 'name': u'消耗人数'},
            {'width': 50, 'name': u'消耗数量'},
            {'width': 50, 'name': u'到达人数'},
            {'width': 50, 'name': u'等级消耗ARPPU'},
            {'width': 50, 'name': u'等级消耗率'},
        ]

        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            start_date_date,end_date_date=_date_charge(start_date)
            server_id = int(request.POST.get("server_id"))
            # 分表设置显示
            row_lst = user_level_consume_gold_state_table.get_table(start_date_date, server_id)
            server_list, platform_list = _get_server_list(start_date_date, start_date_date)
            return render_to_response("log/user_level_consume_gold_state.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'cur_server_id': server_id,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date, }, RequestContext(request))

        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            register_start = now_date_str
            register_end = now_date_str
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/user_level_consume_gold_state.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'register_start_date': register_start, 'register_end_date': register_end, 'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def user_stone_shop(request):
    """
        钻石商城物品购买
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'购买物品'},
            {'width': 50, 'name': u'钻石数'},
            {'width': 50, 'name': u'人数'},
            {'width': 50, 'name': u'次数'},
            {'width': 50, 'name': u'人数占比'},
            {'width': 50, 'name': u'钻石消耗占比'},
        ]
        if request.method == 'POST':
            register_start = request.POST.get("register_start_date")
            register_end = request.POST.get("register_end_date")
            start_date = request.POST.get("search_start_date")
            end_date = request.POST.get("search_end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))

            start_date_date,end_date_date=_date_charge(start_date,end_date)

            end_date_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").date()

            register_start_date = None
            if register_start:
                register_start_date = datetime.datetime.strptime(register_start, "%m/%d/%Y").date()
            register_end_date = None
            if register_end:
                register_end_date = datetime.datetime.strptime(register_end, "%m/%d/%Y").date()



            # 分表设置显示
            row_lst = user_stone_shop_table.get_table(start_date_date, end_date_date, register_start_date, register_end_date,server_id)
            server_list, platform_list = _get_server_list(start_date_date, end_date_date)
            return render_to_response("log/user_stone_shop.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'register_start_date': register_start, 'register_end_date': register_end, 'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id}, RequestContext(request))

        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            register_start = now_date_str
            register_end = now_date_str
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/user_stone_shop.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'register_start_date': register_start, 'register_end_date': register_end, 'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

# --------------------------------------------------数值平衡------------------------------------------------------
@require_permission
def user_generate_gold(request):
    """
        金币产出
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'事件'},
            {'width': 50, 'name': u'数量'},
            {'width': 50, 'name': u'比率'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            start_date_date,end_date_date=_date_charge(start_date)
            server_id = int(request.POST.get("server_id"))

            # 分表设置显示
            row_lst = user_generate_gold_table.get_table(start_date_date, server_id)
            server_list, platform_list = _get_server_list(start_date_date, start_date_date)
            return render_to_response("log/user_generate_gold.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'cur_server_id': server_id, 'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/user_generate_gold.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def user_generate_stone(request):
    """
        钻石产出
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'事件'},
            {'width': 50, 'name': u'数量'},
            {'width': 50, 'name': u'比率'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            start_date_date,end_date_date=_date_charge(start_date)
            server_id = int(request.POST.get("server_id"))

            # 分表设置显示
            row_lst = user_generate_stone_table.get_table(start_date_date, server_id)

            server_list, platform_list = _get_server_list(start_date_date, start_date_date)
            return render_to_response("log/user_generate_stone.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'cur_server_id': server_id,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str

            server_list, platform_list = _get_server_list()
            return render_to_response("log/user_generate_stone.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def user_cost_gold(request):
    """
        金币消耗
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()

    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'事件'},
            {'width': 50, 'name': u'数量'},
            {'width': 50, 'name': u'比率'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            start_date_date,end_date_date=_date_charge(start_date)
            server_id = int(request.POST.get("server_id"))
            # 分表设置显示
            row_lst = user_cost_gold_table.get_table(start_date_date, server_id)

            server_list, platform_list = _get_server_list(start_date_date, start_date_date)
            return render_to_response("log/user_cost_gold.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'cur_server_id': server_id, 'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/user_cost_gold.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def user_cost_stone(request):
    """
        钻石消耗
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'事件'},
            {'width': 50, 'name': u'数量'},
            {'width': 50, 'name': u'比率'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            start_date_date,end_date_date=_date_charge(start_date)
            server_id = int(request.POST.get("server_id"))

            # 分表设置显示
            row_lst = user_cost_stone_table.get_table(start_date_date, server_id)

            server_list, platform_list = _get_server_list(start_date_date, start_date_date)
            return render_to_response("log/user_cost_stone.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'cur_server_id': server_id,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/user_cost_stone.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def user_hold_gold(request):
    """
        玩家金币持有
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'日期'},
            {'width': 50, 'name': u'持有数量'},
            {'width': 50, 'name': u'玩家数量'},
            {'width': 50, 'name': u'活跃玩家总数'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            start_date_date,end_date_date=_date_charge(start_date)
            server_id = int(request.POST.get("server_id"))
            # 分表设置显示
            row_lst = user_hold_gold_table.get_table(start_date_date, server_id)
            server_list, platform_list = _get_server_list(start_date_date, start_date_date)

            return render_to_response("log/user_hold_gold.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'cur_server_id': server_id, 'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/user_hold_gold.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def user_hold_stone(request):
    """
        玩家钻石持有
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'日期'},
            {'width': 50, 'name': u'持有数量'},
            {'width': 50, 'name': u'玩家数量'},
            {'width': 50, 'name': u'活跃玩家总数'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            start_date_date,end_date_date=_date_charge(start_date)
            server_id = int(request.POST.get("server_id"))
            # 分表设置显示
            row_lst = user_hold_stone_table.get_table(start_date_date, server_id)
            server_list, platform_list = _get_server_list(start_date_date, start_date_date)
            return render_to_response("log/user_hold_stone.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'cur_server_id': server_id, 'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/user_hold_stone.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def user_cost_gold_with_vip(request):
    """
        玩家金币消耗(VIP用户)
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'事件名称'},
            {'width': 50, 'name': u'充值用户消耗人数'},
            {'width': 50, 'name': u'充值用户消耗次数'},
            {'width': 50, 'name': u'非充值用户消耗人数'},
            {'width': 50, 'name': u'非充值用户消耗次数'},
            {'width': 50, 'name': u'消耗钻石数量'},
        ]
        for i in xrange(0, 13):
            head_lst.append({'width': 50, 'name': u'VIP%d消耗金额' % i})
            head_lst.append({'width': 50, 'name': u'VIP%d消耗人数' % i})
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            start_date_date,end_date_date=_date_charge(start_date)
            server_id = int(request.POST.get("server_id"))

            # 分表设置显示
            row_lst = user_cost_gold_with_vip_table.get_table(start_date_date, server_id)
            server_list, platform_list = _get_server_list(start_date_date, start_date_date)

            return render_to_response("log/user_cost_gold_with_vip.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'cur_server_id': server_id, 'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/user_cost_gold_with_vip.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def user_cost_stone_with_vip(request):
    """
        玩家钻石消耗(VIP用户)
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'事件名称'},
            {'width': 50, 'name': u'充值用户消耗人数'},
            {'width': 50, 'name': u'充值用户消耗次数'},
            {'width': 50, 'name': u'非充值用户消耗人数'},
            {'width': 50, 'name': u'非充值用户消耗次数'},
            {'width': 50, 'name': u'消耗钻石数量'},
        ]
        for i in xrange(0, 13):
            head_lst.append({'width': 50, 'name': u'VIP%d消耗金额' % i})
            head_lst.append({'width': 50, 'name': u'VIP%d消耗人数' % i})
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            start_date_date,end_date_date=_date_charge(start_date)
            server_id = int(request.POST.get("server_id"))

            # 分表设置显示
            row_lst = user_cost_stone_with_vip_table.get_table(start_date_date, server_id)
            server_list, platform_list = _get_server_list(start_date_date, start_date_date)

            return render_to_response("log/user_cost_stone_with_vip.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'cur_server_id': server_id, 'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            server_list, platform_list = _get_server_list()

            return render_to_response("log/user_cost_stone_with_vip.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list, 'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

# --------------------------------------------------活动模块分析------------------------------------------------------
@require_permission
def fishing(request):
    """
        钓鱼
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'日期'},
            {'width': 50, 'name': u'参与人数'},
            {'width': 50, 'name': u'总钓鱼次数'},
            {'width': 50, 'name': u'到达要求人数'},
            {'width': 50, 'name': u'参与率'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            end_date = request.POST.get("search_end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))

            start_date_date,end_date_date=_date_charge(start_date,end_date)

            # 分表设置显示
            row_lst = fishing_table.get_table(start_date_date, end_date_date, cur_server_id=server_id)

            server_list, platform_list = _get_server_list(start_date_date, end_date_date)
            return render_to_response("log/fishing.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/fishing.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def finger_guess(request):
    """
        猜拳
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'日期'},
            {'width': 50, 'name': u'参与人数'},
            {'width': 50, 'name': u'总猜拳次数'},
            {'width': 50, 'name': u'到达要求人数'},
            {'width': 50, 'name': u'参与率'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            end_date = request.POST.get("search_end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            start_date_date,end_date_date=_date_charge(start_date,end_date)

            # 分表设置显示
            row_lst = finger_guess_table.get_table(start_date_date, end_date_date, cur_server_id=server_id)

            server_list, platform_list = _get_server_list(start_date_date, end_date_date)
            return render_to_response("log/finger_guess.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/finger_guess.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def question(request):
    """
        问答
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'日期'},
            {'width': 50, 'name': u'参与人数'},
            {'width': 50, 'name': u'总参与次数'},
            {'width': 50, 'name': u'到达要求人数'},
            {'width': 50, 'name': u'参与率'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            end_date = request.POST.get("search_end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            start_date_date,end_date_date=_date_charge(start_date,end_date)

            # 分表设置显示
            row_lst = question_table.get_table(start_date_date, end_date_date, cur_server_id=server_id)

            server_list, platform_list = _get_server_list(start_date_date, end_date_date)
            return render_to_response("log/question.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/question.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))

    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def tonic(request):
    """
        进补
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'日期'},
            {'width': 50, 'name': u'参与人数'},
            {'width': 50, 'name': u'总参与次数'},
            {'width': 50, 'name': u'到达要求人数'},
            {'width': 50, 'name': u'参与率'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            end_date = request.POST.get("search_end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            start_date_date,end_date_date=_date_charge(start_date,end_date)

            # 分表设置显示
            row_lst = tonic_table.get_table(start_date_date, end_date_date, cur_server_id=server_id)

            server_list, platform_list = _get_server_list(start_date_date, end_date_date)
            return render_to_response("log/tonic.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/tonic.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def massage(request):
    """
        按摩
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'日期'},
            {'width': 50, 'name': u'参与人数'},
            {'width': 50, 'name': u'总参与次数'},
            {'width': 50, 'name': u'到达要求人数'},
            {'width': 50, 'name': u'参与率'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            end_date = request.POST.get("search_end_date")
            # channel_id = int(request.POST.get("channel_id"))
            server_id = int(request.POST.get("server_id"))
            start_date_date,end_date_date=_date_charge(start_date,end_date)

            # 分表设置显示
            row_lst = massage_table.get_table(start_date_date, end_date_date, cur_server_id=server_id)

            server_list, platform_list = _get_server_list(start_date_date, end_date_date)
            return render_to_response("log/massage.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list, 'cur_server_id': server_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/massage.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date, 'channel_list': platform_list, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

# --------------------------------------------------宠物相关统计------------------------------------------------------

@require_permission
def create_monster(request):
    """
        宠物产出统计
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'种类'},
            {'width': 50, 'name': u'星级'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            start_date_date,end_date_date=_date_charge(start_date)
            server_id = int(request.POST.get("server_id"))

            row_lst, head_extend_lst = monster_create_consume_table.get_create_table(start_date_date, start_date_date, server_id)
            # print("row_lst: "+str(row_lst))
            # print("head_extend_lst: "+str(head_extend_lst))
            for head_extend in head_extend_lst:
                head_lst.append({'width': 50, 'name': '%s' % head_extend})

            server_list, platform_list = _get_server_list(start_date_date, start_date_date)
            return render_to_response("log/create_monster.html", {'account':manager.account,'btn_lst':btn_lst,'cur_server_id':server_id,'row_lst': row_lst,'head_lst': head_lst, 'server_list': server_list, 'search_start_date': start_date, 'search_end_date': start_date_date}, RequestContext(request))

        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str

            server_list, platform_list = _get_server_list()
            return render_to_response("log/create_monster.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'server_list': server_list,  'search_start_date': start_date, 'search_end_date': start_date}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def remove_monster(request):
    """
        宠物消耗统计
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'种类'},
            {'width': 50, 'name': u'星级'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            start_date_date,end_date_date=_date_charge(start_date)
            server_id = int(request.POST.get("server_id"))

            # 分表设置显示
            row_lst,head_extend_lst = monster_create_consume_table.get_consume_table(start_date_date, start_date_date, server_id)
            for head_extend in head_extend_lst:
                head_lst.append({'width': 50, 'name': '%s' % head_extend})
            server_list, platform_list = _get_server_list(start_date_date, start_date_date)

            return render_to_response("log/remove_monster.html", {'account':manager.account,'btn_lst':btn_lst,'cur_server_id':server_id,'row_lst': row_lst,'head_lst': head_lst, 'server_list': server_list, 'search_start_date': start_date, 'search_end_date': start_date_date}, RequestContext(request))

        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/remove_monster.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'server_list': server_list, 'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def monster_reset_individual(request):
    """
        宠物洗练统计
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:
        head_lst = [
            {'width': 50, 'name': u'宠物名称'},
            {'width': 50, 'name': u'5次以内'},
        ]
        for i in xrange(5, 100, 5):
            head_lst.append({'width': 50, 'name': u'%d-%d' % (i, i+5)})
        head_lst.append({'width': 50, 'name': u'100次以上'})
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            # end_date = request.POST.get("search_end_date")

            start_date_date,end_date_date=_date_charge(start_date)
            # end_date_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").date()
            server_id = int(request.POST.get("server_id"))

            # 分表设置显示
            row_lst = reset_individual_table.get_table(start_date_date, start_date_date, server_id)
            server_list, platform_list = _get_server_list(start_date_date, start_date_date)
            return render_to_response("log/monster_reset_individual.html", {'account':manager.account,'btn_lst':btn_lst,'cur_server_id':server_id,'row_lst': row_lst,'head_lst': head_lst,'search_start_date': start_date, 'search_end_date': start_date_date, 'server_list': server_list}, RequestContext(request))

        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")

            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/monster_reset_individual.html", {'account':manager.account,'btn_lst':btn_lst,'row_lst': row_lst,'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date, 'server_list': server_list}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

# --------------------------------------------------装备相关统计------------------------------------------------------
def create_equipment(request):
    """
        装备产出统计
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'名称'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            start_date_date,end_date_date=_date_charge(start_date)
            server_id = int(request.POST.get("server_id"))

            row_lst, head_extend_lst = equip_create_consume_table.get_create_table(start_date_date, start_date_date, server_id)
            for head_extend in head_extend_lst:
                head_lst.append({'width': 50, 'name': '%s' % head_extend})

            all_equip_list = _get_equipment_list()
            server_list, platform_list = _get_server_list(start_date_date,start_date_date)

            return render_to_response("log/create_equipment.html", {'account':manager.account,'btn_lst':btn_lst,'cur_server_id':server_id,'server_list': server_list,'row_lst': row_lst,'head_lst': head_lst, 'all_equip_list': all_equip_list, 'search_start_date': start_date, 'search_end_date': start_date_date}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")

            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list()
            all_equip_list = _get_equipment_list()
            return render_to_response("log/create_equipment.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list,'row_lst': row_lst,'head_lst': head_lst, 'all_equip_list': all_equip_list, 'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def consume_equipment(request):
    """
        装备产出统计
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'名称'},
        ]
        if request.method == 'POST':

            start_date = request.POST.get("search_start_date")
            start_date_date,end_date_date=_date_charge(start_date)
            server_id = int(request.POST.get("server_id"))

            row_lst,head_extend_lst = equip_create_consume_table.get_consume_table(start_date_date, start_date_date, server_id)
            for head_extend in head_extend_lst:
                head_lst.append({'width': 50, 'name': '%s' % head_extend})

            all_equip_list = _get_equipment_list()
            server_list, platform_list = _get_server_list(start_date_date,start_date_date)

            return render_to_response("log/consume_equipment.html", {'account':manager.account,'btn_lst':btn_lst,'cur_server_id':server_id,'server_list': server_list,'row_lst': row_lst,'head_lst': head_lst, 'all_equip_list': all_equip_list,  'search_start_date': start_date, 'search_end_date': start_date_date}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")

            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list()

            all_equip_list = _get_equipment_list()
            return render_to_response("log/consume_equipment.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list,'row_lst': row_lst,'head_lst': head_lst, 'all_equip_list': all_equip_list,'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def cost_stamina(request):
    """
        体力消耗
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'日期'},
            {'width': 50, 'name': u'0-120'},
            {'width': 50, 'name': u'120-240'},
            {'width': 50, 'name': u'240-360'},
            {'width': 50, 'name': u'360-480'},
            {'width': 50, 'name': u'480-600'},
            {'width': 50, 'name': u'600-720'},
            {'width': 50, 'name': u'720-840'},
            {'width': 50, 'name': u'840以上'},
        ]
        if request.method == 'POST':

            start_date = request.POST.get("search_start_date")
            end_date = request.POST.get("search_end_date")
            start_date_date,end_date_date=_date_charge(start_date,end_date)
            server_id = int(request.POST.get("server_id"))

            # 分表设置显示
            row_lst = cost_stamina_table.get_table(start_date_date, end_date_date,server_id)
            server_list, platform_list = _get_server_list(start_date_date, end_date_date)

            return render_to_response("log/cost_stamina.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst,  'search_start_date': start_date, 'search_end_date': end_date, 'cur_server_id': server_id}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")

            start_date = now_date_str
            end_date = now_date_str
            server_list, platform_list = _get_server_list()
            return render_to_response("log/cost_stamina.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))

    else:
        return HttpResponseRedirect('/Tyranitar6/login/')
# --------------------------------------------------物品相关统计------------------------------------------------------
@require_permission
def create_item(request):
    """
        物品产出统计
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'名称'},
        ]
        if request.method == 'POST':

            start_date = request.POST.get("search_start_date")
            start_date_date,end_date_date=_date_charge(start_date)
            server_id = int(request.POST.get("server_id"))

            row_lst,head_extend_lst = item_create_consume_table.get_create_table(start_date_date, start_date_date,server_id)
            for head_extend in head_extend_lst:
                head_lst.append({'width': 50, 'name': '%s' % head_extend})

            all_item_list = _get_item_list()
            server_list, platform_list = _get_server_list(start_date_date, start_date_date)

            return render_to_response("log/create_item.html", {'account':manager.account,'btn_lst':btn_lst,'cur_server_id':server_id,'server_list': server_list,'row_lst': row_lst,'head_lst': head_lst, 'all_item_list': all_item_list, 'search_start_date': start_date, 'search_end_date': start_date_date}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")
            start_date = now_date_str
            end_date = now_date_str
            all_item_list = _get_item_list()
            server_list, platform_list = _get_server_list()
            return render_to_response("log/create_item.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list,'row_lst': row_lst,'head_lst': head_lst, 'all_item_list': all_item_list,  'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

@require_permission
def consume_item(request):
    """
        物品消耗统计
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    if btn_lst:

        head_lst = [
            {'width': 50, 'name': u'名称'},
        ]
        if request.method == 'POST':
            start_date = request.POST.get("search_start_date")
            start_date_date,end_date_date=_date_charge(start_date)
            server_id = int(request.POST.get("server_id"))

            row_lst,head_extend_lst = item_create_consume_table.get_consume_table(start_date_date, start_date_date,server_id)
            for head_extend in head_extend_lst:
                head_lst.append({'width': 50, 'name': '%s' % head_extend})

            all_item_list = _get_item_list()
            server_list, platform_list = _get_server_list(start_date_date,start_date_date)

            return render_to_response("log/consume_item.html", {'account':manager.account,'btn_lst':btn_lst,'cur_server_id':server_id,'server_list': server_list,'row_lst': row_lst,'head_lst': head_lst, 'all_item_list': all_item_list, 'search_start_date': start_date, 'search_end_date': start_date_date}, RequestContext(request))
        else:
            row_lst = []
            now_date_str = datetime.date.today().strftime("%m/%d/%Y")

            start_date = now_date_str
            end_date = now_date_str
            all_item_list = _get_item_list()
            server_list, platform_list = _get_server_list()
            return render_to_response("log/consume_item.html", {'account':manager.account,'btn_lst':btn_lst,'server_list': server_list,'row_lst': row_lst,'head_lst': head_lst, 'all_item_list': all_item_list, 'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/login/')

def _get_monster_list():
    """
        获取游戏宠物列表
    """

    from apps.config import game_config
    monster_id_name = game_config.get_monster_config_with_id_name()
    monster_id_name_lst = []
    for (tid, name) in monster_id_name.items():
        content = dict()
        content['tid'] = tid
        content['name'] = name + "_" + str(tid)
        monster_id_name_lst.append(content)
    monster_id_name_lst = sorted(monster_id_name_lst, cmp=lambda x, y: cmp(x['tid'], y['tid']))

    return monster_id_name_lst

def _get_equipment_list():
    """
        获取游戏装备列表
    """

    from apps.config import game_config
    item_id_name, item_id_type = game_config.get_item_config_with_id_name()
    item_tid_name_lst = []
    for (tid, name) in item_id_name.items():
        item_type = item_id_type[tid]
        if item_type == game_define.ITEM_TYPE_EQUIP:
            content = dict()
            content['tid'] = tid
            content['name'] = name
            item_tid_name_lst.append(content)
    item_tid_name_lst = sorted(item_tid_name_lst, cmp=lambda x, y: cmp(x['tid'], y['tid']))

    return item_tid_name_lst

def _get_item_list():
    """
        获取游戏物品列表
    """

    from apps.config import game_config
    item_id_name, item_id_type = game_config.get_item_config_with_id_name()
    item_tid_name_lst = []
    for (tid, name) in item_id_name.items():
        item_type = item_id_type[tid]
        if item_type != game_define.ITEM_TYPE_EQUIP:
            content = dict()
            content['tid'] = tid
            content['name'] = name
            item_tid_name_lst.append(content)
    item_tid_name_lst = sorted(item_tid_name_lst, cmp=lambda x, y: cmp(x['tid'], y['tid']))

    return item_tid_name_lst


# --------------------------------------------------副本进度------------------------------------------------------
@require_permission
def stage_normal(request):
    """
        普通副本
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    head_lst = [
        {'width': 50, 'name': u'日期'},
        {'width': 50, 'name': u'副本名称'},
        {'width': 50, 'name': u'挑战数'},
        {'width': 50, 'name': u'通过数'},
        {'width': 50, 'name': u'扫荡次数'},
        {'width': 50, 'name': u'成功率'},
    ]
    if request.method == 'POST':

        start_date = request.POST.get("search_start_date")
        end_date = request.POST.get("search_end_date")
        start_date_date,end_date_date=_date_charge(start_date,end_date)
        server_id = int(request.POST.get("server_id"))

        # 分表设置显示
        row_lst = normal_stage_challenge_table.get_table(start_date_date, end_date_date, server_id=server_id)
        server_list, platform_list = _get_server_list(start_date_date, end_date_date)
        return render_to_response("log/stage_normal.html", {'btn_lst':btn_lst,'cur_server_id':server_id,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))
    else:
        row_lst = []
        now_date_str = datetime.date.today().strftime("%m/%d/%Y")
        start_date = now_date_str
        end_date = now_date_str
        server_list, platform_list = _get_server_list()
        return render_to_response("log/stage_normal.html", {'btn_lst':btn_lst,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))

@require_permission
def stage_hard(request):
    """
        困难副本
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    head_lst = [
        {'width': 50, 'name': u'日期'},
        {'width': 50, 'name': u'副本名称'},
        {'width': 50, 'name': u'挑战数'},
        {'width': 50, 'name': u'通过数'},
        {'width': 50, 'name': u'扫荡次数'},
        {'width': 50, 'name': u'成功率'},
    ]
    if request.method == 'POST':
        start_date = request.POST.get("search_start_date")
        end_date   = request.POST.get("search_end_date")
        start_date_date,end_date_date=_date_charge(start_date,end_date)
        server_id = int(request.POST.get("server_id"))

        # 分表设置显示
        row_lst = hard_stage_challenge_table.get_table(start_date_date, end_date_date, server_id=server_id)
        server_list, platform_list = _get_server_list(start_date_date, end_date_date)

        return render_to_response("log/stage_hard.html", {'btn_lst':btn_lst,'cur_server_id':server_id,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst,  'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))
    else:
        row_lst = []
        now_date_str = datetime.date.today().strftime("%m/%d/%Y")
        start_date = now_date_str
        end_date = now_date_str
        server_list, platform_list = _get_server_list()
        return render_to_response("log/stage_hard.html", {'btn_lst':btn_lst,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))

@require_permission
def stage_exp(request):
    """
        经验副本
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    head_lst = [
        {'width': 50, 'name': u'日期'},
        {'width': 50, 'name': u'副本名称'},
        {'width': 50, 'name': u'参与人数'},
        {'width': 50, 'name': u'总参与次数'},
        {'width': 50, 'name': u'完成人数'},
        {'width': 50, 'name': u'总完成次数'},
        {'width': 50, 'name': u'到达要求人数'},
        {'width': 50, 'name': u'参与率'},
        {'width': 50, 'name': u'成功率'},

    ]
    if request.method == 'POST':

        start_date = request.POST.get("search_start_date")
        end_date = request.POST.get("search_end_date")
        start_date_date,end_date_date=_date_charge(start_date,end_date)
        server_id = int(request.POST.get("server_id"))

        # 分表设置显示
        row_lst = exp_stage_challenge_table.get_table(start_date_date, end_date_date, server_id=server_id)
        server_list, platform_list = _get_server_list(start_date_date, end_date_date)

        return render_to_response("log/stage_exp.html", {'btn_lst':btn_lst,'cur_server_id':server_id,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))
    else:
        row_lst = []
        now_date_str = datetime.date.today().strftime("%m/%d/%Y")
        start_date = now_date_str
        end_date = now_date_str
        server_list, platform_list = _get_server_list()
        return render_to_response("log/stage_exp.html", {'btn_lst':btn_lst,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))

@require_permission
def stage_gold(request):
    """
        金币副本
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    head_lst = [
        {'width': 50, 'name': u'日期'},
        {'width': 50, 'name': u'副本名称'},
        {'width': 50, 'name': u'参与人数'},
        {'width': 50, 'name': u'总参与次数'},
        {'width': 50, 'name': u'完成人数'},
        {'width': 50, 'name': u'总完成次数'},
        {'width': 50, 'name': u'到达要求人数'},
        {'width': 50, 'name': u'参与率'},
        {'width': 50, 'name': u'成功率'},

    ]
    if request.method == 'POST':

        start_date = request.POST.get("search_start_date")
        end_date = request.POST.get("search_end_date")
        start_date_date,end_date_date=_date_charge(start_date,end_date)

        server_id = int(request.POST.get("server_id"))

        # 分表设置显示
        row_lst = gold_stage_challenge_table.get_table(start_date_date, end_date_date, server_id=server_id)

        server_list, platform_list = _get_server_list(start_date_date, end_date_date)
        return render_to_response("log/stage_gold.html", {'btn_lst':btn_lst,'cur_server_id':server_id,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst,  'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))
        # return render_to_response("log/stage_gold.html", {'btn_lst':btn_lst,'row_lst': row_lst,' head_lst': head_lst,  'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))        #一个空格引起的错误 ！！
    else:
        row_lst = []
        now_date_str = datetime.date.today().strftime("%m/%d/%Y")

        start_date = now_date_str
        end_date = now_date_str

        server_list, platform_list = _get_server_list()
        return render_to_response("log/stage_gold.html", {'btn_lst':btn_lst,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))

@require_permission
def stage_trial(request):
    """
        试炼副本
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    head_lst = [
        {'width': 50, 'name': u'日期'},
        {'width': 50, 'name': u'参与人数'},
        {'width': 50, 'name': u'总参与次数'},
        {'width': 50, 'name': u'完成人数'},
        {'width': 50, 'name': u'总完成次数'},
        {'width': 50, 'name': u'到达要求人数'},
        {'width': 50, 'name': u'参与率'},
        {'width': 50, 'name': u'成功率'},

    ]
    if request.method == 'POST':

        start_date = request.POST.get("search_start_date")
        end_date = request.POST.get("search_end_date")
        start_date_date,end_date_date=_date_charge(start_date,end_date)
        server_id = int(request.POST.get("server_id"))

        # 分表设置显示
        row_lst = trial_stage_challenge_table.get_table(start_date_date, end_date_date,server_id=server_id)

        server_list, platform_list = _get_server_list(start_date_date, end_date_date)
        return render_to_response("log/stage_trial.html", {'btn_lst':btn_lst,'cur_server_id':server_id,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst,  'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))
    else:
        row_lst = []
        now_date_str = datetime.date.today().strftime("%m/%d/%Y")

        start_date = now_date_str
        end_date = now_date_str

        server_list, platform_list = _get_server_list()
        return render_to_response("log/stage_trial.html", {'btn_lst':btn_lst,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))

@require_permission
def stage_gym(request):
    """
        道馆副本
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    head_lst = [
        {'width': 50, 'name': u'日期'},
        {'width': 50, 'name': u'参与人数'},
        {'width': 50, 'name': u'总参与次数'},
        {'width': 50, 'name': u'完成人数'},
        {'width': 50, 'name': u'总完成次数'},
        {'width': 50, 'name': u'到达要求人数'},
        {'width': 50, 'name': u'扫荡次数'},
        {'width': 50, 'name': u'参与率'},
        {'width': 50, 'name': u'成功率'},

    ]
    if request.method == 'POST':

        start_date = request.POST.get("search_start_date")
        end_date = request.POST.get("search_end_date")
        start_date_date,end_date_date=_date_charge(start_date,end_date)
        server_id = int(request.POST.get("server_id"))

        # 分表设置显示
        row_lst = gym_stage_challenge_table.get_table(start_date_date, end_date_date, server_id=server_id)

        server_list, platform_list = _get_server_list(start_date_date, end_date_date)
        return render_to_response("log/stage_gym.html", {'btn_lst':btn_lst,'cur_server_id':server_id,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst,  'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))
    else:
        row_lst = []
        now_date_str = datetime.date.today().strftime("%m/%d/%Y")

        start_date = now_date_str
        end_date = now_date_str
        server_list, platform_list = _get_server_list()
        return render_to_response("log/stage_gym.html", {'btn_lst':btn_lst,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))

@require_permission
def stage_world_boss(request):
    """
        世界BOSS副本
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    head_lst = [
        {'width': 50, 'name': u'日期'},
        {'width': 50, 'name': u'参与人数'},
        {'width': 50, 'name': u'总参与次数'},
        {'width': 50, 'name': u'完成人数'},
        {'width': 50, 'name': u'总完成次数'},
        {'width': 50, 'name': u'到达要求人数'},
        {'width': 50, 'name': u'参与率'},
        {'width': 50, 'name': u'成功率'},
    ]
    if request.method == 'POST':

        start_date = request.POST.get("search_start_date")
        end_date = request.POST.get("search_end_date")
        start_date_date,end_date_date=_date_charge(start_date,end_date)
        server_id = int(request.POST.get("server_id"))

        # 分表设置显示
        row_lst = world_boss_stage_challenge_table.get_table(start_date_date, end_date_date, server_id=server_id)

        server_list, platform_list = _get_server_list(start_date_date, end_date_date)
        return render_to_response("log/stage_world_boss.html", {'btn_lst':btn_lst,'cur_server_id':server_id,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst,  'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))
    else:
        row_lst = []
        now_date_str = datetime.date.today().strftime("%m/%d/%Y")

        start_date = now_date_str
        end_date = now_date_str

        server_list, platform_list = _get_server_list()
        return render_to_response("log/stage_world_boss.html", {'btn_lst':btn_lst,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst,  'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))

@require_permission
def stage_catch_monster(request):
    """
        抓宠副本
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    head_lst = [
        {'width': 50, 'name': u'日期'},
        {'width': 50, 'name': u'参与人数'},
        {'width': 50, 'name': u'总参与次数'},
        {'width': 50, 'name': u'完成人数'},
        {'width': 50, 'name': u'总完成次数'},
        {'width': 50, 'name': u'到达要求人数'},
        {'width': 50, 'name': u'参与率'},
        {'width': 50, 'name': u'成功率'},
    ]
    if request.method == 'POST':

        start_date = request.POST.get("search_start_date")
        end_date = request.POST.get("search_end_date")
        start_date_date,end_date_date=_date_charge(start_date,end_date)

        server_id = int(request.POST.get("server_id"))

        # 分表设置显示
        row_lst = catch_monster_stage_challenge_table.get_table(start_date_date, end_date_date, server_id=server_id)
        server_list, platform_list = _get_server_list(start_date_date, end_date_date)
        return render_to_response("log/stage_catch_monster.html", {'btn_lst':btn_lst,'cur_server_id':server_id,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))
    else:
        row_lst = []
        now_date_str = datetime.date.today().strftime("%m/%d/%Y")
        start_date = now_date_str
        end_date = now_date_str
        server_list, platform_list = _get_server_list()
        return render_to_response("log/stage_catch_monster.html", {'btn_lst':btn_lst,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))

@require_permission
def stage_treasure_battle(request):
    """
        夺宝副本
    """
    manager = GameManager.get_by_request(request)
    btn_lst = manager.check_admin_permission()
    head_lst = [
        {'width': 50, 'name': u'日期'},
        {'width': 50, 'name': u'参与人数'},
        {'width': 50, 'name': u'总参与次数'},
        {'width': 50, 'name': u'完成人数'},
        {'width': 50, 'name': u'总完成次数'},
        {'width': 50, 'name': u'到达要求人数'},
        {'width': 50, 'name': u'参与率'},
        {'width': 50, 'name': u'成功率'},
    ]
    if request.method == 'POST':

        start_date = request.POST.get("search_start_date")
        end_date = request.POST.get("search_end_date")
        start_date_date,end_date_date=_date_charge(start_date,end_date)

        server_id = int(request.POST.get("server_id"))

        # 分表设置显示
        row_lst = treasure_battle_stage_challenge_table.get_table(start_date_date, end_date_date, server_id=server_id)

        server_list, platform_list = _get_server_list(start_date_date, end_date_date)
        return render_to_response("log/stage_treasure_battle.html", {'btn_lst':btn_lst,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst,  'search_start_date': start_date, 'search_end_date': end_date,'cur_server_id':server_id}, RequestContext(request))
    else:
        row_lst = []
        now_date_str = datetime.date.today().strftime("%m/%d/%Y")

        start_date = now_date_str
        end_date = now_date_str
        server_list, platform_list = _get_server_list()
        return render_to_response("log/stage_treasure_battle.html", {'btn_lst':btn_lst,'server_list': server_list,'row_lst': row_lst, 'head_lst': head_lst, 'search_start_date': start_date, 'search_end_date': end_date}, RequestContext(request))

