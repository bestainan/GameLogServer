# -*- coding:utf-8 -*-


from apps.game_manager.models.game_manager import *

from apps.game_manager.mysql import server_notice
from django.http import HttpResponseRedirect
from django.template import RequestContext
from apps.utils import game_define
from apps.game_manager.util import memcache
from apps.utils import server_define
from apps.utils import model_define
from apps.config import game_config
from apps.logs.output_action_gm import *
import datetime

head_lst = [
    {'width': 70, 'name': u'编号(日期_编码 避免重复)'},
    {'width': 55, 'name': u'服务器列表'},
    {'width': 55, 'name': u'目标玩家uid'},
    {'width': 50, 'name': u'邮件内容'},
    {'width': 50, 'name': u'开始日期'},
    {'width': 70, 'name': u'有效日期'},
    {'width': 50, 'name': u'金币'},
    {'width': 50, 'name': u'钻石'},
    {'width': 50, 'name': u'免费抽奖材料'},
    {'width': 50, 'name': u'物品'},
    {'width': 50, 'name': u'物品数量'},
    {'width': 50, 'name': u'宠物'},
    {'width': 50, 'name': u'宠物星级'},
    {'width': 50, 'name': u'操作'},
]

def list_to_string(lst):
    """
        把列表转成字符串 [1,2,3] 转换 1,2,3
    """
    lst_str = map(lambda x: str(x), lst)
    return ','.join(lst_str)

def check_system_expiry(server_notice_box_model):
        """
        检测玩家拥有的系统邮件过期情况
        过期移除
            Return:
                有过期邮件
        """
        select_expiry_mail = lambda mail: mail['expiry_date'] <= datetime.datetime.now()
        expiry_mails = filter(select_expiry_mail, server_notice_box_model['mails'])
        for item in expiry_mails:
            server_notice_box_model['mails'].remove(item)
        return len(expiry_mails) > 0


def system_mail_lst(request):
    """
    广播列表
    """
    data = {}
    table_list = []
    all_background_notice_dict = dict()
    all_cmem_dict = server_define.CMEM_MAP
    for key, val in all_cmem_dict.items():
        cmem_url = str(val)
        if cmem_url:
            server_notice_box_model = memcache.get_cmem_val(cmem_url, model_define.SYSTEM_MAIL_BOX_MODEL)
            if server_notice_box_model:
                memcache.put_cmem_val(cmem_url, model_define.SYSTEM_MAIL_BOX_MODEL, server_notice_box_model)
                print server_notice_box_model
                check_system_expiry(server_notice_box_model)
                notices_lst = server_notice_box_model['mails']
                if notices_lst:
                    for mail_dict in notices_lst:
                        if mail_dict:
                            print mail_dict
                            mail_dict['version'] = mail_dict.get('version',0)
                            if 'send_time' in mail_dict:
                                send_time = mail_dict['send_time']
                                mail_dict['send_time'] = send_time.strftime("%Y-%m-%d %H:%M:%S")
                                if send_time <= datetime.datetime.now():
                                    mail_dict['send_time'] += " (已开始)"
                            else:
                                mail_dict['send_time'] = " 错误 "

                            if 'expiry_date' in mail_dict:
                                expiry_date = mail_dict['expiry_date']
                                mail_dict['expiry_date'] = expiry_date.strftime("%Y-%m-%d %H:%M:%S")
                                if expiry_date <= datetime.datetime.now():
                                    mail_dict['expiry_date'] += " (已开始)"
                            else:
                                mail_dict['expiry_date'] = " 错误 "
                            all_background_notice_dict[mail_dict['version']] = mail_dict

    print("all_background_notice_dict: "+str(all_background_notice_dict))
    for key_uid, value in all_background_notice_dict.items():
        if value:
            temp_content = []
            temp_content.insert(0,str(key_uid))
            temp_content.insert(1,value.get('server_id',''))
            temp_content.insert(2,value['target_user_uid'])
            temp_content.insert(3,str(value['title']))
            temp_content.insert(4,value['send_time'])
            temp_content.insert(5,value['expiry_date'])
            temp_content.insert(6,str(value['gold']))
            temp_content.insert(7,str(value['stone']))
            temp_content.insert(8,str(value['free_draw_material']))
            item_config = game_config.get_item_config(value['item'])
            if item_config:
                temp_content.insert(9,str(item_config['name']))
            else:
                temp_content.insert(9,str(u''))
            temp_content.insert(10,str(value['item_num']))

            monster_config = game_config.get_monster_config(value['monster'])
            if monster_config:
                temp_content.insert(11,str(monster_config['name']))
            else:
                temp_content.insert(11,str(u''))

            temp_content.insert(12,str(value['monster_star_level']))
            table_list.append(temp_content)

    data['system_mail_info'] = table_list
    data['head_lst'] = head_lst
    return render_to_response("system_mail/system_mail_lst.html", data, RequestContext(request))



def system_mail_add(request):
    """
    添加系统邮件
    """
    item_id_name, item_id_type = game_config.get_item_config_with_id_name()
    item_tid_name_lst = dict()
    item_tid_name_lst[0] = "无"
    for (tid, name) in item_id_name.items():
        if item_id_type[tid] != game_define.ITEM_TYPE_EQUIP:
            item_tid_name_lst[tid] = name
    data = dict()
    data['item_val'] = item_tid_name_lst.items()

    monster_id_name = game_config.get_monster_config_with_id_name()
    monster_id_name[0] = "无"
    monster_tid_name_lst = dict()
    for (tid, name) in monster_id_name.items():
        monster_tid_name_lst[tid] = name

    data['monster_val'] = monster_tid_name_lst.items()
    data['server_id'] = 10001
    data['target_user_uid'] = '1000004126'
    data['send_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_detla = datetime.timedelta(0, 0, 0, 0, 0, 72)
    indate_default = (datetime.datetime.now() + time_detla).strftime('%Y-%m-%d %H:%M:%S')
    data['indate'] = indate_default
    print data
    return render_to_response("system_mail/system_mail_add.html", data,RequestContext(request))

def string_split_to_int_list(str,   sep=','):
    """
        字符串切割成int数组
    """
    if str == '' or None:
        return []
    lst_str = str.split(sep)
    lst_int = map(lambda x: int(x), lst_str)
    return lst_int


def add_system_mail(server_notice_box_model, mail):
        """
        添加一个系统邮件
            Arg:
                mail 邮件 dict
        """
        mail['uid'] = server_notice_box_model['seq']
        mail['expiry_date'] = mail['indate']

        server_notice_box_model['mails'].append(mail)
        server_notice_box_model['seq'] += 1

def system_mail_update(request):
    """
    更新广播
    """
    if request.method == 'POST':
        version = str(request.POST.get('version'))
        server_id_str = str(request.POST.get('server_id'))
        target_user_uid = str(request.POST.get('target_user_uid'))
        title = str(request.POST.get('title'))
        send_time = datetime.datetime.strptime(request.POST.get('send_time'),"%Y-%m-%d %H:%M:%S")
        indate = datetime.datetime.strptime(request.POST.get('indate'),"%Y-%m-%d %H:%M:%S")
        gold = int(request.POST.get('gold'))
        stone = int(request.POST.get('stone'))
        free_draw_material = int(request.POST.get('free_draw_material'))
        item = int(request.POST.get('item'))
        item_num = int(request.POST.get('item_num'))
        monster = int(request.POST.get('monster'))
        star = int(request.POST.get('star'))

        # 插入系统邮件
        mail = dict()
        mail['version'] = version
        mail['server_id'] = server_id_str
        mail['target_user_uid'] = target_user_uid
        mail['title'] = title
        mail['indate'] = indate
        mail['send_time'] = send_time
        mail['gold'] = gold
        mail['stone'] = stone
        mail['free_draw_material'] = free_draw_material
        mail['item'] = item
        mail['item_num'] = item_num
        mail['monster'] = monster
        mail['monster_star_level'] = star

        print("mail: "+str(mail))
        if not server_id_str:
            all_cmem_dict = server_define.CMEM_MAP
            for key, val in all_cmem_dict.items():
                cmem_url = str(val)
                if cmem_url:
                    server_notice_box_model = memcache.get_cmem_val(cmem_url, model_define.SYSTEM_MAIL_BOX_MODEL)
                    if not server_notice_box_model:
                        server_notice_box_model = {
                            'uid': 'game_system_mail_box',
                            'mails': [],
                            'seq_id': '20150729_1'
                        }
                    add_system_mail(server_notice_box_model,mail)
                    print("server_notice_box_model: "+str(server_notice_box_model))
                    memcache.put_cmem_val(cmem_url, model_define.SYSTEM_MAIL_BOX_MODEL, server_notice_box_model)

                    # 操作日志记录
                    manager = GameManager.get_by_request(request)
                    insert_action_add_mail(manager, mail)
        else:
            server_int_lst = string_split_to_int_list(server_id_str,',')
            for server_int in server_int_lst:
                cmem_url = server_define.CMEM_MAP[int(server_int)]
                if cmem_url:
                    server_notice_box_model = memcache.get_cmem_val(cmem_url, model_define.SYSTEM_MAIL_BOX_MODEL)
                    if not server_notice_box_model:
                        server_notice_box_model = {
                            'uid': 'game_system_mail_box',
                            'mails': [],
                            'seq_id': '20150729_1'
                        }
                    add_system_mail(server_notice_box_model,mail)
                    print("server_notice_box_model: "+str(server_notice_box_model))
                    memcache.put_cmem_val(cmem_url, model_define.SYSTEM_MAIL_BOX_MODEL, server_notice_box_model)

                    # 操作日志记录
                    manager = GameManager.get_by_request(request)
                    insert_action_add_mail(manager, mail)
        return HttpResponseRedirect('/Tyranitar6/server/system_mail_lst/')

    else:
        return render_to_response("system_mail/system_mail_add.html",RequestContext(request))

def system_mail_del_confirm(request):
    """
    删除邮件确认
    """
    if request.method == 'POST':
        version = str(request.POST.get("version"))
        del_notice_dict = dict()
        all_cmem_dict = server_define.CMEM_MAP
        for key, val in all_cmem_dict.items():
            cmem_url = str(val)
            if cmem_url:
                server_notice_box_model = memcache.get_cmem_val(cmem_url, model_define.SYSTEM_MAIL_BOX_MODEL)
                if server_notice_box_model:
                    memcache.put_cmem_val(cmem_url, model_define.SYSTEM_MAIL_BOX_MODEL, server_notice_box_model)
                    print server_notice_box_model
                    check_system_expiry(server_notice_box_model)
                    notices_lst = server_notice_box_model['mails']
                    if notices_lst:
                        for notice_dict in notices_lst:
                            if notice_dict:
                                if version == str(notice_dict['version']):
                                    del_notice_dict = notice_dict
                                    break

        del_notice_dict['send_time'] = str(del_notice_dict['send_time'].strftime('%Y-%m-%d %H:%M:%S'))
        del_notice_dict['expiry_date'] = str(del_notice_dict['expiry_date'].strftime('%Y-%m-%d %H:%M:%S'))
        item_config = game_config.get_item_config(del_notice_dict['item'])
        if item_config:
            del_notice_dict['item'] = str(item_config['name'])
        else:
            del_notice_dict['item'] = str(u'')

        monster_config = game_config.get_monster_config(del_notice_dict['monster'])
        if monster_config:
            del_notice_dict['monster'] = str(monster_config['name'])
        else:
            del_notice_dict['monster'] = str(u'')

        return render_to_response("system_mail/system_mail_del_confirm.html", {'system_mail_info': del_notice_dict,'head_lst': head_lst}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/server/system_mail_lst/')

def system_mail_del(request):
    """
    删除系统邮件
    """
    if request.method == 'POST':
        version = str(request.POST.get("version"))
        del_notice_dict = dict()
        all_cmem_dict = server_define.CMEM_MAP
        for key, val in all_cmem_dict.items():
            cmem_url = str(val)
            if cmem_url:
                server_notice_box_model = memcache.get_cmem_val(cmem_url, model_define.SYSTEM_MAIL_BOX_MODEL)
                if server_notice_box_model:
                    memcache.put_cmem_val(cmem_url, model_define.SYSTEM_MAIL_BOX_MODEL, server_notice_box_model)
                    print server_notice_box_model
                    check_system_expiry(server_notice_box_model)
                    notices_lst = server_notice_box_model['mails']
                    if notices_lst:
                        for notice_dict in notices_lst:
                            if notice_dict:
                                if version == str(notice_dict['version']):
                                    server_notice_box_model['mails'].remove(notice_dict)
                                    memcache.put_cmem_val(cmem_url, model_define.SYSTEM_MAIL_BOX_MODEL, server_notice_box_model)
                                    # 操作日志记录
                                    manager = GameManager.get_by_request(request)
                                    insert_action_delete_mail(manager, version)
                                    break

        return HttpResponseRedirect('/Tyranitar6/server/system_mail_lst/')
    else:
        return render_to_response("system_mail/system_mail_add.html",RequestContext(request))