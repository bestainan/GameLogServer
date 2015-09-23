# -*- coding:utf-8 -*-


from apps.game_manager.models.game_manager import *

from apps.game_manager.mysql import server_notice
from django.http import HttpResponseRedirect
from django.template import RequestContext
from apps.utils import game_define
from apps.game_manager.util import memcache
from apps.utils import server_define
from apps.utils import model_define
from apps.logs.output_action_gm import *
import datetime


head_lst = [
    {'width': 70, 'name': u'广播UID'},
    {'width': 55, 'name': u'服务器列表'},
    {'width': 50, 'name': u'内容'},
    {'width': 50, 'name': u'开始时间'},
    {'width': 70, 'name': u'销毁时间'},
    {'width': 50, 'name': u'间隔分钟数'},
    {'width': 50, 'name': u'操作'},
]

def list_to_string(lst):
    """
        把列表转成字符串 [1,2,3] 转换 1,2,3
    """
    lst_str = map(lambda x: str(x), lst)
    return ','.join(lst_str)

def check_notice_expiry(server_notice_box_model):
        """
        检测广播过期
        """

        select_expiry_notice = lambda notice: notice['expiry_date'] <= datetime.datetime.now()
        expiry_notice = filter(select_expiry_notice, server_notice_box_model['notices'])
        for item in expiry_notice:
            server_notice_box_model['notices'].remove(item)
        expiry_player_notice = filter(select_expiry_notice, server_notice_box_model['player_notices'])
        for item in expiry_player_notice:
            server_notice_box_model['player_notices'].remove(item)
        return len(expiry_notice) > 0 or len(expiry_player_notice) > 0

def notice_lst(request):
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
            server_notice_box_model = memcache.get_cmem_val(cmem_url, model_define.NOTICE_MODEL)
            if server_notice_box_model:
                # server_notice_box_model = {
                #     'uid': 'game_notice',
                #     'notices': [],
                #     'player_notices': [],
                #     'seq_id': 1
                # }
                # server_notice_box_model = memcache.put_cmem_val(cmem_url, model_define.NOTICE_MODEL, server_notice_box_model)
                memcache.put_cmem_val(cmem_url, model_define.NOTICE_MODEL, server_notice_box_model)
                print server_notice_box_model
                check_notice_expiry(server_notice_box_model)
                notices_lst = server_notice_box_model['notices']
                if notices_lst:
                    for notice_dict in notices_lst:
                        if notice_dict:
                            notice_uid = notice_dict['uid']
                            # if notice_uid in all_background_notice_dict:
                            #     print("notice_uid: "+str(notice_uid))
                            #     notice_dict['server_id'] = notice_dict.get('server_id','')+","+str(key)
                            # else:
                            #     notice_dict['server_id'] = str(key)
                            all_background_notice_dict[notice_uid] = notice_dict

    print("all_background_notice_dict: "+str(all_background_notice_dict))
    for key_uid, value in all_background_notice_dict.items():
        if value:
            temp_content = []
            temp_content.insert(0,str(key_uid))
            temp_content.insert(1,value['server_id'])
            temp_content.insert(2,str(value['content']))
            temp_content.insert(3,value['start_time'].strftime('%Y-%m-%d %H:%M:%S'))
            temp_content.insert(4,value['expiry_date'].strftime('%Y-%m-%d %H:%M:%S'))
            temp_content.insert(5,str(value['distance_time']))
            table_list.append(temp_content)

    data['notice_info'] = table_list
    data['head_lst'] = head_lst
    return render_to_response("notice/notice_lst.html", data, RequestContext(request))


def notice_add(request):
    """
    添加广播
    """
    return render_to_response("notice/notice_add.html", RequestContext(request))

def string_split_to_int_list(str,   sep=','):
    """
        字符串切割成int数组
    """
    if str == '' or None:
        return []
    lst_str = str.split(sep)
    lst_int = map(lambda x: int(x), lst_str)
    return lst_int

def add_background_notice(server_notice_box_model, notice):
        """
            添加系统广播
        """
        notice['type'] = 0
        notice['publish'] = datetime.datetime.now()

        server_notice_box_model['notices'].append(notice)
        server_notice_box_model['seq_id'] += 1


def notice_update(request):
    """
    更新广播
    """
    if request.method == 'POST':
        content = str(request.POST.get('content'))
        start_time = datetime.datetime.strptime(request.POST.get('start_time'),"%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(request.POST.get('end_time'),"%Y-%m-%d %H:%M:%S")
        distance_time = int(request.POST.get('distance_time'))
        str_server_id = str(request.POST.get('server_id'))
        uid = str(request.POST.get('uid'))

        #插入系统邮件
        notice = dict()
        notice['content'] = content
        notice['start_time'] = start_time
        notice['distance_time'] = distance_time
        notice['expiry_date'] = end_time
        notice['server_id'] = str_server_id
        notice['uid'] = uid
        print("notice: "+str(notice))
        server_int_lst = string_split_to_int_list(str_server_id,',')
        for server_int in server_int_lst:
            cmem_url = server_define.CMEM_MAP[int(server_int)]
            if cmem_url:
                server_notice_box_model = memcache.get_cmem_val(cmem_url, model_define.NOTICE_MODEL)
                if not server_notice_box_model:
                    server_notice_box_model = {
                        'uid': 'game_notice',
                        'notices': [],
                        'player_notices': [],
                        'seq_id': '20150729_1'
                    }
                add_background_notice(server_notice_box_model,notice)
                print("server_notice_box_model: "+str(server_notice_box_model))
                memcache.put_cmem_val(cmem_url, model_define.NOTICE_MODEL, server_notice_box_model)

                # 操作日志记录
                manager = GameManager.get_by_request(request)
                insert_action_update_notice(manager, notice)

        return HttpResponseRedirect('/Tyranitar6/server/notice_lst/')
    else:
        return render_to_response("notice/notice_add.html",RequestContext(request))

def notice_del_confirm(request):
    """
    删除广播确认
    """
    if request.method == 'POST':
        uid = str(request.POST.get("uid"))
        del_notice_dict = dict()
        all_cmem_dict = server_define.CMEM_MAP
        for key, val in all_cmem_dict.items():
            cmem_url = str(val)
            if cmem_url:
                server_notice_box_model = memcache.get_cmem_val(cmem_url, model_define.NOTICE_MODEL)
                if server_notice_box_model:
                    memcache.put_cmem_val(cmem_url, model_define.NOTICE_MODEL, server_notice_box_model)
                    print server_notice_box_model
                    check_notice_expiry(server_notice_box_model)
                    notices_lst = server_notice_box_model['notices']
                    if notices_lst:
                        for notice_dict in notices_lst:
                            if notice_dict:
                                if uid == str(notice_dict['uid']):
                                    del_notice_dict = notice_dict
                                    break

        del_notice_dict['start_time'] = str(del_notice_dict['start_time'].strftime('%Y-%m-%d %H:%M:%S'))
        del_notice_dict['expiry_date'] = str(del_notice_dict['expiry_date'].strftime('%Y-%m-%d %H:%M:%S'))
        return render_to_response("notice/notice_del_confirm.html", {'notice_info': del_notice_dict,'head_lst': head_lst}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/server/notice_lst/')

def notice_del(request):
    """
    删除广播
    """
    if request.method == 'POST':
        uid = str(request.POST.get("uid"))
        # del_notice_dict = dict()
        all_cmem_dict = server_define.CMEM_MAP
        for key, val in all_cmem_dict.items():
            cmem_url = str(val)
            if cmem_url:
                server_notice_box_model = memcache.get_cmem_val(cmem_url, model_define.NOTICE_MODEL)
                if server_notice_box_model:
                    print server_notice_box_model
                    check_notice_expiry(server_notice_box_model)
                    notices_lst = server_notice_box_model['notices']
                    if notices_lst:
                        for notice_dict in notices_lst:
                            if notice_dict:
                                if uid == str(notice_dict['uid']):
                                    # del_notice_dict = notice_dict
                                    server_notice_box_model['notices'].remove(notice_dict)
                                    memcache.put_cmem_val(cmem_url, model_define.NOTICE_MODEL, server_notice_box_model)
                                    # 操作日志记录
                                    manager = GameManager.get_by_request(request)
                                    insert_action_delete_notice(manager, uid)
                                    break

        return HttpResponseRedirect('/Tyranitar6/server/notice_lst/')
    else:
        return render_to_response("notice/notice_add.html",RequestContext(request))