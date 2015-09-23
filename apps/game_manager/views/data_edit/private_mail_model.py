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
    """  玩家私信
    author ： 全勇男
    {'new_label': True, #已读未读
    'private_mail': [{'content': u'\u6211\u5df2\u7ecf\u63a5\u53d7\u4e86\u60a8\u7684\u597d\u53cb\u9080\u8bf7\uff0c\u5927\u5bb6\u4e00\u8d77\u73a9\u800d\u5427\uff01',
    'name': '\xe4\xb8\xa4\xe5\x9d\x97\xe4\xba\x94',
    'time': 1438328576.698478},
    {'content': 'fkjdshfkdsfdsf ',
    'name': '\xe4\xb8\xa4\xe5\x9d\x97\xe4\xba\x94',
    'time': 1438328605.817033},
    {'content': 'wenni fdfg dg dg dgd',
    'name': '\xe4\xb8\xa4\xe5\x9d\x97\xe4\xba\x94',
    'time': 1438328616.180619},
    {'content': 'dgdf gdfg d',
    'name': '\xe4\xb8\xa4\xe5\x9d\x97\xe4\xba\x94',
    'time': 1438328619.498057},
    {'content': 'dg dgdg dgdgd d',
    'name': '\xe4\xb8\xa4\xe5\x9d\x97\xe4\xba\x94',
    'time': 1438328623.004101},
    {'content': 'gfhgfhfh gfhfh d h',
    'name': '\xe4\xb8\xa4\xe5\x9d\x97\xe4\xba\x94',
    'time': 1438328626.179098},
    {'content': 'hgf hf hgf ',
    'name': '\xe4\xb8\xa4\xe5\x9d\x97\xe4\xba\x94',
    'time': 1438328629.125485}],
    'uid': '1000110564'}
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
                    mail_dict = memcache.get_cmem_val(cmem_url, model_define.PRIVATE_MAIL_MODEL.format(user_id=user_uid))

                elif len(user_name):
                    name = hashlib.md5(user_name).hexdigest().upper()
                    key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                    user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    mail_dict = memcache.get_cmem_val(cmem_url, model_define.PRIVATE_MAIL_MODEL.format(user_id=user_uid))
                elif len(user_openid):
                    result = memcache.get_cmem_val(cmem_url,
                                                   model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    mail_dict = memcache.get_cmem_val(cmem_url, model_define.PRIVATE_MAIL_MODEL.format(user_id=result['uid']))

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


