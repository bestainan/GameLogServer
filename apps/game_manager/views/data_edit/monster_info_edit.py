# -*- coding:utf-8 -*-

import math
import random
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
from apps.game_manager.models.game_manager import GameManager
from apps.logs.output_action_gm import *


@require_permission
def get_monster_lst(request):
    """
    数据后台 --- 宠物信息

    seq_id  <type 'int'>
    uid  <type 'str'>
    monster_high_star_level  <type 'int'>
    monster_kind <type 'list'>
    data_version  <type 'str'>
    monster_high_level  <type 'int'>
    monster_high_quality  <type 'int'>
    monsters <type 'str'>
    [
        evo_level 4 <type 'int'>
        star_level_exp 16 <type 'int'>
        skillsExp [0, 0] <type 'list'>
        level 54 <type 'int'>
        playerID 1000095298 <type 'str'>
        effort 2 <type 'int'>
        starLevel 3 <type 'int'>
        sex 0 <type 'int'>
        generation 1 <type 'int'>
        individual [1, 0, 1, 0, 0, 0] <type 'list'>
        evo_sun_stone 96 <type 'int'>
        skillsLevel [6, 10] <type 'list'>
        exp 11739 <type 'int'>
        personality 11 <type 'int'>
        tid 25 <type 'int'>
        uid 1 <type 'int'>
        star_level_rate 0.02083 <type 'float'>
        maxLevel 60 <type 'int'>
        createTime 2015-05-31 09:12:51.761554 <type 'datetime.datetime'>
        evo_fail_count 0 <type 'int'>
    ]
    list中都是int
    HpIndividual = 0
    AttackIndividual = 1
    DefenceIndividual = 2
    SpcAttackIndividual = 3
    SpcDefenceIndividual = 4
    SpeedIndividual = 5
    """
    # 获取当前管理员
    manager = GameManager.get_by_request(request)

    function_name = 'data_edit.monster_info_edit.{function}'.format(function=set_memcache.__name__)
    server_list, platform_list = daily_log._get_server_list(None, None)
    server_list.remove(server_list[0])
    if request.method == 'POST':
        user_uid = request.POST.get('user_uid')
        user_name = request.POST.get('user_name').encode('utf-8')
        user_openid = request.POST.get('user_openid')
        server_id = request.POST.get('server_id')
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        table_lst = []

        if len(user_uid):
            monster_model = memcache.get_cmem_val(cmem_url, model_define.MONSTER_MODEL.format(user_id=int(user_uid)))
        elif len(user_name):
            name = hashlib.md5(user_name).hexdigest().upper()
            key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
            user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
            monster_model = memcache.get_cmem_val(cmem_url, model_define.MONSTER_MODEL.format(user_id=user_uid))
        elif len(user_openid):
            result = memcache.get_cmem_val(cmem_url, model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
            monster_model = memcache.get_cmem_val(cmem_url, model_define.MONSTER_MODEL.format(user_id=result['uid']))
        # 宠物相关最高值
        uid = monster_model['uid']
        monster_high_star_level = monster_model['monster_high_star_level']
        monster_kind = monster_model['monster_kind']
        monster_high_level = monster_model['monster_high_level']
        monster_high_quality = monster_model['monster_high_quality']
        all_monsters = monster_model['monsters']
        head_lst = [
            {'width': 50, 'name': u'玩家ID'},
            {'width': 50, 'name': u'宠物最高星级'},
            {'width': 50, 'name': u'宠物最高等级'},
            {'width': 50, 'name': u'宠物最高品质'},
            {'width': 50, 'name': u'宠物种类个数'},
        ]
        row_lst = [uid, monster_high_star_level, monster_high_level, monster_high_quality, len(monster_kind)]
        table_lst.append(row_lst)

        for _monster in all_monsters:
            _monster_config = game_config.get_monster_config(_monster['tid'])
            _monster['name'] = _monster_config['name']

        type_hidden = 'visible'
        return render_to_response("data_edit/monster_info_edit.html",
                                  {"server_list": server_list, "user_uid": user_uid, 'server_id': int(server_id),
                                   'row_lst': table_lst, 'head_lst': head_lst, 'monster_lst': all_monsters,
                                   'function_name': function_name, 'type_hidden': type_hidden},
                                  RequestContext(request))

    else:
        # row_list = []
        type_hidden = 'hidden'
        return render_to_response("data_edit/monster_info_edit.html", locals(), RequestContext(request))


def set_memcache(value_dict):
    """
        修改memcache数据
    """
    server_id = int(value_dict['server_id'])
    user_id = value_dict['user_id']
    item_id = value_dict['item_id']
    old_value = int(value_dict['value'])
    new_value = int(value_dict['input_value'])
    manager = value_dict['manager']

    data = item_id.split("&&")
    monster_uid = int(data[0])
    change_key = str(data[1])
    cmem_url = server_define.CMEM_MAP[int(server_id)]
    monster_tid = 0

    if cmem_url:
        if len(user_id):
            if int(new_value) < 0:
                return False
            monster_model = memcache.get_cmem_val(cmem_url, model_define.MONSTER_MODEL.format(user_id=int(user_id)))
            for _monster in monster_model['monsters']:
                if monster_uid == _monster['uid']:
                    monster_tid = _monster['tid']
                    if change_key in ['individual', 'skillsLevel', 'skillsExp']:
                        change_index = int(data[2])
                        _monster[change_key][change_index] = int(new_value)
                    else:
                        _monster[change_key] = int(new_value)
                    break
            memcache.put_cmem_val(cmem_url, model_define.MONSTER_MODEL.format(user_id=user_id), monster_model)
            # 操作日志记录
            insert_action_change_monster(manager, server_id, user_id, monster_uid, monster_tid, change_key, old_value, new_value)

            return True
    return False


def add_monster(request):
    """
        增加宠物数据
        {'generation': 1,  'star_level_rate': 0.02083, 'createTime': datetime.datetime(2015, 5, 31, 9, 12, 51, 761554)}

        evo_level 4 <type 'int'>
        star_level_exp 16 <type 'int'>
        skillsExp [0, 0] <type 'list'>
        level 54 <type 'int'>
        playerID 1000095298 <type 'str'>
        effort 2 <type 'int'>
        starLevel 3 <type 'int'> "4"
        sex 0 <type 'int'>
        generation 1 <type 'int'>
        individual [1, 0, 1, 0, 0, 0] <type 'list'>
        evo_sun_stone 96 <type 'int'>
        skillsLevel [6, 10] <type 'list'>
        exp 11739 <type 'int'>
        personality 11 <type 'int'>
        tid 25 <type 'int'>
        uid 1 <type 'int'>
        star_level_rate 0.02083 <type 'float'>
        maxLevel 60 <type 'int'>
        createTime 2015-05-31 09:12:51.761554 <type 'datetime.datetime'>
        evo_fail_count 0 <type 'int'>
    """
    manager = GameManager.get_by_request(request)
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        server_id = request.GET.get('server_id')
        cmem_url = server_define.CMEM_MAP[int(server_id)]

        # 获取宠物tid和名字对应列表
        monster_id_name = game_config.get_monster_config_with_id_name()
        monster_id_name_lst = []
        for (tid, name) in monster_id_name.items():
            content = dict()
            content['tid'] = tid
            content['name'] = name + "_" + str(tid)
            monster_id_name_lst.append(content)
        monster_id_name_lst = sorted(monster_id_name_lst, cmp=lambda x, y: cmp(x['tid'], y['tid']))

        monster_model = memcache.get_cmem_val(cmem_url, model_define.MONSTER_MODEL.format(user_id=str(user_id)))
        monster_uid = monster_model['seq_id']

        return render_to_response("data_edit/add_monster.html",
                                  {'user_id': user_id, 'server_id': server_id, 'monster_uid': monster_uid,
                                   'monster_id_name_lst': monster_id_name_lst},
                                  RequestContext(request))
    elif request.method == 'POST':
        # 获取对应值
        user_id = str(request.POST.get('user_id'))
        monster_uid = int(request.POST.get('monster_uid'))
        server_id = int(request.POST.get('server_id'))
        monster_tid = int(request.POST.get("tid"))
        star_level = int(request.POST.get("star_level"))
        level = int(request.POST.get("level"))

        # 创建一个新宠物
        result = create_monster(user_id, monster_uid, server_id, monster_tid, star_level, level)
        # 操作日志记录
        insert_action_create_monster(manager, server_id, user_id, monster_uid, monster_tid, star_level, level)

        # 创建完成返回宠物查询页面
        function_name = 'data_edit.monster_info_edit.{function}'.format(function=set_memcache.__name__)
        server_list, platform_list = daily_log._get_server_list(None, None)
        server_list.remove(server_list[0])

        cmem_url = server_define.CMEM_MAP[int(server_id)]
        monster_model = memcache.get_cmem_val(cmem_url, model_define.MONSTER_MODEL.format(user_id=str(user_id)))

        # 获取宠物相关最高值
        uid = monster_model['uid']
        monster_high_star_level = monster_model['monster_high_star_level']
        monster_kind = monster_model['monster_kind']
        monster_high_level = monster_model['monster_high_level']
        monster_high_quality = monster_model['monster_high_quality']

        all_monsters = monster_model['monsters']
        table_lst = []
        head_lst = [
            {'width': 50, 'name': u'玩家ID'},
            {'width': 50, 'name': u'宠物最高星级'},
            {'width': 50, 'name': u'宠物最高等级'},
            {'width': 50, 'name': u'宠物最高品质'},
            {'width': 50, 'name': u'宠物种类个数'},
        ]
        row_lst = [uid, monster_high_star_level, monster_high_level, monster_high_quality, len(monster_kind)]
        table_lst.append(row_lst)

        for _monster in all_monsters:
            _monster_config = game_config.get_monster_config(_monster['tid'])
            _monster['name'] = _monster_config['name']

        type_hidden = 'visible'
        # return HttpResponseRedirect("data_edit/monster_info_edit.html")
        return render_to_response("data_edit/monster_info_edit.html",
                                  {"server_list": server_list, "user_id": user_id, 'server_id': int(server_id),
                                   'row_lst': table_lst, 'head_lst': head_lst, 'monster_lst': all_monsters,
                                   'function_name': function_name, 'type_hidden': type_hidden},
                                  RequestContext(request))


def delete_monster_confirm(request):
    """
        删除宠物确认
    """
    if request.method == 'GET':
        user_id = str(request.GET.get('user_id'))
        server_id = int(request.GET.get('server_id'))
        monster = dict()
        monster['uid'] = request.GET.get('monster_uid')
        monster['name'] = request.GET.get('name')
        monster['starLevel'] = request.GET.get('starLevel')
        monster['level'] = request.GET.get('level')
        head_lst = [
            {'width': 50, 'name': u'UID'},
            {'width': 50, 'name': u'名字'},
            {'width': 50, 'name': u'星级'},
            {'width': 50, 'name': u'等级'},
            {'width': 50, 'name': u'操作'},
        ]
        # server_notice_dat = server_notice.get_version_notice(version)
        # _server_notice_dict = dict()
        # _server_notice_dict['version'] = version
        # _server_notice_dict['notice'] = server_notice_dat['notice']
        return render_to_response("data_edit/delete_monster_confirm.html", {'user_id': user_id, 'server_id': server_id, 'monster': monster, 'head_lst': head_lst}, RequestContext(request))
    else:
        return HttpResponseRedirect('/Tyranitar6/data_edit/monster_info_edit/')


def delete_monster(request):
    """
        删除宠物
    """
    manager = GameManager.get_by_request(request)
    if request.method == 'POST':
        user_id = str(request.POST.get('user_id'))
        server_id = str(request.POST.get('server_id'))
        monster_uid = str(request.POST.get('monster_uid'))
        starLevel = str(request.POST.get('starLevel'))
        level = str(request.POST.get('level'))
        remove_monster(manager, user_id, server_id, monster_uid, starLevel, level)
        return HttpResponseRedirect('/Tyranitar6/data_edit/monster_info_edit/')
    else:
        return render_to_response("data_edit/add_monster.html", RequestContext(request))


def remove_monster(manager, user_id, server_id, uid, star_level, level):
    """
        移除一个怪
    """
    cmem_url = server_define.CMEM_MAP[int(server_id)]
    monster_model = memcache.get_cmem_val(cmem_url, model_define.MONSTER_MODEL.format(user_id=str(user_id)))
    for mon in monster_model['monsters']:
        if mon["uid"] == int(uid):
            monster_tid = mon['tid']
            monster_model['monsters'].remove(mon)
            memcache.put_cmem_val(cmem_url, model_define.MONSTER_MODEL.format(user_id=str(user_id)), monster_model)
            # 操作日志记录
            insert_action_delete_monster(manager, server_id, user_id, uid, monster_tid, star_level, level)
            break


def create_monster(user_id, monster_uid, server_id, monster_tid, star_level, level):
    """
        创建一个宠物
    """
    try:
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        monster_model = memcache.get_cmem_val(cmem_url, model_define.MONSTER_MODEL.format(user_id=str(user_id)))

        mon_config = game_config.get_monster_config(monster_tid)

        mon = dict()
        mon["uid"] = int(monster_uid)  # 序号
        mon["playerID"] = str(user_id)  # 所属玩家ID
        mon["tid"] = int(monster_tid)  # 数据表ID

        rand_sex = _random_sex(monster_tid)
        mon["sex"] = rand_sex  # 性别（0-1）

        mon["individual"] = [0] * 6  # 个体值
        mon["effort"] = 0  # 努力值    (变化: 突破)
        mon["personality"] = random.randint(1, 25)  # 性格 （1-25）
        mon["generation"] = 1  # 世代值 （1-6）
        mon["createTime"] = datetime.datetime.now()
        mon["exp"] = 0  # 经验
        mon["level"] = int(level)  # 等级
        mon["maxLevel"] = 30  # 等级上限

        # 技能等级
        skills_level = []
        # 技能经验
        skills_exp = []
        for index in range(1, 3):
            skills_level.append(1)
            skills_exp.append(0)
        mon["skillsLevel"] = skills_level  # 技能等级
        mon["skillsExp"] = skills_exp    # 技能经验

        # 星级部分
        mon["starLevel"] = int(star_level)  # 星级
        mon['star_level_exp'] = get_monster_star_num(mon['starLevel'])  # 星级对应的吃卡
        mon['star_level_rate'] = 0        # 升星比率

        # 进化部分
        mon['evo_sun_stone'] = 0   # 进化太阳石
        mon['evo_level'] = mon_config['defeatEvoClass']     # 进化等级
        mon['evo_fail_count'] = 0     # 进化失败次数

        monster_model['seq_id'] += 1
        monster_model['monsters'].append(mon)

        # 检测最高数值
        if monster_model['monster_high_level'] < mon['level']:
            monster_model['monster_high_level'] = mon['level']
        if monster_model['monster_high_star_level'] < mon['starLevel']:
            monster_model['monster_high_star_level'] = mon['starLevel']
        if monster_model['monster_high_quality'] < mon_config['color']:
            monster_model['monster_high_quality'] = mon_config['color']
        if monster_tid not in monster_model['monster_kind']:
            monster_model['monster_kind'].append(monster_tid)

        memcache.put_cmem_val(cmem_url, model_define.MONSTER_MODEL.format(user_id=str(user_id)), monster_model)
        return True
    except:
        return False


def _random_sex(tid):
    """
    随机性别
    """
    mon_config = game_config.get_monster_config(tid)
    if mon_config:
        ran_sex = float(random.randint(0, 1000)) / 10
        sex = 0
        if ran_sex > float(mon_config['sexRate']):
            sex = 1
    else:
        return 'error'
    return sex


def get_monster_star_num(monster_star_level):
    """
        获取生星级需要1星卡牌数量
    """
    if monster_star_level > 5:
        monster_star_level = 5
    return int(math.pow(4, monster_star_level - 1) - 1)


# @require_permission
# def change_monster(request):
#     """
#         修改宠物数据
#         {'generation': 1,  'star_level_rate': 0.02083, 'createTime': datetime.datetime(2015, 5, 31, 9, 12, 51, 761554)}
#
#         evo_level 4 <type 'int'>
#         star_level_exp 16 <type 'int'>
#         skillsExp [0, 0] <type 'list'>
#         level 54 <type 'int'>
#         playerID 1000095298 <type 'str'>
#         effort 2 <type 'int'>
#         starLevel 3 <type 'int'> "4"
#         sex 0 <type 'int'>
#         generation 1 <type 'int'>
#         individual [1, 0, 1, 0, 0, 0] <type 'list'>
#         evo_sun_stone 96 <type 'int'>
#         skillsLevel [6, 10] <type 'list'>
#         exp 11739 <type 'int'>
#         personality 11 <type 'int'>
#         tid 25 <type 'int'>
#         uid 1 <type 'int'>
#         star_level_rate 0.02083 <type 'float'>
#         maxLevel 60 <type 'int'>
#         createTime 2015-05-31 09:12:51.761554 <type 'datetime.datetime'>
#         evo_fail_count 0 <type 'int'>
#     """
#     if request.method == 'GET':
#         user_id = request.GET.get('user_id')
#         monster_uid = request.GET.get('monster_uid')
#         server_id = request.GET.get('server_id')
#         cmem_url = server_define.CMEM_MAP[int(server_id)]
#         if cmem_url:
#             monster_model = memcache.get_cmem_val(cmem_url, model_define.MONSTER_MODEL.format(user_id=int(user_id)))
#             all_monsters = monster_model['monsters']
#             for _monster in all_monsters:
#                 if _monster['uid'] == int(monster_uid):
#                     monster = _monster
#                     print("-------------")
#                     print monster
#                     _monster_config = game_config.get_monster_config(_monster['tid'])
#                     monster['name'] = _monster_config['name']
#                     break
#
#         return render_to_response("data_edit/change_monster.html",
#                                   {'user_id': user_id, 'server_id': server_id},
#                                   RequestContext(request))
#     elif request.method == 'POST':
#         user_id = request.POST.get('user_id')
#         monster_uid = request.POST.get('monster_uid')
#         server_id = request.POST.get('server_id')
#         tid = request.POST.get("tid")
#         sex = request.POST.get("sex")
#         star_level = request.POST.get("starLevel")
#         star_level_exp = request.POST.get("star_level_exp")
#         level = request.POST.get("level")
#         max_level = request.POST.get("maxLevel")
#         exp = request.POST.get("exp")
#         effort = request.POST.get("effort")
#         personality = request.POST.get("personality")
#         evo_sun_stone = request.POST.get("evo_sun_stone")
#         evo_level = request.POST.get("evo_level")
#         evo_fail_count = request.POST.get("evo_fail_count")
#         individual_lst = []
#         for i in xrange(6):
#             individual = request.POST.get("individual" + str(i))
#             individual_lst.append(individual)
#         skills_level_lst = []
#         skills_exp_lst = []
#         for i in xrange(2):
#             skill_level = request.POST.get("skill_level" + str(i))
#             skill_exp = request.POST.get("skill_exp" + str(i))
#             skills_level_lst.append(skill_level)
#             skills_exp_lst.append(skill_exp)
#         cmem_url = server_define.CMEM_MAP[int(server_id)]
#         monster_model = memcache.get_cmem_val(cmem_url, model_define.MONSTER_MODEL.format(user_id=int(user_id)))
#         all_monsters = monster_model['monsters']
#         for _monster in all_monsters:
#             if _monster['uid'] == int(monster_uid):
#                 monster = _monster
#                 print("-------------")
#                 print monster
#                 break
#         if tid:
#             monster['tid'] = int(tid)
#             print tid, type(tid)
#         if sex:
#             monster['sex'] = int(sex)
#             print sex, type(sex)
#         if level:
#             monster['level'] = int(level)
#             print level, type(level)
#         if max_level:
#             monster['maxLevel'] = int(max_level)
#             print max_level, type(max_level)
#         if star_level:
#             monster['starLevel'] = int(star_level)
#             print star_level, type(star_level)
#         if star_level_exp:
#             monster['star_level_exp'] = int(star_level_exp)
#             print star_level_exp, type(star_level_exp)
#         if exp:
#             monster['exp'] = int(exp)
#             print exp, type(exp)
#         if effort:
#             monster['effort'] = int(effort)
#             print effort, type(effort)
#         if personality:
#             monster['personality'] = int(personality)
#             print personality, type(personality)
#
#         for index in xrange(len(individual_lst)):
#             individual = request.POST.get("individual" + str(index))
#             if individual:
#                 print monster['individual']
#                 monster['individual'][index] = int(individual)
#                 print monster['individual'][index], type(monster['individual'][index])
#         for index in xrange(len(skills_level_lst)):
#             skill_level = request.POST.get("skill_level" + str(index))
#             if skill_level:
#                 print monster['skillsLevel']
#                 monster['skillsLevel'][index] = int(skill_level)
#                 print monster['skillsLevel'][index], type(monster['skillsLevel'][index])
#         for index in xrange(len(skills_exp_lst)):
#             skill_exp = request.POST.get("skill_exp" + str(index))
#             if skill_exp:
#                 print monster['skillsExp']
#                 monster['skillsExp'][index] = int(skill_exp)
#                 print monster['skillsExp'][index], type(monster['skillsExp'][index])
#         if evo_sun_stone:
#             monster['evo_sun_stone'] = int(evo_sun_stone)
#             print evo_sun_stone, type(evo_sun_stone)
#         if evo_level:
#             monster['evo_level'] = int(evo_level)
#             print evo_level, type(evo_level)
#         if evo_fail_count:
#             monster['evo_fail_count'] = int(evo_fail_count)
#             print evo_fail_count, type(evo_fail_count)
#
#         # a = memcache.put_cmem_val(cmem_url, model_define.USER_MODEL.format(user_id=user_id), source)
#         # return HttpResponseRedirect("data_edit/change_monster.html")
#         return render_to_response("data_edit/monster_info_edit.html", locals(), RequestContext(request))


