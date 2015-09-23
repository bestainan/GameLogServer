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
    """  30天签到
    author ： 全勇男
    last_sign_date=None,    # 上次签到日
    cur_reward_index=1,     # 当前领奖序列
    has_double_reward=False,    # 已经领取双倍奖励
    reward_sign_series_id=0,        # 连续签到次数
    has_series_reward=False,    # 30天是否领取奖励

    {'uid': '1000110564',
    'last_sign_date': None,
    'has_double_reward': False, 双倍领奖
    'cur_reward_index': 1,   序号
    'has_series_reward': False,  已经连续奖励
    'reward_sign_series_id': 0}  领奖id
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
                    source = memcache.get_cmem_val(cmem_url, model_define.SIGN_30_MODEL.format(user_id=user_uid))
                    print source
                elif len(user_name):
                    name = hashlib.md5(user_name).hexdigest().upper()
                    key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                    user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    source = memcache.get_cmem_val(cmem_url, model_define.SIGN_30_MODEL.format(user_id=user_uid))
                elif len(user_openid):
                    result = memcache.get_cmem_val(cmem_url,
                                                   model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.SIGN_30_MODEL.format(user_id=result['uid']))
                    user_uid = user_id = result['uid']
                row_dict = collections.OrderedDict()

                row_dict = {u'上次签到日': source['last_sign_date'],
                            u'已经领取双倍奖励': source['has_double_reward'],
                            u'当前领奖序列': source['cur_reward_index'],
                            u'30天是否领取奖励': source['has_series_reward'],
                            u'连续签到次数': source['reward_sign_series_id'], }
                return render_to_response(template, locals(), RequestContext(request))
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
