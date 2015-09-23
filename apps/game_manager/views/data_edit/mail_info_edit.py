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
from apps.utils.mem_key_name import  MEM_KEY_NAME,FORBIDE_CHANGE_VALUES
import hashlib
import time



# 获取角色信息，在utils文件夹下有一个meme_key_name函数，来规定各个关键字的名字和全局不可修改关键字
@require_permission
def get_mail_info(request):
    head_lst = [
        {'width': 50, 'name': u'标题'},
        {'width': 50, 'name': u'发送时间'},
        {'width': 50, 'name': u'有效期至'},
        ]
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
        print user_id
        if cmem_url:
            if len(user_id) <> 0:
                source = memcache.get_cmem_val(cmem_url, model_define.MAIL_MODEL.format(user_id=user_id))
                print source,'source'
                row_lst = _get_player_mem(source,user_id,server_id)
            elif len(user_name)<> 0:
                name = hashlib.md5(user_name).hexdigest().upper()
                key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                source = memcache.get_cmem_val(cmem_url,model_define.MAIL_MODEL.format(user_id=user_uid))
                row_lst = _get_player_mem(source,user_id,server_id)
            elif len(user_openid) <> 0:
                try:
                    result = memcache.get_cmem_val(cmem_url,model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.MAIL_MODEL.format(user_id=result['uid']))
                    row_lst = _get_player_mem(source,user_id,server_id)
                except:
                    pass
        return render_to_response("data_edit/mail_info_edit.html",
                                  {'row_lst': row_lst,'user_id':user_id,'user_openid':user_openid,'user_name':user_name,
                                   'head_lst': head_lst, 'server_list': server_list_dat,'cur_server_id':server_id}, RequestContext(request))
    else:
        row_lst = []
        return render_to_response("data_edit/mail_info_edit.html",
                                  {'row_lst': row_lst,
                                   'head_lst': head_lst, 'server_list': server_list_dat,}, RequestContext(request))


def _get_player_mem(source,user_id,server_id):
    row_lst=[]
    if source <> None:
        if len(source['system_mail']) <> 0:
            for line in source['system_mail']:
                row_lst.append([line['title'],str(line['send_time']),str(line['expiry_date'])])
    return row_lst

