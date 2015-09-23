# -*- coding:utf-8 -*-


from django.template import RequestContext
from django.shortcuts import render_to_response
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define,game_define
from apps.common.decorators.decorators import require_permission
from apps.game_manager.mysql.server_list import get_server_list_dat
from apps.config.game_config import get_all_invitation_reward_config,get_monster_config
import hashlib



# 获取玩家试炼信息
@require_permission
def get_player_invitation_info(request):
    head_lst = [
        {'width': 50, 'name': u'谁的邀请'},
        {'width': 50, 'name': u'对方UID'},
        {'width': 50, 'name': u'对方等级'},
        {'width': 50, 'name': u'是否有奖励'},
        {'width': 50, 'name': u'奖励内容'}
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
        # print user_id
        # source=None
        # f=open('/opt/CGameLogserver/apps/game_manager/views/data_edit/USER_DETAIL')
        # d=pickle.load(f)
        # for i in d:
        #     user_id=str(i)
        name_dict=get_all_invitation_reward_config()
        if cmem_url:
            if  len(user_id) <> 0:
                source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_INVITATION_MODEL.format(user_id=user_id))
                #print source,'source'
            elif  len(user_name)<> 0:
                name = hashlib.md5(user_name).hexdigest().upper()
                key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                source = memcache.get_cmem_val(cmem_url,model_define.PLAYER_INVITATION_MODEL.format(user_id=user_uid))
            elif  len(user_openid) <> 0:
                try:
                    result = memcache.get_cmem_val(cmem_url,model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_INVITATION_MODEL.format(user_id=result['uid']))
                except:
                    pass
            if source:
                if source['invite_me']<>0:
                    row_lst.append(['该玩家被邀请',source['uid'],'','',''])
                if len(source['i_invite_dict'])<>0:
                    for i in source['i_invite_dict'].keys():
                        if i in source['i_invite_has_reward_lst_dict'].keys():
                            row_lst.append(['该玩家向他人发出的邀请',i,source['i_invite_dict'][i],'是',_get_reward(source['i_invite_has_reward_lst_dict'][i],name_dict)])
                        else:
                             row_lst.append(['该玩家向他人发出的邀请',i,source['i_invite_dict'][i],'否',''])
        return render_to_response("data_edit/player_invitation_info.html",
                                  {'row_lst': row_lst,'user_id':user_id,'user_openid':user_openid,'user_name':user_name,
                                   'head_lst': head_lst, 'server_list': server_list_dat,'cur_server_id':server_id}, RequestContext(request))
    else:
        row_lst = []
        return render_to_response("data_edit/player_invitation_info.html",
                                  {'row_lst': row_lst,
                                   'head_lst': head_lst, 'server_list': server_list_dat}, RequestContext(request))



def _get_reward(reward,name_dict):
    monster=''
    gold=''
    stone=''
    for i in reward:
        info=name_dict[i]
        if info['monsterId']<>0:
            monster +='%s星宠物%s' % (str(name_dict[i][u'monsterStar']).encode('utf-8'),get_monster_config(info['monsterId'])['name'].encode('utf-8'))
        if info['gold']<>0:
            gold += '金币%s' % str(info['gold']).encode('utf-8')
        if info['stone']<>0:
            stone+= '钻石%s' % str(info['stone']).encode('utf-8')
    return monster+'\n'+gold+'\n'+stone