# -*- coding:utf-8 -*-

import hashlib
from django.template import RequestContext
from apps.game_manager.views.log import daily_log
from django.shortcuts import render_to_response
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define
from apps.common.decorators.decorators import require_permission
from apps.config import game_config
from apps.utils.Robot_function import get_dict_key_with_value

@require_permission
def index(request, template):
    """  玩家联盟商店
    author ： 全勇男
    get_union_shop_items_config

    {'uid': '1000110564',
    'union_item_lst': [12, 15, 35, 53, 70, 76], # 商店商品列表
    'union_item_state_dict': {35: 0, 70: 0, 12: 0, 76: 0, 15: 0, 53: 0}, # 物品状态
    'reward_date': datetime.date(2015, 8, 1),
    'refresh_date': datetime.datetime(2015, 8, 1, 13, 3, 25, 588918), #最后刷新时间
    'refresh_num': 4} #刷新次数

    """
    server_list, platform_list = daily_log._get_server_list(None, None)
    server_list.remove(server_list[0])

    if request.method == 'POST':
        user_uid = request.POST.get('user_uid')
        user_name = request.POST.get('user_name').encode('utf-8')
        user_openid = request.POST.get('user_openid')
        server_id = int(request.POST.get('server_id'))
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        row_lst = []
        try:
            if cmem_url:
                if len(user_uid):
                    source = memcache.get_cmem_val(cmem_url, model_define.UNION_SHOP_MODEL.format(user_id=user_uid))

                elif len(user_name):
                    name = hashlib.md5(user_name).hexdigest().upper()
                    key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                    user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    source = memcache.get_cmem_val(cmem_url, model_define.UNION_SHOP_MODEL.format(user_id=user_uid))
                elif len(user_openid):
                    result = memcache.get_cmem_val(cmem_url,
                                                   model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.UNION_SHOP_MODEL.format(user_id=result['uid']))
                for item_num in source['union_item_lst']:
                    item_name = game_config.get_item_config(game_config.get_union_shop_items_by_num(item_num))['name']

                    print item_name
                    row_lst.append( [
                        source['reward_date'],
                        item_name,
                        source['union_item_state_dict'][item_num]])
                    print row_lst
                last_refresh = source['refresh_date']
                refresh_count = source['refresh_num']
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




