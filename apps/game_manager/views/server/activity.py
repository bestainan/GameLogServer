# -*- coding:utf-8 -*-


from apps.game_manager.models.game_manager import *
from apps.logs.output_action_gm import *

from apps.game_manager.mysql import activity_list
from django.http import HttpResponseRedirect
from django.template import RequestContext

from apps.utils import game_define
from apps.config import game_config
import datetime
SERVER_HIDDEN_NAME_DICT={
    1: u'隐藏',
    0: u'显示',
}

head_lst = [
    {'width': 70, 'name': u'活动ID'},
    {'width': 50, 'name': u'活动名称'},
    {'width': 50, 'name': u'活动版本号'},
    {'width': 55, 'name': u'服务器列表(空=全部)'},
    {'width': 50, 'name': u'活动开始时间'},
    {'width': 50, 'name': u'活动持续天数'},
    {'width': 50, 'name': u'活动间隔时间'},
    {'width': 50, 'name': u'强制开启状态'},
    {'width': 50, 'name': u'操作'},
]
def list_to_string(lst):
    """
        把列表转成字符串 [1,2,3] 转换 1,2,3
    """
    lst_str = map(lambda x: str(x), lst)
    return ','.join(lst_str)

def activity_lst(request):
    """
    活动列表
    """
    data = {}
    table_list = []

    all_activity_dict = activity_list.get_all_activity(True)
    for key, val in all_activity_dict.items():
        str_server_lst = list_to_string(val['server_int_lst'])
        temp_content = []
        temp_content.insert(0,str(val['activity_id']))
        temp_content.insert(1,str(game_define.ACTIVITY_NAME_DICT[val['activity_id']]))
        temp_content.insert(2,str(val['new']))
        temp_content.insert(3,str_server_lst)
        temp_content.insert(4,val['begin_date'].strftime('%Y-%m-%d'))
        temp_content.insert(5,str(val['time_length']))
        temp_content.insert(6,str(val['time_distance']))
        temp_content.insert(7,game_define.ACTIVITY_STATE_NAME_DICT[val['is_forced_open']])
        table_list.append(temp_content)

    data['activity_info'] = table_list
    data['head_lst'] = head_lst
    return render_to_response("activity/activity_lst.html", data, RequestContext(request))

def activity_edit(request):
    """
    编辑服务器信息
    """
    activity_id = int(request.POST.get("act_id"))
    activity = activity_list.get_activity(activity_id, True)
    _activity_dict = dict()
    _activity_dict['activity_id'] = activity['activity_id']
    _activity_dict['server_id'] = list_to_string(activity['server_int_lst'])
    _activity_dict['begin_time'] = activity['begin_date'].strftime('%m/%d/%Y')
    _activity_dict['time_length'] = activity['time_length']
    _activity_dict['time_distance'] = activity['time_distance']
    _activity_dict['is_forced_open'] = activity['is_forced_open']
    _activity_dict['new'] = activity['new']
    _activity_dict['item_id1'] = activity['item_id1']
    _activity_dict['item_num1'] = activity['item_num1']
    _activity_dict['item_id2'] = activity['item_id2']
    _activity_dict['item_num2'] = activity['item_num2']
    _activity_dict['item_id3'] = activity['item_id3']
    _activity_dict['item_num3'] = activity['item_num3']
    _activity_dict['gold'] = activity['gold']
    _activity_dict['stone'] = activity['stone']
    _activity_dict['free'] = activity['free']
    _activity_dict['exp'] = activity['exp']
    _activity_dict['equip'] = activity['equip']
    _activity_dict['monster'] = activity['monster']
    _activity_dict['star'] = activity['star']
    _activity_dict['discount'] = activity['discount']
    _activity_dict['title'] = activity['title']
    _activity_dict['label'] = activity['label']
    _activity_dict['detail'] = activity['detail']
    _activity_dict['title2'] = activity['title2']
    _activity_dict['label2'] = activity['label2']
    _activity_dict['detail2'] = activity['detail2']

    data = dict()
    data['activity_state_val'] = game_define.ACTIVITY_STATE_NAME_DICT.items()

    item_id_name, item_id_type = game_config.get_item_config_with_id_name()
    equip_tid_name_lst = dict()
    equip_tid_name_lst[0] = "无"
    for (tid, name) in item_id_name.items():
        if item_id_type[tid] == game_define.ITEM_TYPE_EQUIP:
            equip_tid_name_lst[tid] = name
    data['activity_equip_val'] = equip_tid_name_lst.items()

    monster_id_name = game_config.get_monster_config_with_id_name()
    monster_id_name[0] = "无"
    data['activity_monster_val'] = monster_id_name.items()

    item_tid_name_lst = dict()
    item_tid_name_lst[0] = "无"
    for (tid, name) in item_id_name.items():
        if item_id_type[tid] != game_define.ITEM_TYPE_EQUIP:
            item_tid_name_lst[tid] = name
    data['activity_item_val'] = item_tid_name_lst.items()

    data['activity'] = _activity_dict
    return render_to_response("activity/activity_edit.html", data,RequestContext(request))

def activity_update(request):
    """
    更新服务器
    """
    if request.method == 'POST':
        activity_id = int(request.POST.get('act_id'))
        # print('server_id '+str(server_id))
        server_id = str(request.POST.get('server_id'))
        begin_time = datetime.datetime.strptime(request.POST.get('begin_time'),"%m/%d/%Y").date()
        time_length = int(request.POST.get('time_length'))
        time_distance = int(request.POST.get('time_distance'))
        is_forced_open = str(request.POST.get('is_forced_open'))
        new = str(request.POST.get('new'))
        item_id1 = int(request.POST.get('item_id1'))
        item_num1 = int(request.POST.get('item_num1'))
        item_id2 = int(request.POST.get('item_id2'))
        item_num2 = int(request.POST.get('item_num2'))
        item_id3 = int(request.POST.get('item_id3'))
        item_num3 = int(request.POST.get('item_num3'))
        gold = int(request.POST.get('gold'))
        stone = int(request.POST.get('stone'))
        free = int(request.POST.get('free'))
        exp = int(request.POST.get('exp'))
        equip = int(request.POST.get('equip'))
        monster = int(request.POST.get('monster'))
        star = int(request.POST.get('star'))
        discount = int(request.POST.get('discount'))
        title = str(request.POST.get('title'))
        detail = request.POST.get('detail').encode('utf-8')
        label = str(request.POST.get('label'))
        title2 = str(request.POST.get('title2'))
        detail2 = request.POST.get('detail2').encode('utf-8')
        label2 = str(request.POST.get('label2'))

        activity_list.change_activity(activity_id, server_id, begin_time, time_length, time_distance, is_forced_open, new,item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone, free, exp, equip, monster, star, discount, title, detail,label,title2,label2, detail2)

        # 操作日志记录
        manager = GameManager.get_by_request(request)
        insert_action_change_activity(manager, activity_id, server_id, begin_time, time_length, time_distance, is_forced_open, new,item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone, free, exp, equip, monster, star, discount, title, detail,label,title2,label2, detail2)

        return HttpResponseRedirect('/Tyranitar6/server/activity_lst/')
    else:
        return render_to_response("activity/activity_add.html",RequestContext(request))