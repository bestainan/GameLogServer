# -*- coding:utf-8 -*-

import collections
import hashlib
from django.template import RequestContext
from apps.game_manager.views.log import daily_log
from django.shortcuts import render_to_response
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define
from apps.config import game_config


def get_stage_data_function(request, player_stage_edit):
    """
        玩家关卡数据编辑
        {
        'data_version': '2',
         'stages': {30211: {'num': 0, 'id': 30211, 'rank': -1, 'buy_count': 0},30085: {'num': 0, 'id': 30085, 'rank': 0, 'buy_count': 0},}
        'uid': '1000099826',
        'last_reset_time': datetime.date(2015, 7, 24)
        }
    """
    # 以函数的指针方式传递函数并调用
    function_name = 'data_edit.player_stage_edit.{function}'.format(function=set_stage_data_function.__name__)
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
        type_hidden = 'visible'
        cmem_url = server_define.CMEM_MAP[int(server_id)]

        head_lst = [
            {'name': u'副本名称'},
            {'name': u'攻打次数'},
            {'name': u'是否已开启'},
            {'name': u'重置次数'},
        ]
        if cmem_url:
            try:
                source = dict()

                if len(user_uid):
                    source = memcache.get_cmem_val(cmem_url, model_define.STAGE_MODEL.format(user_id=user_uid))
                    return_uid = user_uid
                elif len(user_name):
                    name = hashlib.md5(user_name).hexdigest().upper()
                    key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                    user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    return_uid = user_uid
                    return_name = user_name
                    source = memcache.get_cmem_val(cmem_url, model_define.STAGE_MODEL.format(user_id=user_uid))
                elif len(user_openid):
                    result = memcache.get_cmem_val(cmem_url, model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    user_uid = result['uid']
                    return_uid = user_uid
                    return_openid = user_openid
                    source = memcache.get_cmem_val(cmem_url, model_define.STAGE_MODEL.format(user_id=return_uid))
                if source:
                    # print 'source', source

                    row_dict = collections.OrderedDict()  # 有序字典

                    for stage_id, stage_state in source['stages'].items():
                        stage_config = game_config.get_stages_config(int(stage_id))
                        try:
                            row_dict[stage_id] = {'name': stage_config['stageInfo'] + '_' + str(stage_config['id']),
                                                  'num': stage_state.get('num', 'None'),
                                                  'rank': stage_state.get('rank', 'None'),
                                                  'buy_count': stage_state.get('buy_count', 'None'),
                                                  }
                        except:
                            print stage_id, stage_state
                return render_to_response(player_stage_edit, locals(), RequestContext(request))

            except UnboundLocalError:
                type_hidden = 'hidden'
                return render_to_response(player_stage_edit, locals(), RequestContext(request))

            except TypeError:
                type_hidden = 'hidden'
                return render_to_response(player_stage_edit, locals(), RequestContext(request))

    else:
        row_list = []
        type_hidden = 'hidden'
        return render_to_response(player_stage_edit, locals(), RequestContext(request))


# @require_permission
def set_stage_data_function(value_dict):
    """
    修改memcache数据

    tem_id 30057$$num
    """
    cmem_url = server_define.CMEM_MAP[int(value_dict['server_id'])]
    if cmem_url:
        if len(value_dict['user_id']):
            source = memcache.get_cmem_val(cmem_url, model_define.STAGE_MODEL.format(user_id=value_dict['user_id']))
            try:
                (first_key, second_key) = value_dict['item_id'].split('$$')
                first_key = int(first_key)
                input_value = int(value_dict['input_value'])
                second_key = str(second_key)
                # print first_key, second_key, input_value

                if 'num' == second_key and 0 <= input_value:
                    source['stages'][first_key][second_key] = input_value
                elif 'rank' == second_key and (0 == input_value or -1 == input_value):
                    source['stages'][first_key][second_key] = input_value
                elif 'buy_count' == second_key and 0 <= input_value:
                    source['stages'][first_key][second_key] = input_value
                else:
                    return False
            except:
                return False
            # 传回 url  uid  以及数据 做外层检测
            result = memcache.put_cmem_val(cmem_url, model_define.STAGE_MODEL.format(user_id=value_dict['user_id']), source)
            return result