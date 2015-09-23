# -*- coding:utf-8 -*-

import datetime
import collections
from django.template import RequestContext
from apps.game_manager.views.log import daily_log
from django.shortcuts import render_to_response
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define,game_define
from apps.common.decorators.decorators import require_permission
from apps.game_manager.mysql.server_list import get_server_list_dat
from apps.config.game_config import get_all_stone_shop_config,get_item_config_with_id_name,get_all_pvp_shop_config,get_world_boss_shop_config,get_ditto_shop_with_id,get_monster_config,\
    get_gym_shop_config
import hashlib
import pickle



# 钻石商店
@require_permission
def get_stone_shop_info(request):
    head_lst = [
        {'width': 50, 'name': u'物品名称'},
        {'width': 50, 'name': u'物品数量'},
        {'width': 50, 'name': u'物品价格（钻石）'},
        {'width': 50, 'name': u'是否购买'},
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
        row_lst=[]
        print user_id
        source=None
        refresh_time=''
        if cmem_url:
            if  len(user_id) <> 0:
                source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_STONE_SHOP_MODEL.format(user_id=user_id))
            elif  len(user_name)<> 0:
                name = hashlib.md5(user_name).hexdigest().upper()
                key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                source = memcache.get_cmem_val(cmem_url,model_define.PLAYER_STONE_SHOP_MODEL.format(user_id=user_uid))
            elif  len(user_openid) <> 0:
                try:
                    result = memcache.get_cmem_val(cmem_url,model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_STONE_SHOP_MODEL.format(user_id=result['uid']))
                except:
                    pass
            if source<> None:
                refresh_time='刷新时间：%s'% source['refresh_datetime'].strftime("%Y-%m-%d %H:%M:%S")
                if 'refresh_num' in source.keys():
                    refresh_time+='，刷新次数:  %s'% source['refresh_num']
                if len(['shop_item_state_dict'])<>0:
                    for i in source['shop_item_state_dict'].items():
                        result=_get_stone_shop_name(i[0],name_dict,shop_dict)
                        row_lst.append([result[0],result[1],result[2],_get_stone_shop_state(i[1])])
        return render_to_response("data_edit/stone_shop_info.html",
                                  {'row_lst': row_lst,'user_id':user_id,'user_openid':user_openid,'user_name':user_name,
                                   'head_lst': head_lst, 'server_list': server_list_dat,'cur_server_id':server_id,'refresh_time':refresh_time}, RequestContext(request))
    else:
        row_lst = []
        return render_to_response("data_edit/stone_shop_info.html",
                                  {'row_lst': row_lst,
                                   'head_lst': head_lst, 'server_list': server_list_dat}, RequestContext(request))

#玩家PVP商店
def get_pvp_shop_info(request):
    head_lst = [
        {'width': 50, 'name': u'物品名称'},
        {'width': 50, 'name': u'物品数量'},
        {'width': 50, 'name': u'物品价格（PVP点数）'},
        {'width': 50, 'name': u'是否购买'},
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
        shop_dict=get_all_pvp_shop_config()
        print shop_dict
        server_id = int(request.POST.get('server_id'))
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        row_lst=[]
        print user_id
        source=None
        # f=open('/opt/CGameLogserver/apps/game_manager/views/data_edit/USER_DETAIL')
        # d=pickle.load(f)
        # for i in d:
        # user_id=str(i)
        refresh_time=''
        if cmem_url:
            if  len(user_id) <> 0:
                source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_PVP_SHOP_MODEL.format(user_id=user_id))
            elif  len(user_name)<> 0:
                name = hashlib.md5(user_name).hexdigest().upper()
                key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                source = memcache.get_cmem_val(cmem_url,model_define.PLAYER_PVP_SHOP_MODEL.format(user_id=user_uid))
            elif  len(user_openid) <> 0:
                try:
                    result = memcache.get_cmem_val(cmem_url,model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_PVP_SHOP_MODEL.format(user_id=result['uid']))
                except:
                    pass
            if source<> None:
                refresh_time='刷新时间：%s'% source['refresh_datetime'].strftime("%Y-%m-%d %H:%M:%S")
                if 'refresh_num' in source.keys():
                    refresh_time+='，刷新次数:  %s'% source['refresh_num']
                if 'arena_emblem' in source.keys():
                    refresh_time+='，玩家现有PVP点数:  %s'% source['refresh_num']
                if len(['shop_item_state_dict'])<>0:
                    for i in source['shop_item_state_dict'].items():
                        result=_get_pvp_shop_name(i[0],name_dict,shop_dict)
                        row_lst.append([result[0],result[1],result[2],_get_stone_shop_state(i[1])])



        return render_to_response("data_edit/pvp_shop_info.html",
                                  {'row_lst': row_lst,'user_id':user_id,'user_openid':user_openid,'user_name':user_name,
                                   'head_lst': head_lst, 'server_list': server_list_dat,'cur_server_id':server_id,'refresh_time':refresh_time}, RequestContext(request))
    else:
        row_lst = []
        return render_to_response("data_edit/pvp_shop_info.html",
                                  {'row_lst': row_lst,
                                   'head_lst': head_lst, 'server_list': server_list_dat}, RequestContext(request))

#玩家百变怪商店
def get_ditto_shop_info(request):
    head_lst = [
        {'width': 50, 'name': u'物品名称'},
        {'width': 50, 'name': u'物品价格（百变怪点数）'},
        # {'width': 50, 'name': u'星级'},
        {'width': 50, 'name': u'是否购买'},
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
        refresh_time=''
        if cmem_url:
            if  len(user_id) <> 0:
                source = memcache.get_cmem_val(cmem_url, model_define.DITTO_SHOP_MODEL.format(user_id=user_id))
            elif  len(user_name)<> 0:
                name = hashlib.md5(user_name).hexdigest().upper()
                key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                source = memcache.get_cmem_val(cmem_url,model_define.DITTO_SHOP_MODEL.format(user_id=user_uid))
            elif  len(user_openid) <> 0:
                try:
                    result = memcache.get_cmem_val(cmem_url,model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.DITTO_SHOP_MODEL.format(user_id=result['uid']))
                except:
                    pass
            if source<> None:
                print source
                refresh_time='刷新时间：%s'% source['refresh_datetime'].strftime("%Y-%m-%d %H:%M:%S")
                if 'refresh_num' in source.keys():
                    refresh_time+='，刷新次数:  %s'% source['refresh_num']
                if len(['ditto_item_state_dict'])<>0:
                    print source['ditto_item_state_dict']
                    for i in source['ditto_item_state_dict'].items():
                        result=_get_ditto_shop_name(i[0])
                        row_lst.append([result[0],result[1],_get_stone_shop_state(i[1])])
        return render_to_response("data_edit/ditto_shop_info.html",
                                  {'row_lst': row_lst,'user_id':user_id,'user_openid':user_openid,'user_name':user_name,
                                   'head_lst': head_lst, 'server_list': server_list_dat,'cur_server_id':server_id,'refresh_time':refresh_time}, RequestContext(request))
    else:
        row_lst = []
        return render_to_response("data_edit/ditto_shop_info.html",
                                  {'row_lst': row_lst,
                                   'head_lst': head_lst, 'server_list': server_list_dat}, RequestContext(request))


#世界BOSS商店
def get_world_boss_shop_info(request):
    head_lst = [
        {'width': 50, 'name': u'物品名称'},
        {'width': 50, 'name': u'物品数量'},
        {'width': 50, 'name': u'物品价格（世界BOSS点数）'},
        {'width': 50, 'name': u'是否购买'},
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
        # shop_dict= get_world_boss_shop_config()
        server_id = int(request.POST.get('server_id'))
        type_hidden = 'visible'
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        state_list = game_define.USER_STATE_NAME_DICT
        row_lst=[]
        print user_id
        source=None
        refresh_time=''
        if cmem_url:
            if  len(user_id) <> 0:
                source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_WORLD_BOSS_SHOP_MODEL.format(user_id=user_id))
            elif  len(user_name)<> 0:
                name = hashlib.md5(user_name).hexdigest().upper()
                key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                source = memcache.get_cmem_val(cmem_url,model_define.PLAYER_WORLD_BOSS_SHOP_MODEL.format(user_id=user_uid))
            elif  len(user_openid) <> 0:
                try:
                    result = memcache.get_cmem_val(cmem_url,model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_WORLD_BOSS_SHOP_MODEL.format(user_id=result['uid']))
                except:
                    pass
            if source<> None:
                refresh_time='刷新时间：%s'% source['refresh_datetime'].strftime("%Y-%m-%d %H:%M:%S")
                if 'refresh_num' in source.keys():
                    refresh_time+='，刷新次数:  %s'% source['refresh_num']
                if 'world_boss_shop_point' in source.keys():
                    refresh_time+='，玩家现有世界BOSS点数:  %s'% source['refresh_num']
                if 'data_version' in source.keys():
                    refresh_time+='，数据版本 %s' % source['data_version']
                if len(['shop_item_state_dict'])<>0:
                    for i in source['shop_item_state_dict'].items():
                        result=_get_world_boss_shop_name(i[0],name_dict)
                        row_lst.append([result[0],result[1],result[2],_get_stone_shop_state(i[1])])
        return render_to_response("data_edit/world_boss_shop_info.html",
                                  {'row_lst': row_lst,'user_id':user_id,'user_openid':user_openid,'user_name':user_name,
                                   'head_lst': head_lst, 'server_list': server_list_dat,'cur_server_id':server_id,'refresh_time':refresh_time}, RequestContext(request))
    else:
        row_lst = []
        return render_to_response("data_edit/world_boss_shop_info.html",
                                  {'row_lst': row_lst,
                                   'head_lst': head_lst, 'server_list': server_list_dat}, RequestContext(request))


def get_gym_shop_info(request):
    head_lst = [
        {'width': 50, 'name': u'物品名称'},
        {'width': 50, 'name': u'物品数量'},
        {'width': 50, 'name': u'物品价格（道馆币）'},
        {'width': 50, 'name': u'是否购买'},
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
        name_dict,laji=get_item_config_with_id_name()
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        state_list = game_define.USER_STATE_NAME_DICT
        row_lst=[]
        source=None
        # f=open('/opt/CGameLogserver/apps/game_manager/views/data_edit/USER_DETAIL')
        # d=pickle.load(f)
        # for i in d:
        #     user_id=str(i)
        refresh_time=''
        if cmem_url:
            if  len(user_id) <> 0:
                source = memcache.get_cmem_val(cmem_url, model_define.GYM_SHOP_MODEL.format(user_id=user_id))
            elif  len(user_name)<> 0:
                name = hashlib.md5(user_name).hexdigest().upper()
                key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                source = memcache.get_cmem_val(cmem_url,model_define.GYM_SHOP_MODEL.format(user_id=user_uid))
            elif  len(user_openid) <> 0:
                try:
                    result = memcache.get_cmem_val(cmem_url,model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.GYM_SHOP_MODEL.format(user_id=result['uid']))
                except:
                    pass
            if source<> None:
                refresh_time='刷新时间：%s'% source['refresh_datetime'].strftime("%Y-%m-%d %H:%M:%S")
                if 'refresh_num' in source.keys():
                    # if source['refresh_num']<>0:
                    refresh_time+='，刷新次数:  %s'% source['refresh_num']
                if 'gym_point' in source.keys():
                    refresh_time+='，玩家现在有道馆币：%s' % source['gym_point']
                if len(['item_state_dict'])<>0:
                    for i in source['item_state_dict'].items():
                        result=_get_gym_shop_name(i[0],name_dict)
                        row_lst.append([result[0],result[1],result[2],_get_stone_shop_state(i[1])])
        return render_to_response("data_edit/gym_shop_info.html",
                                  {'row_lst': row_lst,'user_id':user_id,'user_openid':user_openid,'user_name':user_name,
                                   'head_lst': head_lst, 'server_list': server_list_dat,'cur_server_id':server_id,'refresh_time':refresh_time}, RequestContext(request))
    else:
        row_lst = []
        return render_to_response("data_edit/gym_shop_info.html",
                                  {'row_lst': row_lst,
                                   'head_lst': head_lst, 'server_list': server_list_dat}, RequestContext(request))

def _get_gym_shop_name(num,name_dict):
    item= get_gym_shop_config(num)['item']
    name=name_dict[item]
    price=get_gym_shop_config(num)['price']
    shuliang=get_gym_shop_config(num)['itemNum']
    return name,shuliang,price
    #return name,price,star


def _get_pvp_shop_name(num,name_dict,shop_dict):
    #print shop_dict
    for i in shop_dict:
        print i
        if num == i['id']:
            if i['item']<>0:
                return  name_dict[i['item']].encode('utf-8'),str(i['price']).encode('utf-8'),str(i['num']).encode('utf-8')
            else:
                if i['treasureFragmentId'] in treasureFragement.keys():
                    return treasureFragement[i['treasureFragmentId']],str(i['price']).encode('utf-8'),str(i['num']).encode('utf-8')
                else:
                    return  i['treasureFragmentId'],str(i['num']).encode('utf-8'),str(i['price']).encode('utf-8')


def _get_world_boss_shop_name(num,name_dict):
    name=name_dict[get_world_boss_shop_config(num)['item']]
    price=get_world_boss_shop_config(num)['price']
    shuliang=get_world_boss_shop_config(num)['num']
    return name,shuliang,price


def _get_ditto_shop_name(num):
    name=get_monster_config(get_ditto_shop_with_id(num)['monsterId'])['name']
    price=get_ditto_shop_with_id(num)['price']
    star=get_ditto_shop_with_id(num)['star']
    return name,price,star


def _get_stone_shop_name(num,name_dict,shop_dict):
    #print shop_dict
    for i in shop_dict:
        if num == i['id']:
            return name_dict[i['item']],str(i['num']).encode('utf-8'),str(i['price']).encode('utf-8')


def _get_stone_shop_state(num):
    # print num
    if num==0:
        return '未购买'
    else:
        return '已购买'



treasureFragement={
100001:u'红宝石碎片1',
100002:u'红宝石碎片2',
100003:u'红宝石碎片3',
100004:u'优质红宝石碎片1',
100005:u'优质红宝石碎片2',
100006:u'优质红宝石碎片3',
100007:u'优质红宝石碎片4',
100008:u'极品红宝石碎片1',
100009:u'极品红宝石碎片2',
100010:u'极品红宝石碎片3',
100011:u'极品红宝石碎片4',
100012:u'极品红宝石碎片5',
100013:u'能量石碎片1',
100014:u'能量石碎片2',
100015:u'能量石碎片3',
100016:u'优质能量石碎片1',
100017:u'优质能量石碎片2',
100018:u'优质能量石碎片3',
100019:u'优质能量石碎片4',
100020:u'极品能量石碎片1',
100021:u'极品能量石碎片2',
100022:u'极品能量石碎片3',
100023:u'极品能量石碎片4',
100024:u'极品能量石碎片5',
100025:u'紫水晶碎片1',
100026:u'紫水晶碎片2',
100027:u'紫水晶碎片3',
100028:u'优质紫水晶碎片1',
100029:u'优质紫水晶碎片2',
100030:u'优质紫水晶碎片3',
100031:u'优质紫水晶碎片4',
100032:u'极品紫水晶碎片1',
100033:u'极品紫水晶碎片2',
100034:u'极品紫水晶碎片3',
100035:u'极品紫水晶碎片4',
100036:u'极品紫水晶碎片5',
100037:u'蓝宝石碎片1',
100038:u'蓝宝石碎片2',
100039:u'蓝宝石碎片3',
100040:u'优质蓝宝石碎片1',
100041:u'优质蓝宝石碎片2',
100042:u'优质蓝宝石碎片3',
100043:u'优质蓝宝石碎片4',
100044:u'极品蓝宝石碎片1',
100045:u'极品蓝宝石碎片2',
100046:u'极品蓝宝石碎片3',
100047:u'极品蓝宝石碎片4',
100048:u'极品蓝宝石碎片5',
}