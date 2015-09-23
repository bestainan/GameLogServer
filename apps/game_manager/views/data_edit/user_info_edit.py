# -*- coding:utf-8 -*-

import datetime
import collections
import hashlib
from django.template import RequestContext
from apps.game_manager.views.log import daily_log
from django.shortcuts import render_to_response
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define, game_define
from apps.common.decorators.decorators import require_permission


@require_permission
def index(request, template):
    """
    数据后台 --- 用户管理

    搜索 显示 memcahe 抓去到的信息

    source['openid']                    <type 'str'>
    source['last_login_time']           <type 'int'>
    source['last_login_cookie_time']    <type 'int'>
    source['platform_id']               <type 'int'>
    source['state']                     <type 'int'>
    source['last_login_distance_days']  <type 'int'>
    source['add_time']                  <type 'datetime.datetime'>
    source['last_player_time']          <type 'float'>
    source['name']                      <type 'str'>
    source['uid']                       <type 'int'>
    """

    server_list, platform_list = daily_log._get_server_list(None, None)
    server_list.remove(server_list[0])
    if request.method == 'POST':

        user_uid = request.POST.get('user_uid')
        user_name = request.POST.get('user_name').encode('utf-8')
        user_openid = request.POST.get('user_openid')
        server_id = int(request.POST.get('server_id'))

        type_hidden = 'visible'
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        state_list = game_define.USER_STATE_NAME_DICT


        if cmem_url:
            try:
                if len(user_uid):
                    source = memcache.get_cmem_val(cmem_url, model_define.USER_MODEL.format(user_id=user_uid))
                elif len(user_name):
                    name = hashlib.md5(user_name).hexdigest().upper()
                    key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                    user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    source = memcache.get_cmem_val(cmem_url,model_define.USER_MODEL.format(user_id=user_uid))
                    print source
                elif len(user_openid):
                    result = memcache.get_cmem_val(cmem_url,model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.USER_MODEL.format(user_id=result['uid']))

                state_id = source['state']

                date_array = datetime.datetime.utcfromtimestamp(source.get('last_player_time',0))
                last_player_time = date_array.strftime("%Y-%m-%d %H:%M:%S")
                if last_player_time == '1970-01-01 00:00:00':
                    last_player_time = 'None'
                row_dict = collections.OrderedDict()
                row_dict[u'uid'] = {'name': u'UID', 'value': source.get('uid','None')}
                row_dict[u'openid'] = {'name': u'OpenID', 'value': source.get('openid','None')}
                row_dict[u'add_time'] = {'name': u'安装时间', 'value': source.get('add_time','None')}
                row_dict[u'platform_id'] = {'name': u'玩家平台', 'value': source.get('platform_id','None')}
                row_dict[u'last_player_time'] = {'name': u'最后游戏时间', 'value': last_player_time}
                row_dict[u'state'] = {'name': u'当前状态', 'value': source.get('state','None')}
                return render_to_response(template, locals(), RequestContext(request))
            except UnicodeEncodeError:
                return render_to_response(template, locals(), RequestContext(request))

            except TypeError:
                return render_to_response(template, locals(), RequestContext(request))

            except UnboundLocalError:
                return render_to_response(template, locals(), RequestContext(request))

    else:
        row_list = []
        type_hidden = 'hidden'
        return render_to_response(template, locals(), RequestContext(request))


@require_permission
def set_user_memcache(request, template):
    '''
    返回修改后的数据
    '''
    server_list, platform_list = daily_log._get_server_list(None, None)

    if request.method == 'POST':
        state = int(request.POST.get('state'))
        uid = request.POST.get('uid')
        server_id = int(request.POST.get('server_id'))
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        if cmem_url:
            source = memcache.get_cmem_val(cmem_url, model_define.USER_MODEL.format(user_id=uid))
            source['state'] = state
            a = memcache.put_cmem_val(cmem_url, model_define.USER_MODEL.format(user_id=uid), source)
        type_hidden = 'hidden'
        return render_to_response(template, locals(), RequestContext(request))
    else:
        row_list = []
        return render_to_response(template, locals(), RequestContext(request))
