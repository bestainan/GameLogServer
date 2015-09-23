# -*- coding:utf-8 -*-

import datetime
import collections
import hashlib
from django.template import RequestContext
from apps.game_manager.views.log import daily_log
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define, game_define
from apps.config import game_config
from apps.common.decorators.decorators import require_permission


# @require_permission
def get_handbook_info(request):
    """
    {'data_version': '1', 'uid': '1000070187', 'monster_tid_set': set([32, 66, 4, 104, 93, 146, 52, 126, 25, 27, 92, 125, 94, 127])}
    """

    server_list, platform_list = daily_log._get_server_list(None, None)
    server_list.remove(server_list[0])
    if request.method == 'POST':
        user_uid = request.POST.get('user_uid')
        # user_name = request.POST.get('user_name').encode('utf-8')
        # user_openid = request.POST.get('user_openid')
        server_id = request.POST.get('server_id')
        # type_hidden = 'visible'
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        handbook_model = memcache.get_cmem_val(cmem_url, model_define.HAND_BOOK_MODEL.format(user_id=int(user_uid)))
        print handbook_model
        table_lst = []
        for uid in handbook_model['monster_tid_set']:
            monster_name_lst = []
            _monster_config = game_config.get_monster_config(uid)
            monster_name_lst.append(uid)
            monster_name_lst.append(_monster_config['name'])
            table_lst.append(monster_name_lst)

        return render_to_response("data_edit/handbook_info.html", {'row_lst': table_lst}, RequestContext(request))

    else:
        # row_list = []
        # type_hidden = 'hidden'
        return render_to_response("data_edit/handbook_info.html", locals(), RequestContext(request))
