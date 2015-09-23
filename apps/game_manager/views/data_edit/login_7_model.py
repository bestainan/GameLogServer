# -*- coding:utf-8 -*-

import datetime
import collections
import hashlib
import json
from django.http import HttpResponse
from django.template import RequestContext
from apps.game_manager.views.log import daily_log
from django.shortcuts import render_to_response
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define
from apps.common.decorators.decorators import require_permission
from apps.config import game_config


@require_permission
def index(request, template):
    """  类型看格式
    author ： 全勇男
    7天登录


    """

    server_list, platform_list = daily_log._get_server_list(None, None)
    server_list.remove(server_list[0])
    if request.method == 'POST':
        user_uid = request.POST.get('user_uid')
        user_name = request.POST.get('user_name').encode('utf-8')
        user_openid = request.POST.get('user_openid')
        server_id = int(request.POST.get('server_id'))
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        try:
            if cmem_url:
                if len(user_uid):
                    source = memcache.get_cmem_val(cmem_url, model_define.LOGIN_7_MODEL.format(user_id=user_uid))
                elif len(user_name):
                    name = hashlib.md5(user_name).hexdigest().upper()
                    key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                    user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    source = memcache.get_cmem_val(cmem_url, model_define.LOGIN_7_MODEL.format(user_id=user_uid))
                elif len(user_openid):
                    result = memcache.get_cmem_val(cmem_url,
                                                   model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.LOGIN_7_MODEL.format(user_id=result['uid']))
                    user_uid = user_id = result['uid']
                row_dict = collections.OrderedDict()

                row_dict = {u'7天登录ID列表': source['reward_id_lst']}
                return render_to_response(template, locals(), RequestContext(request))

        except UnicodeEncodeError:
            return render_to_response(template, locals(), RequestContext(request))

        except TypeError:
            return render_to_response(template, locals(), RequestContext(request))

        except UnboundLocalError:
            return render_to_response(template, locals(), RequestContext(request))

    else:
        row_dict = {}
        return render_to_response(template, locals(), RequestContext(request))
