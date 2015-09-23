# -*- coding:utf-8 -*-


from apps.game_manager.models.game_manager import *

from apps.game_manager.mysql import gift_package
from django.http import HttpResponseRedirect
from django.template import RequestContext

from apps.utils import game_define
from apps.config import game_config
import datetime
from apps.logs.output_action_gm import *


head_lst = [
    {'width': 70, 'name': u'礼包ID'},
    {'width': 50, 'name': u'平台'},
    {'width': 55, 'name': u'服务器列表(空=全部)'},
    {'width': 50, 'name': u'礼包生成时间'},
    {'width': 50, 'name': u'礼包到期时间'},
    {'width': 50, 'name': u'礼包类型名'},
    {'width': 50, 'name': u'物品1'},
    {'width': 50, 'name': u'物品数量1'},
    {'width': 50, 'name': u'物品2'},
    {'width': 50, 'name': u'物品2数量'},
    {'width': 50, 'name': u'物品3'},
    {'width': 50, 'name': u'物品3数量'},
    {'width': 50, 'name': u'金币'},
    {'width': 50, 'name': u'钻石'},
    {'width': 50, 'name': u'操作'},
]
def list_to_string(lst):
    """
        把列表转成字符串 [1,2,3] 转换 1,2,3
    """
    lst_str = map(lambda x: str(x), lst)
    return ','.join(lst_str)

def gift_package_lst(request):
    """
    礼包类型列表
    """
    data = {}
    table_list = []
    all_gift_dict = gift_package.get_all_gift()
    for key, val in all_gift_dict.items():
        temp_content = []
        str_server_lst = list_to_string(val['server_int_lst'])
        temp_content.insert(0,str(val['id']))
        temp_content.insert(1,str(game_define.PLAT_FORM_NAME_DICT[val['platform_id']]))
        temp_content.insert(2,str_server_lst)
        temp_content.insert(3,str(val['time']))
        temp_content.insert(4,str(val['endtime']))
        temp_content.insert(5,str(val['name']))
        item_config = game_config.get_item_config(val['item_id1'])
        if item_config:
            temp_content.insert(6,str(item_config['name']))
        else:
            temp_content.insert(6,str(u''))
        temp_content.insert(7,str(val['item_num1']))

        item_config = game_config.get_item_config(val['item_id2'])
        if item_config:
            temp_content.insert(8,str(item_config['name']))
        else:
            temp_content.insert(8,str(u''))
        temp_content.insert(9,str(val['item_num2']))

        item_config = game_config.get_item_config(val['item_id3'])
        if item_config:
            temp_content.insert(10,str(item_config['name']))
        else:
            temp_content.insert(10,str(u''))
        temp_content.insert(11,str(val['item_num3']))

        temp_content.insert(12,str(val['gold']))
        temp_content.insert(13,str(val['stone']))
        table_list.append(temp_content)
    data['gift_package'] = table_list
    data['head_lst'] = head_lst
    return render_to_response("gift_package/gift_package_lst.html", data, RequestContext(request))

def gift_package_add(request):
    """
    添加礼包类型信息
    """
    data = dict()
    item_id_name, item_id_type = game_config.get_item_config_with_id_name()
    item_tid_name_lst = dict()
    item_tid_name_lst[0] = "无"
    for (tid, name) in item_id_name.items():
        if item_id_type[tid] != game_define.ITEM_TYPE_EQUIP:
            item_tid_name_lst[tid] = name
    data['item_val'] = item_tid_name_lst.items()
    data['platform_val'] = game_define.PLAT_FORM_NAME_DICT.items()
    return render_to_response("gift_package/gift_package_add.html", data,RequestContext(request))

def gift_package_edit(request):
    """
    编辑礼包类型信息
    """
    gift_id = int(request.POST.get("gift_id"))
    gift = gift_package.get_gift(gift_id)

    _gift_dict = dict()
    _gift_dict['id'] = gift['id']
    _gift_dict['platform_id'] = gift['platform_id']
    _gift_dict['endtime'] = str(gift['endtime'].strftime('%m/%d/%Y'))
    _gift_dict['name'] = gift['name']
    _gift_dict['item_id1'] = gift['item_id1']
    _gift_dict['item_num1'] = gift['item_num1']
    _gift_dict['item_id2'] = gift['item_id2']
    _gift_dict['item_num2'] = gift['item_num2']
    _gift_dict['item_id3'] = gift['item_id3']
    _gift_dict['item_num3'] = gift['item_num3']
    _gift_dict['gold'] = gift['gold']
    _gift_dict['stone'] = gift['stone']
    _gift_dict['server_id'] = list_to_string(gift['server_int_lst'])
    item_id_name, item_id_type = game_config.get_item_config_with_id_name()
    item_tid_name_lst = dict()
    item_tid_name_lst[0] = "无"
    for (tid, name) in item_id_name.items():
        if item_id_type[tid] != game_define.ITEM_TYPE_EQUIP:
            item_tid_name_lst[tid] = name
    data = dict()
    data['item_val'] = item_tid_name_lst.items()
    data['platform_val'] = game_define.PLAT_FORM_NAME_DICT.items()
    data['gift'] = _gift_dict
    return render_to_response("gift_package/gift_package_edit.html", data,RequestContext(request))

def gift_package_update(request):
    """
    更新礼包类型
    """
    if request.method == 'POST':
        platform_id = int(request.POST.get('platform_id'))
        endtime = datetime.datetime.strptime(request.POST.get('endtime'),"%m/%d/%Y").date()
        name = str(request.POST.get('name'))
        item_id1 = int(request.POST.get('item_id1'))
        item_num1 = int(request.POST.get('item_num1'))
        item_id2 = int(request.POST.get('item_id2'))
        item_num2 = int(request.POST.get('item_num2'))
        item_id3 = int(request.POST.get('item_id3'))
        item_num3 = int(request.POST.get('item_num3'))
        gold = int(request.POST.get('gold'))
        stone = int(request.POST.get('stone'))
        server_id = str(request.POST.get('server_id'))
        # 获取当前管理员
        manager = GameManager.get_by_request(request)
        if request.POST.get('gift_id'):
            gift_id = int(request.POST.get('gift_id'))
            gift_package.edit(server_id, platform_id, endtime, name,  item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone, gift_id)

            # 操作日志记录
            insert_action_edit_gift(manager, server_id, platform_id, endtime, name,  item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone, gift_id)
        else:
            gift_package.insert(server_id, platform_id, endtime, name,  item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone)

            # 操作日志记录
            insert_action_insert_gift(manager, server_id, platform_id, endtime, name,  item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone)
        return HttpResponseRedirect('/Tyranitar6/server/gift_package_lst/')
    else:
        return render_to_response("gift_package/gift_package_add.html",RequestContext(request))