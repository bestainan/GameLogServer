# -*- coding:utf-8 -*-


# import sys
import collections
import hashlib
from django.template import RequestContext
from apps.game_manager.views.log import daily_log
from django.shortcuts import render_to_response
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define, game_define
# from apps.common.decorators.decorators import require_permission
from apps.config import game_config

STAGE_PASS_NAME = {
    0: u'完美金冠通关',
    -1: u'未通关',
    # None: u'已通关',
}
REWARD_NAME= {
    True: u'奖励已领取',
    False: u'奖励未领取',
}

# @require_permission
def index(request,zone_info_edit):
    """
        玩家区域查询
    """
    # reload(sys)
    # sys.setdefaultencoding('utf-8')
    # manager = GameManager.get_by_request(request)
    # btn_lst = manager.check_admin_permission()

    server_list, platform_list = daily_log._get_server_list(None,None)
    server_list.remove(server_list[0])

    if request.method == 'POST':
        user_uid = request.POST.get("user_uid")
        user_name = request.POST.get("user_name")

        user_openid = request.POST.get("user_openid")
        server_id = int(request.POST.get("server_id"))
        type_hidden = 'visible'
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        # state_list = game_define.USER_STATE_NAME_DICT
        # print state_list

        if cmem_url:
            try:
                source = {}
                if len(user_uid):
                    source = memcache.get_cmem_val(cmem_url, model_define.ZONE_MODEL.format(user_id=user_uid))
                    print source
                elif len(user_name):
                    name = hashlib.md5(user_name.encode('utf-8')).hexdigest().upper()
                    key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                    user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    source = memcache.get_cmem_val(cmem_url,model_define.ZONE_MODEL.format(user_id=user_uid))
                    print source
                elif len(user_openid):
                    result = memcache.get_cmem_val(cmem_url,model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.ZONE_MODEL.format(user_id=result['uid']))
                    print source

                if source:
                    row_dict = collections.OrderedDict()
                    # row_dict = {1001:{'id':222}}
                    for _key,_value in source['zones_dict'].items():
                        print _key , _value
                        # if _value['normal_rank'] == 0:
                        #     _value['normal_rank'] = "娃娃完美金冠通关"      或者可以换成  u'娃娃完美金冠通关’
                        # elif _value['normal_rank'] == -1:
                        #     _value['normal_rank'] = "娃儿"                      同上
                        # elif _value['normal_rank'] == None:
                        #     _value['normal_rank'] = "瓜娃子你不是金冠啊"               同上
                                         #两种方法转换成汉字输出   字典或者if判断    都是以normal为例
                        row_dict[_key] ={'name':game_config.get_zones_config(_key)['name'],
                                         'normal_pass_reward':REWARD_NAME.get(_value['normal_pass_reward']),
                                         'normal_gold_crown_reward':REWARD_NAME.get(_value['normal_gold_crown_reward']),
                                         'hard_pass_reward':REWARD_NAME.get(_value['hard_pass_reward']),
                                         'hard_gold_crown_reward':REWARD_NAME.get(_value['hard_gold_crown_reward']),
                                         # 'normal_rank':STAGE_PASS_NAME.get(_value['normal_rank'],u'已通关'),
                                         # 'hero_rank':STAGE_PASS_NAME.get(_value['hero_rank'],u'已通关'),
                                         'normal_rank':STAGE_PASS_NAME.get(_value['normal_rank'],u'已通关'),
                                         'hero_rank':STAGE_PASS_NAME.get(_value['hero_rank'],u'已通关'),
                                         }

                return render_to_response(zone_info_edit, locals(), RequestContext(request))

            except UnboundLocalError:
                type_hidden = 'hidden'
                return render_to_response(zone_info_edit, locals(), RequestContext(request))
            except TypeError:
                type_hidden = 'hidden'
                return render_to_response(zone_info_edit, locals(), RequestContext(request))

    else:
        row_list = []
        type_hidden = 'hidden'
        row_dict = {}
        # print locals()
        return render_to_response(zone_info_edit, locals(), RequestContext(request))

# @require_permission
# def set_zone_info_edit(request, zone_info_edit):
#     '''
#     返回修改后的数据
#     '''
#     server_list, platform_list = daily_log._get_server_list(None, None)
#
#     if request.method == 'POST':
#         state = int(request.POST.get('state'))
#         uid = request.POST.get('uid')
#         server_id = int(request.POST.get('server_id'))
#         cmem_url = server_define.CMEM_MAP[int(server_id)]
#         url = 'data_edit/zone_info_edit/'
#         if cmem_url:
#             source = memcache.get_cmem_val(cmem_url, model_define.ZONE_MODEL.format(user_id=uid))
#             source['state'] = state
#             a = memcache.put_cmem_val(cmem_url, model_define.ZONE_MODEL.format(user_id=uid), source)
#         type_hidden = 'hidden'
#         return render_to_response(zone_info_edit, locals(), RequestContext(request))
#     else:
#         row_list = []
#         return render_to_response(zone_info_edit, locals(), RequestContext(request))




# def set_zone_memcache(request, template):
#     '''
#     返回修改后的数据
#     '''
#     manager = GameManager.get_by_request(request)
#     server_list, platform_list = daily_log._get_server_list(None, None)
#
#     if request.method == 'POST':
#         state = int(request.POST.get('state'))
#         user_uid = request.POST.get('user_uid')
#         server_id = int(request.POST.get('server_id'))
#         cmem_url = server_define.CMEM_MAP[int(server_id)]
#         if cmem_url:
#             source = memcache.get_cmem_val(cmem_url, model_define.ZONE_MODEL.format(user_id=user_uid))
#             source['state'] = state
#             # a = memcache.put_cmem_val(cmem_url, model_define.ZONE_MODEL.format(user_id=user_uid), source)
#         type_hidden = 'hidden'
#         row_lst =(user_uid,server_id)
#         return render_to_response("data_edit/zone_info_edit.html", {'account':manager.account,'row_lst': row_lst, 'user_uid':user_uid,'server_list': server_list,'server_id': server_id }, RequestContext(request))
#     else:
#         row_lst = []
#         return render_to_response("data_edit/zone_info_edit.html", {'account':manager.account,'row_lst': row_lst, 'server_list': server_list}, RequestContext(request))
#
                #
                # state_list = game_define.USER_STATE_NAME_DICT
                # if cmem_url:
                #     try:
                #         if len(user_uid):
                #             zone_model = memcache.get_cmem_val(cmem_url, model_define.ZONE_MODEL.format(user_id=user_uid))
                #             print zone_model
                #             for k, v in zone_model.items():
                #                 print("----------------")
                #                 print k
                #                 print v,type(v)
                #                 print("111111111111111111")
                #                 if type(v) == dict:
                #                     for _v in v:
                #                         print _v, type(_v)
                #                         print("====================================================")
                #             for i in zone_model['zone']:
                #                 print("----------------")
                #                 print i
                #             one_zone = zone_model['zone'][0]
                #             for key, val in one_zone.items():
                #                 print key, val, type(val)
                #                 if type(val) == list:
                #                     for _val in val:
                #                         print _val, type(_val)
                #     except:
                #         print "ffffdfdsf"
                #


















