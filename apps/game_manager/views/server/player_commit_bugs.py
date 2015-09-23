# -*- coding:utf-8 -*-


from apps.game_manager.models.game_manager import *

from apps.game_manager.mysql import server_notice
from django.http import HttpResponseRedirect
from django.template import RequestContext
from apps.utils import game_define
from apps.game_manager.util import memcache
from apps.utils import server_define
from apps.utils import model_define
from apps.game_manager.mysql import server_list
import datetime
from apps.config import game_config
from apps.logs.output_action_gm import *

head_lst = [
    {'width': 70, 'name': u'玩家UID'},
    {'width': 55, 'name': u'玩家OPEN_ID'},
    {'width': 55, 'name': u'玩家名字'},
    {'width': 50, 'name': u'提交时间'},
    {'width': 50, 'name': u'描述'},
    {'width': 50, 'name': u'是否需要回信'},
    {'width': 50, 'name': u'操作'},
]

def get_bugs(player_commit_bugs_model):
        """
            获取指定区间BUG
        """
        # 按照日期倒序
        player_commit_bugs_model['bugs'] = sorted(player_commit_bugs_model['bugs'], cmp=lambda x,y: cmp(datetime.datetime.strptime(x['commit_time'],"%Y-%m-%d %H:%M:%S"), datetime.datetime.strptime(y['commit_time'],"%Y-%m-%d %H:%M:%S")),reverse=True)
        return player_commit_bugs_model['bugs']

def player_commit_bugs_lst(request):
    """
    获取玩家提交的BUG
    """
    server_list_dat = server_list.get_server_list_dat()
    data = {}
    data['head_lst'] = head_lst
    data['server_list'] = server_list_dat
    if request.POST.get('server_id'):
        server_id = int(request.POST.get('server_id'))
        table_list = []
        all_background_notice_lst = []

        cmem_url = str(server_define.CMEM_MAP.get(server_id))
        if cmem_url:
            player_commit_bugs_model = memcache.get_cmem_val(cmem_url, model_define.PLAYER_COMMIT_BUGS_MODEL)
            if player_commit_bugs_model:
                # memcache.put_cmem_val(cmem_url, model_define.PLAYER_COMMIT_BUGS_MODEL, server_notice_box_model)
                print player_commit_bugs_model
                bug_lst = get_bugs(player_commit_bugs_model)
                if bug_lst:
                    for bug_dict in bug_lst:
                        if bug_dict:
                            all_background_notice_lst.append(bug_dict)

        print("all_background_notice_lst: "+str(all_background_notice_lst))
        for bug_dict in all_background_notice_lst:
            if bug_dict:
                temp_content = []
                temp_content.insert(0,str(bug_dict['user_uid']))
                temp_content.insert(1,str(bug_dict['user_open_id']))
                temp_content.insert(2,str(bug_dict['player_name']))
                temp_content.insert(3,str(bug_dict['commit_time']))
                temp_content.insert(4,str(bug_dict['describe']))
                if bug_dict.get('handle',False):
                    temp_content.insert(5,"已回信")
                else:
                    temp_content.insert(5,"需要回信")
                table_list.append(temp_content)

        data['player_commit_bugs'] = table_list
        data['server_id'] = server_id
        print data
        return render_to_response("player_commit_bugs/player_commit_bugs_lst.html", data, RequestContext(request))
    else:
        data['player_commit_bugs'] = []
        return render_to_response("player_commit_bugs/player_commit_bugs_lst.html", data, RequestContext(request))

def remove_all_bugs(player_commit_bugs_model):
        """
            移除全部
        """
        player_commit_bugs_model['bugs'] = []

def get_bug_uid_time(player_commit_bugs_model, uid, time):
        """
            用uid和time获取bug
        """
        for item in player_commit_bugs_model['bugs']:
            if item['user_uid'] == uid and item['commit_time'] == time:
                return item
        return dict()

def remove_bug(player_commit_bugs_model, bug_dict):
        """
            移除一个BUG
            Arg:
                bug_dict bug具体内容 dict
        """
        player_commit_bugs_model['bugs'].remove(bug_dict)



def player_commit_bugs_del_confirm(request):
    """
    删除玩家提交的BUG确认
    """
    if request.method == 'POST':
        user_uid = str(request.POST.get("uid"))
        time = str(request.POST.get("time"))
        # time = datetime.datetime.strptime(request.POST.get('time'),"%Y-%m-%d %H:%M:%S")
        server_id = int(request.POST.get("server_id"))
        print("user_uid: "+str(user_uid))
        print("time: "+str(time))
        print("server_id: "+str(server_id))
        bug_dict = dict()
        cmem_url = str(server_define.CMEM_MAP.get(server_id))
        if cmem_url:
            player_commit_bugs_model = memcache.get_cmem_val(cmem_url, model_define.PLAYER_COMMIT_BUGS_MODEL)
            if player_commit_bugs_model:
                print player_commit_bugs_model
                bug_dict = get_bug_uid_time(player_commit_bugs_model,user_uid, time)

        bug_dict['server_id'] = server_id
        if bug_dict.get('handle',False):
            bug_dict['handle'] = "已回信"
        else:
            bug_dict['handle'] = "需要回信"
        print bug_dict
        return render_to_response("player_commit_bugs/player_commit_bugs_del_confirm.html", {'bug_dict': bug_dict,'head_lst': head_lst}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/server/player_commit_bugs_lst/')

def player_commit_bugs_del(request):
    """
    删除玩家提交的BUG
    """
    if request.method == 'POST':
        user_uid = str(request.POST.get("uid"))
        time = str(request.POST.get("time"))
        server_id = int(request.POST.get("server_id"))
        cmem_url = str(server_define.CMEM_MAP.get(server_id))
        if cmem_url:
            player_commit_bugs_model = memcache.get_cmem_val(cmem_url, model_define.PLAYER_COMMIT_BUGS_MODEL)
            if player_commit_bugs_model:
                print player_commit_bugs_model
                bug_dict = get_bug_uid_time(player_commit_bugs_model,user_uid, time)
                remove_bug(player_commit_bugs_model,bug_dict)
                memcache.put_cmem_val(cmem_url, model_define.PLAYER_COMMIT_BUGS_MODEL, player_commit_bugs_model)

                # 操作日志记录
                manager = GameManager.get_by_request(request)
                insert_action_delete_bug(manager, bug_dict)

    return HttpResponseRedirect('/Tyranitar6/server/player_commit_bugs_lst/')

def player_commit_bugs_del_all_confirm(request):
    """
    删除玩家提交的BUG确认
    """
    if request.method == 'POST':
        server_id = int(request.POST.get("server_id"))
        print("server_id: "+str(server_id))
        bug_dict = dict()
        cmem_url = str(server_define.CMEM_MAP.get(server_id))
        if cmem_url:
            player_commit_bugs_model = memcache.get_cmem_val(cmem_url, model_define.PLAYER_COMMIT_BUGS_MODEL)
            if player_commit_bugs_model:
                print player_commit_bugs_model

        bug_dict['server_id'] = server_id
        return render_to_response("player_commit_bugs/player_commit_bugs_del_all_confirm.html", {'bug_dict': bug_dict}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/server/player_commit_bugs_lst/')

def player_commit_bugs_del_all(request):
    """
    删除玩家提交的BUG
    """
    if request.method == 'POST':
        server_id = int(request.POST.get("server_id"))
        cmem_url = str(server_define.CMEM_MAP.get(server_id))
        if cmem_url:
            player_commit_bugs_model = memcache.get_cmem_val(cmem_url, model_define.PLAYER_COMMIT_BUGS_MODEL)
            if player_commit_bugs_model:
                print player_commit_bugs_model
                remove_all_bugs(player_commit_bugs_model)
                memcache.put_cmem_val(cmem_url, model_define.PLAYER_COMMIT_BUGS_MODEL, player_commit_bugs_model)

                # 操作日志记录
                manager = GameManager.get_by_request(request)
                insert_action_delete_bug_all(manager)

    return HttpResponseRedirect('/Tyranitar6/server/player_commit_bugs_lst/')

def player_commit_bugs_mail(request):
    """
    回信
    """
    target_user_uid = str(request.POST.get('user_uid'))
    server_id = int(request.POST.get("server_id"))
    time = str(request.POST.get("time"))

    time_detla = datetime.timedelta(0, 0, 0, 0, 0, 72)
    indate_default = (datetime.datetime.now() + time_detla).strftime('%Y-%m-%d %H:%M:%S')

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
    data['target_user_uid'] = target_user_uid
    data['indate'] = indate_default
    data['send_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['server_id'] = server_id
    data['time'] = time
    print data
    return render_to_response("player_commit_bugs/player_commit_bugs_mail_add.html", data,RequestContext(request))

def add_system_mail(player_mail_box_model, mail):
        """
        添加一个系统邮件
        """
        mail['uid'] = player_mail_box_model['seq']
        mail['is_active'] = True
        mail['is_del'] = False
        mail['is_reward'] = False
        mail['expiry_date'] = mail['indate']
        player_mail_box_model['seq'] += 1
        player_mail_box_model['system_mail'].append(mail)

def player_commit_bugs_mail_update(request):
    """
    回信
    """
    time = str(request.POST.get("time"))
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
    cmem_url = server_define.CMEM_MAP[int(server_id_str)]
    if cmem_url:
        player_mail_box_model = memcache.get_cmem_val(cmem_url, model_define.PLAYER_MAIL_BOX_MODEL.format(user_id=target_user_uid))
        if not player_mail_box_model:
            player_mail_box_model = {
                'uid': target_user_uid,
                'system_mail': [],
                'seq': '1000'
            }
        # 给玩家发送邮件 告知返还事宜
        add_system_mail(player_mail_box_model, mail)
        print("player_mail_box_model: "+str(player_mail_box_model))
        memcache.put_cmem_val(cmem_url, model_define.PLAYER_MAIL_BOX_MODEL.format(user_id=target_user_uid), player_mail_box_model)

        # 操作日志记录
        manager = GameManager.get_by_request(request)
        insert_action_add_bug_mail(manager, mail)

        player_commit_bugs_model = memcache.get_cmem_val(cmem_url, model_define.PLAYER_COMMIT_BUGS_MODEL)
        if player_commit_bugs_model:
            print player_commit_bugs_model
            mail_bug = get_bug_uid_time(player_commit_bugs_model,target_user_uid, time)
            mail_bug['handle'] = True
            memcache.put_cmem_val(cmem_url, model_define.PLAYER_COMMIT_BUGS_MODEL, player_commit_bugs_model)

    return HttpResponseRedirect('/Tyranitar6/server/player_commit_bugs_lst/')