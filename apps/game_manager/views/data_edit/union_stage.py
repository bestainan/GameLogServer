# -*- coding:utf-8 -*-

import collections
import hashlib
import time
from django.template import RequestContext
from apps.game_manager.views.log import daily_log
from django.shortcuts import render_to_response
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define
from apps.config import game_config

NORMAL_DICT = {
        'union_top_pass_stage_level_time':'联盟最高关卡完成时间: ',
        'union_max_user_num': '联盟最高人数：',
        'uid': '联盟UID：',
        'union_next_target_stage_level': '盟主设定的目标关卡: ',
        'stage_cur_hp': '当前生命值(几个关卡的当前HP总和)：',
        'stage_total_hp': '总体生命值(几个关卡的HP总和)：',
        'union_target_stage_level': '联盟目标关卡：',
        'union_open_stage_level': '公会开启关卡：',
        'union_top_pass_stage_level': '联盟通关的最高级关卡：',
        'last_union_stage_refresh_datetime': '联盟关卡刷新时间: ',
        'union_user_num': '联盟人数: ',
        }

def get_union_stage_function(request, templates):
    """
        联盟关卡：
        source {
        'union_stage_chest':  #通关宝箱个数=当前人数+10 [{'id': 9, 'name': '', 'uid': 0}, {'id': 14, 'name': '', 'uid': 0},
                                                      {'id': 14, 'name': '', 'uid': 0}, {'id': 16, 'name': '', 'uid': 0}, {'id': 1, 'name': '', 'uid': 0},
                                                      {'id': 14, 'name': '', 'uid': 0}, {'id': 7, 'name': '', 'uid': 0}, {'id': 19, 'name': '', 'uid': 0},
                                                      {'id': 3, 'name': '', 'uid': 0}, {'id': 25, 'name': '', 'uid': 0}, {'id': 19, 'name': '', 'uid': 0}
                                                    ],
          'stage_dat': {70001: [50000, 50000, 50000, 50000, 100000], 70002: [50000, 50000, 50000, 50000, 100000], 70003: [50000, 50000, 50000, 50000, 100000], 70004: [50000, 50000, 50000, 50000, 100000], 70005: [50000, 50000, 50000, 50000, 100000], 70006: [0, 150000, 0, 0, 0]},
          'union_stage_damage': {'1000110497': {'uid': '1000110497', 'dmg': 450000}},
          'damage_rank': [{'uid': '1000099479', 'dmg': 0}],
          'union_stage_killer': {70002: '1000110497', 70006: '1000110497'},
          'union_stage_reward_config_lst': None,

          'union_top_pass_stage_level_time': 0,
          'union_max_user_num': 30,
          'uid': '3016',
          'union_next_target_stage_level': 1,
          'stage_cur_hp': 1650000,
          'stage_total_hp': 1650000,
          'union_target_stage_level': 1,
          'union_open_stage_level': 1,
          'union_top_pass_stage_level': 0,
          'last_union_stage_refresh_datetime': datetime.datetime(2015, 8, 3, 18, 0),
          'union_user_num': 6
          }

    def_attrs = dict(
            uid=None,
            union_user_num=1,   # 联盟人数
            union_max_user_num=1,   # 联盟最高人数
            # 关卡部分
            last_union_stage_refresh_datetime=None,   # 联盟关卡刷新时间
            union_target_stage_level=1,        # 联盟目标关卡
            union_next_target_stage_level=1,   # 盟主设定的目标关卡
            union_top_pass_stage_level=0,      # 联盟通关的最高级关卡
            union_top_pass_stage_level_time=0,  # 联盟最高关卡完成时间
            stage_dat=dict(),  # 关卡数据
            stage_total_hp=0,  # 总体生命值(几个关卡的HP总和)
            stage_cur_hp=0,  # 当前生命值(几个关卡的当前HP总和)
            union_open_stage_level=1,   # 公会开启关卡

            union_stage_chest=[],   # 关卡宝箱
            union_stage_reward_config_lst=None,    # 宝箱部分配置表

            union_stage_damage=dict(),      # 联盟关卡伤害数据
            damage_rank=[],      # 伤害排行

            # 击杀显示
            union_stage_killer=dict(),      # 联盟关卡击杀
    )

    """
    # 以函数的指针方式传递函数并调用
    function_name = 'data_edit.union_stage.{function}'.format(function=set_union_stage_function.__name__)
    server_list, platform_list = daily_log._get_server_list(None, None)
    try:
        server_list.remove(server_list[0])
    except:
        pass

    return_uid = '请输入uid'
    return_openid = "请输入openid"
    return_name = "请输入玩家昵称"
    if request.method == 'POST':
        union_uid = request.POST.get('union_uid')
        union_name = request.POST.get('union_name').encode('utf-8')
        print union_name
        server_id = int(request.POST.get('server_id'))
        type_hidden = 'visible'
        cmem_url = server_define.CMEM_MAP[int(server_id)]

        head_lst = [
            {'name': u'条目'},
            {'name': u'内容'},
        ]
        if cmem_url:
            try:
                source = dict()
                if len(union_uid):
                    source = memcache.get_cmem_val(cmem_url, model_define.UNION_STAGE_CAS_MODEL.format(union_id=union_uid))
                    return_uid = union_uid
                elif len(union_name):
                    name = hashlib.md5(union_name).hexdigest().upper()
                    key = model_define.UNION_NAME_MODEL.format(union_name_md5=name)
                    union_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    return_uid = union_uid
                    return_name = union_name
                    source = memcache.get_cmem_val(cmem_url, model_define.UNION_STAGE_CAS_MODEL.format(union_id=union_uid))
                if source:
                    print 'source', source

                    row_dict = collections.OrderedDict()  # 有序字典
                    # --------------------------------------显示部分------------------------------------------------
                    # 17条
                    # 普通选项（key:单值） 11条 其中2条需要取公会名字 2条需要转换时间
                    nor_lst = []
                    for _each_nor_key, _each_name in NORMAL_DICT.items():
                        # 1.处理日期
                        _value = source[_each_nor_key]
                        if 'union_top_pass_stage_level_time' == _each_nor_key:
                            if _value:
                                _value = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(_value))
                        if 'last_union_stage_refresh_datetime' == _each_nor_key:
                            if _value:
                                _value = _value.strftime('%Y-%m-%d %H:%M:%S')
                        # 2.处理关卡id


                        nor_lst.extend([[_each_name, _value]])

                    all_immutable_lst = []
                    if nor_lst:
                        all_immutable_lst.append(nor_lst)
                    # --------------------------------------可修改部分----------------------------------------------

                return render_to_response(templates, locals(), RequestContext(request))

            except UnboundLocalError:
                type_hidden = 'hidden'
                return render_to_response(templates, locals(), RequestContext(request))

            except TypeError:
                type_hidden = 'hidden'
                return render_to_response(templates, locals(), RequestContext(request))

    else:
        row_list = []
        type_hidden = 'hidden'
        return render_to_response(templates, locals(), RequestContext(request))


# @require_permission
def set_union_stage_function(value_dict):
    """
    修改memcache数据

    tem_id 30057$$num
    """
    cmem_url = server_define.CMEM_MAP[int(value_dict['server_id'])]
    if cmem_url:
        if len(value_dict['user_id']):# 注 此处user_id 是union_id
            source = memcache.get_cmem_val(cmem_url, model_define.UNION_STAGE_CAS_MODEL.format(union_id=value_dict['union_id']))
            # try:
            #     (first_key, second_key) = value_dict['item_id'].split('$$')
            #     first_key = int(first_key)
            #     input_value = int(value_dict['input_value'])
            #     second_key = str(second_key)
            #     # print first_key, second_key, input_value
            #
            #     if 'num' == second_key and 0 <= input_value:
            #         source['stages'][first_key][second_key] = input_value
            #     elif 'rank' == second_key and (0 == input_value or -1 == input_value):
            #         source['stages'][first_key][second_key] = input_value
            #     elif 'buy_count' == second_key and 0 <= input_value:
            #         source['stages'][first_key][second_key] = input_value
            #     else:
            #         return False
            # except:
            #     return False
            # 传回 url  uid  以及数据 做外层检测
            result = memcache.put_cmem_val(cmem_url, model_define.UNION_STAGE_CAS_MODEL.format(union_id=value_dict['union_id']), source)
            return result