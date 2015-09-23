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
from apps.utils.mem_key_name import  MEM_KEY_NAME,FORBIDE_CHANGE_VALUES
import hashlib
import time
from apps.logs.output_action_gm import *
from apps.game_manager.models.game_manager import GameManager
from apps.config.game_config import get_newbie_phase_config,get_the_title_config,get_reward_monster_kind_config,get_monster_config,get_stages_config,\
    get_reward_monster_quality_config,get_reward_team_power,get_fried_num_config,get_reward_monster_level_config,get_reward_monster_star_level_config



# 获取角色信息，在utils文件夹下有一个meme_key_name函数，来规定各个关键字的名字和全局不可修改关键字
@require_permission
def get_player_info(request):
    # head_lst = [
    #     {'width': 50, 'name': u'名称'},
    #     {'width': 50, 'name': u'当前值'},
    #     {'width': 50, 'name': u'修改'},
    #     ]
    server_list_dat = get_server_list_dat()
    if request.method == 'POST':
        user_id = request.POST.get('user_uid')
        user_name = request.POST.get('user_name').encode('utf-8')

        try:
            user_openid = str(request.POST.get('user_openid'))
        except UnicodeEncodeError :
            user_openid = ''
        server_id = int(request.POST.get('server_id'))
        type_hidden = 'visible'
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        state_list = game_define.USER_STATE_NAME_DICT
        row_lst=[]
        if cmem_url:
            if  len(user_id) <> 0:
                source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_MODEL.format(user_id=user_id))
                if source:
                    user_id=source['uid']
                    row_lst = _get_player_mem(source,user_id,server_id)
            elif len(user_name)<> 0:
                name = hashlib.md5(user_name).hexdigest().upper()
                key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                source = memcache.get_cmem_val(cmem_url,model_define.PLAYER_MODEL.format(user_id=user_uid))
                if source:
                    user_id=source['uid']
                    row_lst = _get_player_mem(source,user_id,server_id)
            elif len(user_openid) <> 0:
                try:
                    result = memcache.get_cmem_val(cmem_url,model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_MODEL.format(user_id=result['uid']))
                    if source:
                        user_id=source['uid']
                        row_lst = _get_player_mem(source,user_id,server_id)
                except:
                    pass
            else:
                row_lst = []
            return render_to_response("data_edit/player_info_edit.html",
                                      {'row_lst': row_lst,
                                        'server_list': server_list_dat,'cur_server_id':server_id}, RequestContext(request))
    else:
        row_lst = []
        return render_to_response("data_edit/player_info_edit.html",
                                  {'row_lst': row_lst,
                                    'server_list': server_list_dat,}, RequestContext(request))

#为player_change页面提供数据
@require_permission
def get_player_data(request):
    '''
    返回修改后的数据
    '''
    if request.method == 'POST':
        server=request.POST.get('server')
        key=request.POST.get('key')
        value=request.POST.get('value')
        uid=request.POST.get('uid')
        typ=request.POST.get('type')
        key_name=request.POST.get('key_name')
        name=request.POST.get('name')
        # print uid
        # print server
        # print request.POST
        #print server,key,value,uid,type,key_name,name
        return render_to_response('data_edit/player_change.html',{'server_id':server,'key':key,'value':value,'uid':uid,
                                                                  'name':name,
                                                                 'type':typ,'key_name':key_name})


#为player_change页面提供修改数据，当修改完成后自动跳回角色信息界面
@require_permission
def set_player_data(request):
    # 获取管理员信息
    manager = GameManager.get_by_request(request)
    head_lst = [
        #{'width': 50, 'name': u'UID'},
        {'width': 50, 'name': u'名称'},
        {'width': 50, 'name': u'当前值'},
        {'width': 50, 'name': u'修改'},
        ]
    server_list_dat = get_server_list_dat()
    if request.method == 'POST':
        print request.POST,'post'
        user_id=request.POST.get('user_id')
        server_id=int(request.POST.get('server_id'))
        typ=request.POST.get('type')
        value=request.POST.get('value')
        #print 'value',value
        if value <> '':
            if typ <> 'str':
                if typ=='bool':
                    value=eval(typ)(eval(value))
                else:
                    value=eval(typ)(value)
                #print value
        key=request.POST.get('key')
        data=''
        if key=='newbie':
            # print 'newbie'
            # print int(value)
            # print get_newbie_phase_config(int(value))
            if get_newbie_phase_config(int(value))==None:
                data='新手引导ID应在1~5之间'
        elif key=='gold':
            pass
        elif key=='champion_index':
            if int(value) not in [1,2,3,4,0]:
                data='冠军宠物位置应该在0~4之间'
        elif key=='reward_cur_monster_star_level_id':
            if get_reward_monster_star_level_config(int(value))==None:
                data=u'宠物等级奖励序列应在1~18之间'
        elif key=='universal_fragment':
            pass
        elif key=='title':
            if get_the_title_config(int(value))==None:
                data='玩家爵位应在1~21之间'
        elif key=='consumption_point':
            pass
        elif key=='role_id':
            pass
        elif key=='reward_login_series_id':
            pass
        elif key=='reward_cur_monster_kind_id':
            if get_reward_monster_kind_config(int(value))==None:
                data='宠物种类奖励序列应在1~18之间'
        elif key=='has_first_recharge_lst':
            pass
        elif key=='is_stone_one_draw':
            if int(value) not in [0,1]:
                 data='首次钻石单抽状态取值应为0或1，0代表未抽过，1代表抽过'
        elif key=='is_ten_draw':
            if int(value) not in [0,1]:
                data='首次钻石十连抽状态取值应为0或1，0代表未抽过，1代表抽过'
        elif key=='champion_tid':
            cmem_url=server_define.CMEM_MAP[int(server_id)]
            source=memcache.get_cmem_val(cmem_url,model_define.MONSTER_MODEL.format(user_id=user_id))
            # print source['monsters']
            sign=0
            for i in source['monsters']:
                if int(value) == i['tid']:
                    sign=1
            # print sign
            if sign==0:
                data=u'输入的宠物id不属于玩家拥有的宠物之一，请正确输入，玩家现有宠物:'
                for i in source['monsters']:
                    a='(%s:%s)'% (i['tid'],get_monster_config(i['tid'])['name'])
                    data+=a
        elif key=='champion_power':
            pass
        elif key=='name':
            pass
        elif key=='level':
            if int(value)>120 or int(value)<1:
                data=u'玩家等级应在1~120级之间，请输入正确的值'
        elif key=='cur_stage':
            if get_stages_config(int(value))==None:
                data=u'关卡ID输入错误'
        elif key=='reward_cur_monster_quality_id':
            if get_reward_monster_quality_config(int(value))==None:
                data=u'当前宠物品质奖励序列应在1~3之间'
        elif key=='reward_cur_team_combat_power_id':
            if get_reward_team_power(int(value))==None:
                data=u'当前队伍战斗力奖励序列应在1~47之间'
        elif key=='reward_friend_num_id':
            if get_fried_num_config(int(value))==None:
                data=u'好友数量奖励序列应在1~6之间'
        elif key=='reward_cur_monster_level_id':
            if get_reward_monster_level_config(int(value))==None:
                data=u'宠物等级奖励序列应在1~10之间'

        if value <> ''and data=='':
            # print "i'work"
            cmem_url=server_define.CMEM_MAP[int(server_id)]
            if cmem_url:
                source=memcache.get_cmem_val(cmem_url,model_define.PLAYER_MODEL.format(user_id=user_id))
                if eval(typ)==type(value) or (typ=='str' and type(value)==unicode) :
                    #print source,key,value,user_id,type(user_id)
                    old_value = source[key]
                    source[key]=value
                    memcache.put_cmem_val(cmem_url,model_define.PLAYER_MODEL.format(user_id=user_id),source)
                    # 操作日志记录
                    insert_action_edit_player(manager, str(server_id), str(user_id), key, old_value, value)
        return HttpResponse(data)



#获取角色的MEMCACHE信息，并进行一定的处理，以方便其他函数的调用和处理
def _get_player_mem(source,user_id,server_id):
    row_lst=[]
    if source <> None:
        # source
        name=source['name']
        for line in source:
            if type(source[line]) == datetime.datetime or type(source[line])==type(None) or type(source[line])==datetime.date or ('time' in line and type(source[line])==float)\
                    or line == 'honour_point_datetime':
                if type(source[line])==type(None):
                    value=datetime.datetime.now().strftime('%m/%d/%Y-%H:%M:%S')
                    row_lst.append({'key':line,'value':value,'type':'No',})
                elif type(source[line]) == datetime.datetime:
                    value=source[line].strftime('%m/%d/%Y-%H:%M:%S')
                    row_lst.append({'key':line,'value':value,'type':'No'})
                elif ('time' in line) and (type(source[line])==float):
                    value=time.strftime('%m/%d/%Y-%H:%M:%S',time.localtime(source[line]))
                    row_lst.append({'key':line,'value':value,'type':'No'})
                elif line == 'honour_point_datetime':
                    if source[line]==0:
                        row_lst.append({'key':line,'value':source[line],'type':'No'})
                    else:
                        value=source[line].strftime('%m/%d/%Y-%H:%M:%S')
                        row_lst.append({'key':line,'value':value,'type':'No'})
                else:
                    value=source[line].strftime('%m/%d/%Y')
                    row_lst.append({'key':line,'value':value,'type':'No'})
                # value=source[line].strftime('%m/%d/%Y-%H:%M:%S')
                # row_lst.append({'key':line,'value':value,'type':'No'})
            else:
                if type(source[line])== list:
                    row_lst.append({'key':line,'value':source[line],'type':'No'})
                else:
                    row_lst.append({'key':line,'value':source[line],'type':(str(type(source[line])).split("'"))[1]})
        a=0
        for row in row_lst:
            row['key_name']= MEM_KEY_NAME[row['key']]
            row['name']=name
            row['uid']=user_id
            row['server']= server_id
            if row['key'] in FORBIDE_CHANGE_VALUES:
                row_lst[a]['type']="No"
            a+=1

    return row_lst


