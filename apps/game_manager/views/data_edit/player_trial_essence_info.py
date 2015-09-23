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

def get_player_trial_essence_info(request):
    """
        玩家熔炼精华
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
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_TRIAL_ESSENCE_MODEL.format(user_id=user_uid))
                elif len(user_name):
                    name = hashlib.md5(user_name.encode('utf-8')).hexdigest().upper()
                    key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                    user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    source = memcache.get_cmem_val(cmem_url,model_define.PLAYER_TRIAL_ESSENCE_MODEL.format(user_id=user_uid))
                elif len(user_openid):
                    result = memcache.get_cmem_val(cmem_url, model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    user_uid = result['uid']
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_TRIAL_ESSENCE_MODEL.format(user_id=user_uid))
                    print source

                if source:
                    refresh_datetime = source['refresh_datetime'].strftime('%Y-%m-%d %H:%M:%S')
                    refresh_datetime_lst = [refresh_datetime]

                    new_row_lst = []
                    row_lst = source['cur_enemy_dat']
                    print row_lst
                    refresh_time = row_lst[0]
                    last_refresh_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(refresh_time)))
                    last_refresh_time_lst = [last_refresh_time]
                    rand_enemy_num = int(row_lst[1])
                    rand_level_result = row_lst[2]
                    rand_individual = row_lst[3]
                    rand_star_result = row_lst[4]
                    new_member_lst = ""
                    member_lst = [row_lst[5],row_lst[6],row_lst[7],row_lst[8],row_lst[9]]
                    for i in member_lst:
                        new_member_lst += (game_config.get_monster_config(int(i))['name']).encode('utf-8')+'\t、'

                    row_list_append = [rand_enemy_num,rand_level_result,rand_individual,rand_star_result,str(new_member_lst)]
                    new_row_lst.extend(row_list_append)

                    print new_row_lst
                    all_items_lst = []
                    if refresh_datetime_lst:
                        all_items_lst.append(refresh_datetime_lst)
                    if last_refresh_time_lst:
                        all_items_lst.append(last_refresh_time_lst)
                    if new_row_lst:
                        all_items_lst.extend(new_row_lst)



        return render_to_response("data_edit/player_trial_essence_info.html",locals(),RequestContext(request))
    else:
        return render_to_response("data_edit/player_trial_essence_info.html",locals(),RequestContext(request))
