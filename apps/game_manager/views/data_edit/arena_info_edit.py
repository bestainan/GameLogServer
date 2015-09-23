# -*- coding:utf-8 -*-

import datetime
import collections
from django.template import RequestContext
from django.shortcuts import render_to_response
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define,game_define
from apps.common.decorators.decorators import require_permission
from apps.game_manager.mysql.server_list import get_server_list_dat
from apps.utils.mem_key_name import  MEM_KEY_NAME,FORBIDE_CHANGE_VALUES
from apps.config.game_config import get_item_config_with_id_name,get_monster_config_with_id_name
import hashlib
import time



# 获取玩家竞技场报告
@require_permission
def get_arena_report_info(request):
    head_lst = [
        {'width': 50, 'name': u'玩家UID'},
        {'width': 50, 'name': u'玩家当前排名'},
        ]
    server_list_dat = get_server_list_dat()
    if request.method == 'POST':
        user_id = request.POST.get('user_uid')
        user_name = request.POST.get('user_name').encode('utf-8')
        user_account = request.POST.get('user_account')
        try:
            user_openid = str(request.POST.get('user_openid'))
        except UnicodeEncodeError :
            user_openid = ''

        server_id = int(request.POST.get('server_id'))
        type_hidden = 'visible'
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        state_list = game_define.USER_STATE_NAME_DICT
        row_lst=[]
        source=None
        if cmem_url:
            if  len(user_id) <> 0:
                source = memcache.get_cmem_val(cmem_url, model_define.ARENA_BATTLE_REPORT_MODEL.format(user_id=user_id))
                #print source,'source'
                info= _get_report_mem(source,user_id,server_id)
            elif  len(user_name)<> 0:
                name = hashlib.md5(user_name).hexdigest().upper()
                key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                source = memcache.get_cmem_val(cmem_url,model_define.ARENA_BATTLE_REPORT_MODEL.format(user_id=user_uid))
                info = _get_report_mem(source,user_id,server_id)
            elif  len(user_openid) <> 0:
                try:
                    result = memcache.get_cmem_val(cmem_url,model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.ARENA_BATTLE_REPORT_MODEL.format(user_id=result['uid']))
                    info = _get_report_mem(source,user_id,server_id)
                except:
                    pass
            else:
                info= []
            return render_to_response("data_edit/arena_report_info.html",
                                      {'row_lst': row_lst,'user_id':user_id,'user_openid':user_openid,'user_name':user_name,
                                       'head_lst': head_lst, 'server_list': server_list_dat,'cur_server_id':server_id,'info':info}, RequestContext(request))
    else:
        row_lst = []
        return render_to_response("data_edit/arena_report_info.html",
                                  {'row_lst': row_lst,
                                   'head_lst': head_lst, 'server_list': server_list_dat}, RequestContext(request))


def get_arena_reward_times_info(request):
    head_lst = [
        {'width': 50, 'name': u'奖励截止时间'},
        {'width': 50, 'name': u'奖励物品'},
        {'width': 50, 'name': u'玩家进行挑战次数'},
        {'width': 50, 'name': u'运营版本'},
        ]
    server_list_dat = get_server_list_dat()
    if request.method == 'POST':
        user_id = request.POST.get('user_uid')
        user_name = request.POST.get('user_name').encode('utf-8')
        user_account = request.POST.get('user_account')
        try:
            user_openid = str(request.POST.get('user_openid'))
        except UnicodeEncodeError :
            user_openid = ''
        server_id = int(request.POST.get('server_id'))
        type_hidden = 'visible'
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        row_lst=[]
        print user_id
        source=None
        if cmem_url:
            if  len(user_id) <> 0:
                source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_ACTIVITY_ARENA_MODEL.format(user_id=user_id))
            elif  len(user_name)<> 0:
                name = hashlib.md5(user_name).hexdigest().upper()
                key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                source = memcache.get_cmem_val(cmem_url,model_define.PLAYER_ACTIVITY_ARENA_MODEL.format(user_id=user_uid))
            elif  len(user_openid )<> 0:
                try:
                    result = memcache.get_cmem_val(cmem_url,model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_ACTIVITY_ARENA_MODEL.format(user_id=result['uid']))
                except:
                    pass
            row_lst.append([str(source['reward_end_date']),source['single_activity_has_reward_lst'],source[ 'num'],source['version']])
            return render_to_response("data_edit/arena_reward_times_info.html",
                                      {'row_lst': row_lst,'user_id':user_id,'user_openid':user_openid,'user_name':user_name,
                                       'head_lst': head_lst, 'server_list': server_list_dat,'cur_server_id':server_id}, RequestContext(request))
    else:
        row_lst = []
        return render_to_response("data_edit/arena_reward_times_info.html",
                                  {'row_lst': row_lst,
                                   'head_lst': head_lst, 'server_list': server_list_dat}, RequestContext(request))



def _get_report_mem(source,user_id,server_id):
    info=[]
    rank=0
    monster_name_dict= get_monster_config_with_id_name()
    print source
    if source <> None:
        dat=source['report_lst']
        for dat_line in dat:
            all_dict={}
            team_equips_lst=[]
            equips=dat_line['dat']['team_equip']
            equips_name_dict=_get_equips(dat_line['dat']['equips'])
            print
            if len(equips_name_dict)<>0:
                for i in equips:
                    temp=[]
                    for j in i:
                        if j <> 0:
                            temp.append({'name':equips_name_dict[j]['name'],'level':'等级:%s'%(equips_name_dict[j]['level'])})
                    if len(temp) <>0:
                       team_equips_lst.append(temp)
                all_dict['equips']=team_equips_lst
            # else:
            #     all_dict['equips']=team_equips_lst

            team_treasures_lst=[]
            treasures=dat_line['dat']['team_treasure']
            treasures_name_dict=_get_treasures(dat_line['dat']['treasures'])
            if len(treasures_name_dict)<>0:
                for i in treasures:
                    temp=[]
                    for j in i:
                        if j <> 0:
                            temp.append({'name':treasures_name_dict[j]['name'],'level':'等级:%s'%(treasures_name_dict[j]['level'])})
                    if len(temp) <>0:
                         team_treasures_lst.append(temp)
                all_dict['treasures']=team_treasures_lst
            # else:
                # all_dict['treasures']=treasures_name_dict

            team_monster_lst=[]
            monsters=dat_line['dat']['monsters']
            if len(monsters) <>0:
                for i in monsters:
                    if i<>None:
                        print i
                    #print monster_name_dict[i['tid']]
                        team_monster_lst.append({'name':monster_name_dict[i['tid']],'level':i['level'],'starLevel':i['starLevel'],
                                            'normal_attack':i['individual'][0],'normal_defense':i['individual'][1],'special_attack':i['individual'][2],'special_defense':i['individual'][3],'speed':i['individual'][4],
                                             'skillsLevel':i['skillsLevel'],'effort':i['effort']})
            all_dict['monster']=team_monster_lst
            all_dict['rank']=dat_line['rank']
            tim=time.strftime('%m/%d/%Y-%H:%M:%S',time.localtime(dat_line['time']))
            all_dict['time']=tim
            all_dict['name']=dat_line['name']
            all_dict['win']=dat_line['win']


            info.append(all_dict)
        uid=source['uid']
        #print info
    return info

def _get_equips(data):
    equips_dict={}
    item_config=get_item_config_with_id_name()[0]
    if len(data) <> 0:
        item_config=get_item_config_with_id_name()[0]
        for dat_line in data:
            equips_dict[dat_line['uid']]=dat_line
            equips_dict[dat_line['uid']]['name']=item_config[dat_line['tid']]
        print equips_dict,'equips'
        return equips_dict
    else:
        return equips_dict

def _get_treasures(data):
    treasures_dict={}
    item_config=get_item_config_with_id_name()[0]
    if len(data) <> 0:
        for dat_line in data:
            treasures_dict[dat_line['uid']]=dat_line
            treasures_dict[dat_line['uid']]['name']=item_config[dat_line['tid']]
        print treasures_dict
        return treasures_dict
    else:
        return treasures_dict

