# -*- coding:utf-8 -*-

from django.template import RequestContext
from apps.game_manager.views.log import daily_log
from django.shortcuts import render_to_response
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define,game_define
from apps.common.decorators.decorators import require_permission
from apps.game_manager.mysql.server_list import get_server_list_dat
from apps.config.game_config import get_all_daily_task_config,get_item_config_with_id_name
import pickle
import hashlib


# 获取玩家每日任务信息
@require_permission
def get_daily_task_info(request):
    head_lst = [
        {'width': 50, 'name': u'任务名称'},
        {'width': 50, 'name': u'任务开放等级'},
        {'width': 50, 'name': u'任务可领取最小等级'},
        {'width': 50, 'name': u'任务可领取最大等级'},
        {'width': 50, 'name': u'任务最多可完成次数'},
        {'width': 50, 'name': u'任务可获得的积分'},
        {'width': 50, 'name': u'任务可以获得的奖励'},
        {'width': 50, 'name': u'玩家完成次数'},
        {'width': 50, 'name': u'获得奖励时间'},
        {'width': 50, 'name': u'是否获得奖励'},
        ]

    head_lst1= [
        {'width': 50, 'name': u'礼包名称'},
        {'width': 50, 'name': u'获得奖励'},
        {'width': 50, 'name': u'所需任务积分'},
        ]
    server_list_dat = get_server_list_dat()
    if request.method == 'POST':
        user_id = request.POST.get('user_uid')
        user_name = request.POST.get('user_name').encode('utf-8')
        user_account = request.POST.get('user_account')
        try:
            user_openid = str(request.POST.get('user_openid'))
        except UnicodeEncodeError :
            user_openid = ''

        server_id = int(request.POST.get('server_id'))
        type_hidden = 'visible'
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        state_list = game_define.USER_STATE_NAME_DICT
        row_lst=[]
        row_lst1=[]
        print user_id
        source=None
        # f=open('/opt/CGameLogserver/apps/game_manager/views/data_edit/USER_DETAIL')
        # d=pickle.load(f)
        # for i in d:
        #     user_id=str(i)
        if cmem_url:
            if  len(user_id) <> 0:
                source = memcache.get_cmem_val(cmem_url, model_define.DAILY_TASK_MODEL.format(user_id=user_id))
                #print source,'source'
            elif  len(user_name)<> 0:
                name = hashlib.md5(user_name).hexdigest().upper()
                key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                source = memcache.get_cmem_val(cmem_url,model_define.DAILY_TASK_MODEL.format(user_id=user_uid))
            elif  len(user_openid) <> 0:
                try:
                    result = memcache.get_cmem_val(cmem_url,model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.DAILY_TASK_MODEL.format(user_id=result['uid']))
                except:
                    pass
            if source<> None:
                for task in source['tasks']:
                    # if task in source['single_daily_task_has_reward_lst']:
                    print task, source['tasks'][task]
                    print  _get_level(task)[0],_get_level(task)[1],_get_level(task)[2],_get_level(task)[3],_get_level(task)[4],
                    row_lst.append([daily_task_name[task],
                                    _get_level(task)[0],_get_level(task)[1],_get_level(task)[2],_get_level(task)[3],_get_level(task)[4],
                                    _get_reward(task),source['tasks'][task]['num'],
                                    str(source['reward_date']),_get_wancheng(task,source['tasks']),
                                    ])
                for i in source['score_has_reward_lst']:
                    row_lst1.append([score_reward[i]['name'],score_reward[i]['reward'],score_reward[i]['score']])
        return render_to_response("data_edit/daily_task_info.html",
                                  {'row_lst': row_lst,'user_id':user_id,'user_openid':user_openid,'user_name':user_name,
                                   'head_lst': head_lst, 'server_list': server_list_dat,'cur_server_id':server_id,
                                   'head_lst1':head_lst1,'row_lst1':row_lst1
                                   }, RequestContext(request))
    else:
        row_lst = []
        row_lst1=[]
        return render_to_response("data_edit/daily_task_info.html",
                                  {'row_lst': row_lst,'head_lst1':head_lst1,'row_lst1':row_lst1,
                                   'head_lst': head_lst, 'server_list': server_list_dat}, RequestContext(request))

def _get_wancheng(task,reward_lst):
    if task in reward_lst:
        return '是'
    else:
        return '否'



def _get_reward(task):
    item_name_dict,laji=get_item_config_with_id_name()
    daily_task_dict=get_all_daily_task_config()
    # print item_name_dict
    if daily_task_dict[str(task)]['gold']<>0:
        return '金币：%s个' % daily_task_dict[str(task)]['gold']
    elif daily_task_dict[str(task)]['item']<>0:
        task_dict=daily_task_dict[str(task)]
        print item_name_dict[task_dict['item']]
        return '装备：%s' % ((item_name_dict[task_dict['item']]).encode('utf-8'))
    elif daily_task_dict[str(task)]['stone']<>0:
        return '钻石：%s个' % daily_task_dict[str(task)]['stone']


def _get_level(task):
    item_name_dict,laji=get_item_config_with_id_name()
    daily_task_dict=get_all_daily_task_config()
    return daily_task_dict[str(task)]['openLevel'],daily_task_dict[str(task)]['minLevel'],daily_task_dict[str(task)]['maxLevel'],daily_task_dict[str(task)]['num'],daily_task_dict[str(task)]['score']

daily_task_name={
    1:	'1	挑战竞技场',
    2:	'2	购买体力',
    3:	'3	购买金币',
    4:	'4	钻石/免费抽奖',
    5:	'5	宠物升星',
    6:	'6	宠物洗练',
    7:	'7	宠物技能强化',
    8:	'8	装备强化',
    9:	'9	猜拳',
    10:	'10	钓鱼',
    11:	'11	普通副本胜利',
    12:	'12	问答',
    13:	'13	按摩',
    14:	'14	进补',
    15:	'15	宠物使用营养液升级升级',
    16:	'16	宠物使用太阳石进化',
    17:	'17	英雄副本胜利/扫荡',
    18:	'18	抓宠副本胜利',
    19:	'19	经验/金币副本胜利',
    20:	'20	世界BOSS战斗',
    21:	'21	道馆挑战',
    22:	'22	夺宝',
}

score_reward={
    1:{'name':'积分礼包1','reward':'金币x10000，钻石x20','score':20},
    2:{'name':'积分礼包2','reward':'小营养液x2，金币x20000，钻石x20','score':60},
    3:{'name':'积分礼包3','reward':'装备精华x10，金币x50000，钻石x20','score':100},
    4:{'name':'积分礼包4','reward':'金色精华x30，金币x100000，钻石x20','score':130},
}