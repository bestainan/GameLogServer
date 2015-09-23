# -*- coding:utf-8 -*-

import datetime
import collections
import hashlib
from django.template import RequestContext
from apps.game_manager.views.log import daily_log
from django.shortcuts import render_to_response
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define
from apps.common.decorators.decorators import require_permission
from apps.config import game_config


def get_everyday_vip_reward_function(request, everyday_vip_reward):
    """
        每日VIP奖励时间
        {'uid': '1000099826', 'reward_date': None}
    """
    # 以函数的指针方式传递函数并调用
    """注： 每日vip不处理数据只显示"""
    # function_name = 'data_edit.everyday_vip_reward.{function}'.format(function=set_everyday_vip_reward_data_function.__name__)
    server_list, platform_list = daily_log._get_server_list(None, None)
    try:
        server_list.remove(server_list[0])
    except:
        pass

    return_uid = '请输入uid'
    return_openid = "请输入openid"
    return_name = "请输入玩家昵称"
    if request.method == 'POST':
        user_uid = request.POST.get('user_uid')
        user_name = request.POST.get('user_name').encode('utf-8')
        user_openid = request.POST.get('user_openid')
        server_id = int(request.POST.get('server_id'))
        cmem_url = server_define.CMEM_MAP[int(server_id)]

        head_lst = [
            {'name': u'VIP_uid'},
            {'name': u'领取时间'},
        ]
        if cmem_url:
            try:
                source = dict()
                
                if len(user_uid):
                    source = memcache.get_cmem_val(cmem_url, model_define.DAILY_VIP_REWARD_MODEL.format(user_id=user_uid))
                    return_uid = user_uid
                elif len(user_name):
                    name = hashlib.md5(user_name).hexdigest().upper()
                    key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                    user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    return_uid = user_uid
                    return_name = user_name
                    source = memcache.get_cmem_val(cmem_url, model_define.DAILY_VIP_REWARD_MODEL.format(user_id=user_uid))
                elif len(user_openid):
                    result = memcache.get_cmem_val(cmem_url, model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    user_uid = result['uid']
                    return_uid = user_uid
                    return_openid = user_openid
                    source = memcache.get_cmem_val(cmem_url, model_define.DAILY_VIP_REWARD_MODEL.format(user_id=return_uid))
                if source:
                    # print 'source', source
                    import copy
                    _source = copy.deepcopy(source)
                    if _source['reward_date']:
                        _source['reward_date'] = _source['reward_date'].strftime('%Y-%m-%d')
                    else:
                        _source['reward_date'] = u'今天还未领取'
                    row_dict = collections.OrderedDict()  # 有序字典
                    row_dict = [_source]
                    # print row_dict, "llllllllllllllllllllllll", source
                return render_to_response(everyday_vip_reward, locals(), RequestContext(request))

            except UnboundLocalError:
                type_hidden = 'hidden'
                return render_to_response(everyday_vip_reward, locals(), RequestContext(request))

            except TypeError:
                type_hidden = 'hidden'
                return render_to_response(everyday_vip_reward, locals(), RequestContext(request))

    else:
        row_list = []
        type_hidden = 'hidden'
        return render_to_response(everyday_vip_reward, locals(), RequestContext(request))


# @require_permission
def set_everyday_vip_reward_data_function(value_dict):
    """
    修改memcache数据 每日VIP奖励
    不修改
    """
    cmem_url = server_define.CMEM_MAP[int(value_dict['server_id'])]
    if cmem_url:
        if len(value_dict['user_id']):
            source = memcache.get_cmem_val(cmem_url, model_define.DAILY_VIP_REWARD_MODEL.format(user_id=value_dict['user_id']))

            # 传回 url  uid  以及数据 做外层检测
            result = memcache.put_cmem_val(cmem_url, model_define.DAILY_VIP_REWARD_MODEL.format(user_id=value_dict['user_id']), source)
            return result