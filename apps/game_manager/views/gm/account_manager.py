# -*- coding:utf-8 -*-

import pickle
from apps.game_manager.models.game_manager import *
from apps.utils.encryption import decrypt
from apps.game_manager.util import memcache
from apps.utils import server_define
from apps.utils import model_define
from apps.game_manager.mysql import server_list
from django.http import HttpResponseRedirect
from django.template import RequestContext
from apps.utils.game_define import USER_STATE_FREEZE,USER_STATE_NAME_DICT

from apps.common.decorators.decorators import require_permission

@require_permission
def acount_release_forbiden(request):
    """
    聊天信息统计
    """
    # _gm = GameManager()
    # btn_lst = _gm.check_admin_permission()
    #server_id =  request.POST.get('server_id')

    # manager = GameManager.get_by_request(request)
    # btn_lst = manager.check_admin_permission()
    # if btn_lst:
    head_lst = [
        {'width': 70, 'name': u'OPEN_ID'},
        {'width': 50, 'name': u'UID'},
        {'width': 55, 'name': u'昵称'},
        {'width': 50, 'name': u'等级'},
        {'width': 50, 'name': u'VIP等级'},
        {'width': 50, 'name': u'当前金币'},
        {'width': 50, 'name': u'当前钻石'},
        {'width': 50, 'name': u'当前经验'},
        {'width': 50, 'name': u'当前状态'},
    ]
    server_list_dat = server_list.get_server_list_dat()
    print server_list_dat
    #print server_list_dat
    change_lst=[{'id':3,'name':u'查询'},{'id':-1,'name':u'解封'},{'id':1,'name':u'封禁'},{'id':2,'name':u'内部账号'}]
    # for i in USER_STATE_NAME_DICT.items():
    #     print i, i[1][0:-1]
    #     change_lst.append({'id':i[0],'name':i[1][0:-4]})
    # print change_lst
    if request.method == 'POST':
        user_id=request.POST.get('user_id')
        server_id=request.POST.get('server_id')
        #submit_value=request.POST.get('submit_value')
        change_id=request.POST.get('change_id')
        cmem_url=server_define.CMEM_MAP[int(server_id)]
        row_lst=[]
        if cmem_url:
            if int(change_id)==3:
                try:
                    row_lst=_get_imformation(user_id,cmem_url)
                except:
                    row_lst=[]
            else:
                try:
                    _set_state(user_id,int(change_id),cmem_url)
                    row_lst=_get_imformation(user_id,cmem_url)
                except:
                    row_lst=[]
        return render_to_response("gm/account_release_forbiden.html",
                                  # {'account': manager.account, 'btn_lst': btn_lst,
                                   {'row_lst': row_lst,
                                   'head_lst': head_lst, 'server_list': server_list_dat,'cur_server_id':server_id,'change_list':change_lst}, RequestContext(request))
    else:
        return render_to_response("gm/account_release_forbiden.html",
                                  # {'account': manager.account, 'btn_lst': btn_lst,
                                   {'row_lst': [],
                                   'head_lst': head_lst, 'server_list': server_list_dat,'change_list':change_lst},RequestContext(request))
    # else:
    #     return HttpResponseRedirect('/Tyranitar6/login/')


#获取玩家的状态信息
def _get_imformation(user_id,cmem_url):
    user_info1=memcache.get_cmem_val(cmem_url,model_define.USER_MODEL.format(user_id=user_id))
    user_info = memcache.get_cmem_val(cmem_url,model_define.PLAYER_MODEL.format(user_id=user_id))
    user_info1.update(user_info)
    #print user_info1['state'],type(user_info1['state'])
    state=USER_STATE_NAME_DICT[user_info1['state']]
    row_lst=[[user_info1['openid'],user_info1['uid'],user_info1['name'],user_info1['level'],user_info1['vip_level'],user_info1['gold'],user_info1['stone'],
             user_info1['exp'],state]]
    return row_lst


#设置玩家的状态
def _set_state(user_id,change_id,cmem_url):
    user_state=memcache.get_cmem_val(cmem_url,model_define.USER_MODEL.format(user_id=user_id))
    user_state['state']=change_id
    a=memcache.put_cmem_val(cmem_url,model_define.USER_MODEL.format(user_id=user_id),user_state)