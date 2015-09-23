# -*- coding:utf-8 -*-

import datetime
import collections
from django.template import RequestContext
from apps.game_manager.views.log import daily_log
from django.shortcuts import render_to_response,HttpResponse
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define,game_define
from apps.common.decorators.decorators import require_permission
from apps.game_manager.mysql.server_list import get_server_list_dat
from apps.config.game_config import get_all_stone_shop_config,get_item_config_with_id_name,get_gym_buff_config,get_gym_stage_config,get_gym_zone_config
import hashlib
import pickle



# 道馆信息
@require_permission
def get_gym_info(request):
    head_lst = [
        {'width': 50, 'name': u'当前关卡ID'},
        {'width': 50, 'name': u'当前手动重置挑战次数'},
        {'width': 50, 'name': u'当前挑战星级'},
        {'width': 50, 'name': u'历史挑战最高星级'},

        {'width': 50, 'name': u'当前关卡是否已挑战'},
        {'width': 50, 'name': u'当前可用星级'},
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
        name_dict,laji=get_item_config_with_id_name()
        shop_dict=get_all_stone_shop_config()
        server_id = int(request.POST.get('server_id'))
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        row_lst={}
        print user_id
        source=None
        # f=open('/opt/CGameLogserver/apps/game_manager/views/data_edit/USER_DETAIL')
        # d=pickle.load(f)
        # for i in d:
        #     user_id=str(i)
        refresh_time=''
        if cmem_url:
            if  len(user_id) <> 0:
                source = memcache.get_cmem_val(cmem_url, model_define.GYM_MODEL.format(user_id=user_id))
            elif  len(user_name)<> 0:
                name = hashlib.md5(user_name).hexdigest().upper()
                key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                source = memcache.get_cmem_val(cmem_url,model_define.GYM_MODEL.format(user_id=user_uid))
            elif  len(user_openid) <> 0:
                try:
                    result = memcache.get_cmem_val(cmem_url,model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.GYM_MODEL.format(user_id=result['uid']))
                    user_id=source['uid']
                except:
                    pass
            if source<> None:
                refresh_time='上次手动刷新时间 %s' % str(source['last_refresh_date'])
                row_lst['cur_gym_id']=['当前关卡ID',source['cur_gym_id']]
                row_lst['cur_reset_gym_count']=[u'当前手动重置挑战次数',source['cur_reset_gym_count']]
                row_lst['history_top_star_num']=[ u'历史最高星级',source['history_top_star_num']]
                row_lst['cur_star_num']=[u'当前星级',source['cur_star_num']]
                row_lst['cur_gym_end']=[u'当前关卡是否已挑战',source['cur_gym_end']]
                row_lst['cur_use_star']=[ u'当前已使用星级',source['cur_use_star']]
                cur_zone_star_num_lst=source['cur_zone_star_num_lst']
                cur_battle_buffs=''
                if len(source['cur_battle_buffs'])<>0:
                    for i in source['cur_battle_buffs']:
                        cur_battle_buffs+=str(i)+'，'
                can_mop_zone=''
                if len(list(source['can_mop_zone']))<>0:
                    for i in list(source['can_mop_zone']):
                        can_mop_zone+=str(i)+' ， '
                has_reward_id=''
                if len(list(source['has_reward_id']))<>0:
                    for i in list(source['has_reward_id']):
                        has_reward_id+=str(i)+'，'

                # row_lst['cur_zone_star_num_lst']=['当前挑战区域关卡星级：',source['cur_zone_star_num_lst'][0],source['cur_zone_star_num_lst'][1],source['cur_zone_star_num_lst'][2]]
                # row_lst['cur_battle_buffs']=['当前所携带的BUFF：']
                # for i in xrange(len(source['cur_battle_buffs'])):
                #     row_lst['cur_battle_buffs'].append(source['cur_battle_buffs'][i])
                # row_lst['can_mop_zone']=['可以扫荡的区域ID：']
                # for i in xrange(len(source['can_mop_zone'])):
                #     row_lst['can_mop_zone'].append(list(source['can_mop_zone'])[i])
                # row_lst['has_reward_id']=['已经购买的奖励ID：']
                # for i in xrange(len(source['has_reward_id'])):
                #     # print tuple(source['has_reward_id'])[1]
                #     row_lst['has_reward_id'].append(list(source['has_reward_id'])[i])

                # # for i in xrange(len(source['cur_zone_star_num_lst'])):
                #     row_lst['cur_zone_star_num_lst%s' % str(i+1) ]=['当前挑战区域关卡%s的挑战星级：' % i+1,source['cur_zone_star_num_lst'][i]]
                # print get_gym_buff_config(1)
                # for i in xrange(len(source['cur_battle_buffs'])):
                #     row_lst['cur_battle_buffs%s' % i+1 ]=['当前所携带的BUFF：' % i+1,source['cur_battle_buffs'][i]]
                # for i in xrange(len(source['can_mop_zone'])):
                #     row_lst['can_mop_zone%s' % i+1]=['可以扫荡的区域%s：'% i+1,source['can_mop_zone'][i]]
                print row_lst
        return render_to_response("data_edit/gym_info.html",
                                  {'row_lst': row_lst,'user_id':user_id,'user_openid':user_openid,'user_name':user_name,
                                   'head_lst': head_lst, 'server_list': server_list_dat,'cur_server_id':server_id,'refresh_time':refresh_time
                                   ,'cur_zone_star_num_lst':cur_zone_star_num_lst,'cur_battle_buffs':cur_battle_buffs,'has_reward_id':has_reward_id}, RequestContext(request))
    else:
        row_lst = []
        return render_to_response("data_edit/gym_info.html",
                                  {'row_lst': row_lst,
                                   'head_lst': head_lst, 'server_list': server_list_dat}, RequestContext(request))


@require_permission
def set_gym_zone_star(request):
    print request.POST
    if request.POST:
        ps=request.POST.get('ps')
        server_id=request.POST.get('server_id')
        user_id=request.POST.get('user_id')
        print user_id
        value=request.POST.get('value')
        key=request.POST.get('key')
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        source = memcache.get_cmem_val(cmem_url, model_define.GYM_MODEL.format(user_id=user_id))
        source[key][int(ps)-1] = int(value)
        data=memcache.put_cmem_val(cmem_url,model_define.GYM_MODEL.format(user_id=user_id),source)
        if data==True:
            data='True'
        elif data==False:
            data='False'
        return HttpResponse(data)

@require_permission
def set_gym_value(request):
    print request.POST
    key=request.POST.get('key')
    server_id=request.POST.get('server_id')
    user_id=request.POST.get('user_id')
    value=request.POST.get('value')
    junge=0
    alert_info=''
    print value
    cmem_url = server_define.CMEM_MAP[int(server_id)]
    source = memcache.get_cmem_val(cmem_url, model_define.GYM_MODEL.format(user_id=user_id))
    if key=='cur_reset_gym_count':
        if int(value) not in [0,1,2,3]:
            alert_info='应取值0~3之间'
    elif key=='cur_gym_id':
        if get_gym_stage_config(int(value))==None:
            alert_info='道馆关卡ID应取值1~60之间'
        else:
            value=((get_gym_stage_config(int(value))['zone']-1)*3)+1
            print value,'value'
    elif key=='cur_use_star':
        if int(value) > source['cur_star_num']:
            alert_info='‘当前已使用星级’不可大于‘当前星级’'
    if alert_info!='':
        return HttpResponse(alert_info)
    else:

        if value =='False' or value=='True':
            if value=='False':
                source[key]=False
            else:
                source[key]=True
        else:
            source[key]=int(value)
        print source
        data=memcache.put_cmem_val(cmem_url,model_define.GYM_MODEL.format(user_id=user_id),source)
        if data:
             return HttpResponse(alert_info)