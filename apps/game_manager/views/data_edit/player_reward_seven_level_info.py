# -*- coding:utf-8 -*-


import time
import collections
import datetime
import hashlib
from django.template import RequestContext

from apps.game_manager.views.log import daily_log
from django.shortcuts import render_to_response
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define, game_define
# from apps.common.decorators.decorators import require_permission
from apps.config import game_config

def get_player_reward_seven_level_info(request):
    """
        玩家开服七天等级
    """
    server_list, platform_list = daily_log._get_server_list(None,None)
    server_list.remove(server_list[0])

    if request.method == 'POST':
        user_uid = request.POST.get("user_uid")
        user_name = request.POST.get("user_name")
        user_openid = request.POST.get("user_openid")
        server_id = int(request.POST.get("server_id"))
        type_hidden = 'visible'
        cmem_url = server_define.CMEM_MAP[int(server_id)]

        if cmem_url:

                source = {}
                if len(user_uid):
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_REWARD_SEVEN_LEVEL_MODEL.format(user_id=user_uid))
                elif len(user_name):
                    name = hashlib.md5(user_name.encode('utf-8')).hexdigest().upper()
                    key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                    user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    source = memcache.get_cmem_val(cmem_url,model_define.PLAYER_REWARD_SEVEN_LEVEL_MODEL.format(user_id=user_uid))
                elif len(user_openid):
                    result = memcache.get_cmem_val(cmem_url, model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    user_uid = result['uid']
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_REWARD_SEVEN_LEVEL_MODEL.format(user_id=user_uid))
                    print source

                if source:
                    each_config_dic ={}
                    reward_lst = source['single_activity_has_reward_lst']
                    new_reward_config_lst = game_config.get_all_reward_seven_level_config()
                    each_config_dic = new_reward_config_lst[str(1)]
                    if reward_lst:
                        for reward_id in reward_lst:
                            each_config_dic = new_reward_config_lst[str(reward_id)]
                            key_lst = new_reward_config_lst['1'].keys()
                            dic = {}
                            lst = []
                            print "沙发沙发沙发",key_lst
                            for each_key in key_lst:
                                lst = []
                                for _key ,_val in new_reward_config_lst.items():
                                    lst.append(_val[each_key])
                                dic[each_key] = lst
                            print "好了没",dic

        return render_to_response("data_edit/player_reward_seven_level_info.html",locals(),RequestContext(request))
    else:
        return render_to_response("data_edit/player_reward_seven_level_info.html",locals(),RequestContext(request))
