#coding:utf-8
import os
import cPickle
from apps.utils import game_define
from apps.game_manager import game_manage_define
from apps.config import game_config
from apps.game_manager.mysql import server_list
from apps.utils import mem_key_name
import datetime

monster_id_name = game_config.get_monster_config_with_id_name()
item_id_name, item_id_type = game_config.get_item_config_with_id_name()
item_id_name[0] = "无"
monster_id_name[0] = "无"
all_server_dict = server_list.get_server_id_name_dict()

SERVER_HIDDEN_NAME_DICT = {
    1: u'隐藏',
    0: u'显示',
}


# ---------------------------管理员部分-------------------------------
def gm_action_super_register(action_dict):
    return "编号"+str(action_dict['uid'])+"账户名"+str(action_dict['account'])+"名字"+action_dict['name'].encode('utf-8')+"描述"+str(action_dict['description'])+"权限"+str(action_dict['permission'])


def gm_action_delete_manager(action_dict):
    return "删除管理员:"+str(action_dict['del_gm'])


def gm_action_manager_register(action_dict):
    return "编号"+str(action_dict['uid'])+"账户名"+str(action_dict['account'])+"名字"+action_dict['name'].encode('utf-8')+"描述"+action_dict['description'].encode('utf-8')+"权限"+str(action_dict['permission'])


def gm_action_manager_login(action_dict):
    return "上次登录时间:"+str(action_dict['last_login_time'])+"\t上次登录IP:"+str(action_dict['last_login_ip'])


def gm_action_update_password(action_dict):
    return "编号"+str(action_dict['uid'])+"账户名"+str(action_dict['account'])+"名字"+action_dict['name'].encode('utf-8')+"描述"+action_dict['description'].encode('utf-8')+"权限"+str(action_dict['permission'])


def gm_action_update_manager_info(action_dict):
    return "编号"+str(action_dict['uid'])+"账户名"+str(action_dict['account'])+"-->"+str(action_dict['new_account'])+"名字"+action_dict['name'].encode('utf-8')+"-->"+action_dict['new_name'].encode('utf-8')+"描述"+str(action_dict['description'])+"-->"+str(action_dict['new_description'])+"权限"+str(action_dict['permission'])+"-->"+str(action_dict['new_permission'])


# ---------------------------玩家数据部分-------------------------------
def gm_action_edit_player(action_dict):
    change_key = mem_key_name.MEM_KEY_NAME[action_dict['key']]
    server = all_server_dict[int(action_dict['server_id'])]
    return "服务器:"+server.encode('utf-8')+"\t用户ID:"+str(action_dict['user_id'])+"\t修改属性 "+change_key.encode('utf-8')+":"+str(action_dict['old'])+"-->"+str(action_dict['new'])


def gm_action_create_monster(action_dict):
    mon_name = monster_id_name[int(action_dict['mon_tid'])]
    print mon_name
    server = all_server_dict[int(action_dict['server_id'])]
    print server
    return "服务器:"+server.encode('utf-8')+"\t用户ID:"+str(action_dict['user_id'])+"\t宠物名称:"+mon_name.encode('utf-8')+"\t星级:"+str(action_dict['star_level'])+"\t等级:"+str(action_dict['mon_level'])


def gm_action_change_monster(action_dict):
    mon_name = monster_id_name[int(action_dict['mon_tid'])]
    change_key = game_manage_define.GM_ACTION_CHANGE_KEY[action_dict['key']]
    server = all_server_dict[int(action_dict['server_id'])]
    return "服务器:"+server.encode('utf-8')+"\t用户ID:"+str(action_dict['user_id'])+"\t宠物名称:"+mon_name.encode('utf-8')+"\t修改属性 "+change_key+":"+str(action_dict['old'])+"-->"+str(action_dict['new'])


def gm_action_delete_monster(action_dict):
    mon_name = monster_id_name[int(action_dict['mon_tid'])]
    server = all_server_dict[int(action_dict['server_id'])]
    return "服务器:"+server.encode('utf-8')+"\t用户ID:"+str(action_dict['user_id'])+"\t序号:"+str(action_dict['mon_uid'])+"\t宠物名称:"+mon_name.encode('utf-8')+"\t星级:"+str(action_dict['star_level'])+"\t等级:"+str(action_dict['level'])


def gm_action_add_item(action_dict):
    item_name = item_id_name[int(action_dict['item_id'])]
    server = all_server_dict[int(action_dict['server_id'])]
    return "服务器:"+server.encode('utf-8')+"\t用户ID:"+str(action_dict['user_id'])+"\t物品:"+item_name.encode('utf-8')+str(action_dict['num'])+"个"


def gm_action_change_item(action_dict):
    item_name = item_id_name[int(action_dict['item_id'])]
    server = all_server_dict[int(action_dict['server_id'])]
    return "服务器:"+server.encode('utf-8')+"\t用户ID:"+str(action_dict['user_id'])+"\t修改属性 "+item_name.encode('utf-8')+":"+str(action_dict['old'])+"-->"+str(action_dict['new'])


def gm_action_delete_item(action_dict):
    item_name = item_id_name[int(action_dict['item_id'])]
    server = all_server_dict[int(action_dict['server_id'])]
    return "服务器:"+server.encode('utf-8')+"\t用户ID:"+str(action_dict['user_id'])+"\t物品:"+item_name.encode('utf-8')+str(action_dict['num'])+"个"


def gm_action_add_equip(action_dict):
    item_name = item_id_name[int(action_dict['tid'])]
    server = all_server_dict[int(action_dict['server_id'])]
    return "服务器:"+server.encode('utf-8')+"\t用户ID:"+str(action_dict['user_id'])+"\t序号:"+str(action_dict['uid'])+"\t装备:"+item_name.encode('utf-8')+"\t等级:"+str(action_dict['level'])


def gm_action_change_equip(action_dict):
    old_item = item_id_name[int(action_dict['old_tid'])]
    new_item = item_id_name[int(action_dict['new_tid'])]
    server = all_server_dict[int(action_dict['server_id'])]
    return "服务器:"+server.encode('utf-8')+"\t用户ID:"+str(action_dict['user_id'])+"\t序号:"+str(action_dict['uid'])+"\t装备:"+old_item.encode('utf-8')+str(action_dict['old_level'])+"级-->"+new_item.encode('utf-8')+str(action_dict['new_level'])+"级"


def gm_action_delete_equip(action_dict):
    item_name = item_id_name[int(action_dict['tid'])]
    server = all_server_dict[int(action_dict['server_id'])]
    return "服务器:"+server.encode('utf-8')+"\t用户ID:"+str(action_dict['user_id'])+"\t序号:"+str(action_dict['uid'])+"\t装备:"+item_name.encode('utf-8')+"\t等级:"+str(action_dict['level'])


# ---------------------------服务器列表部分-------------------------------
def gm_action_insert_server(action_dict):
    state = game_define.SERVER_STATE_NAME_DICT[int(action_dict['state'])]
    hidden = SERVER_HIDDEN_NAME_DICT[int(action_dict['hidden'])]
    return "服务器:"+action_dict['server_id']+"\t"+action_dict['name'].encode('utf-8')+"\t状态:"+state.encode('utf-8')+"\t"+hidden.encode('utf-8')+"\t版本号:"+action_dict['version']+"\t开服时间:"+str(action_dict['open_time'])+"\t"+str(action_dict['url'])


def gm_action_update_server(action_dict):
    state = game_define.SERVER_STATE_NAME_DICT[int(action_dict['state'])]
    hidden = SERVER_HIDDEN_NAME_DICT[int(action_dict['hidden'])]
    return "服务器:"+action_dict['server_id']+"\t"+action_dict['name'].encode('utf-8')+"\t状态:"+state.encode('utf-8')+"\t"+hidden.encode('utf-8')+"\t版本号:"+action_dict['version']+"\t开服时间:"+str(action_dict['open_time'])+"\t"+str(action_dict['url'])


def gm_action_delete_server(action_dict):
    return "服务器:"+action_dict['server_id']


# ---------------------------版本公告-------------------------------
def gm_action_insert_version_notice(action_dict):
    return "版本:"+action_dict['version']+"\t公告:"+action_dict['notice'].encode('utf-8')


def gm_action_update_version_notice(action_dict):
    return "版本:"+action_dict['version']+"\t公告:"+action_dict['notice'].encode('utf-8')


def gm_action_delete_version_notice(action_dict):
    return "版本:"+action_dict['version']


# ---------------------------礼包兑换-------------------------------
def gm_action_insert_gift(action_dict):
    item_str = ""
    for i in xrange(1, 4):
        item_id = int(action_dict['item_id%s' % i])
        if item_id:
            item_name = item_id_name[item_id]
            item_str += item_name.encode('utf-8')+str(action_dict['item_num%s' % i])+"个\t"
    return "服务器ID:"+str(action_dict['server_id'])+"\t平台:"+str(action_dict['platform_id'])+"\t到期时间:"+action_dict['endtime']+"\t名称:"+action_dict['name'].encode('utf-8')\
           + "\t物品:"+item_str\
           + "\t金币:"+str(action_dict['gold'])+"\t钻石:"+str(action_dict['stone'])


def gm_action_edit_gift(action_dict):
    item_str = ""
    for i in xrange(1, 4):
        item_id = int(action_dict['item_id%s' % i])
        if item_id:
            item_name = item_id_name[item_id]
            item_str += item_name.encode('utf-8')+str(action_dict['item_num%s' % i])+"个\t"
    return "礼包ID:"+str(action_dict['gift_id'])+"服务器ID:"+str(action_dict['server_id'])+"\t平台:"+str(action_dict['platform_id'])+"\t到期时间:"+action_dict['endtime']+"\t名称:"+action_dict['name'].encode('utf-8')\
           + "\t物品:"+item_str\
           + "\t金币:"+str(action_dict['gold'])+"\t钻石:"+str(action_dict['stone'])


def gm_action_insert_exchange_code(action_dict):
    return "礼包ID:"+str(action_dict['gift_id'])+"\t数量:"+str(action_dict['num'])+"个"


# ---------------------------广播-------------------------------
def gm_action_update_notice(action_dict):
    notice = eval(action_dict['notice'])
    return "广播UID:"+str(notice['uid'])+"\t服务器ID:"+str(notice['server_id'])+"\t开始时间:"+notice['start_time'].strftime('%Y-%m-%d %H:%M:%S')+"\t销毁时间:"+notice['expiry_date'].strftime('%Y-%m-%d %H:%M:%S')+"\t间隔分钟数:"+str(notice['distance_time'])+"\t内容:"+notice['content']


def gm_action_delete_notice(action_dict):
    return "广播UID:"+action_dict['notice_uid']


# ---------------------------系统邮件-------------------------------
def gm_action_add_mail(action_dict):
    mail = eval(action_dict['mail'])
    if mail['item']:
        item_name = item_id_name[int(mail['item'])]
        item_str = item_name.encode('utf-8')+str(mail['item_num'])+"个"
    else:
        item_str = "无"
    if mail['monster']:
        mon_name = monster_id_name[int(mail['monster'])]
        mon_str = mon_name.encode('utf-8')+str(mail['monster_star_level'])+"星"
    else:
        mon_str = "无"
    return "服务器ID:"+str(mail['server_id'])+"\t目标玩家:"+str(mail['target_user_uid'])+"\t邮件内容:"+str(mail['title'])\
           + "\t开始日期:"+mail['send_time'].strftime('%Y-%m-%d %H:%M:%S')+"\t有效日期:"+mail['indate'].strftime('%Y-%m-%d %H:%M:%S')\
           + "\t金币:"+str(mail['gold'])+"\t钻石:"+str(mail['stone'])+"\t免费抽奖材料:"+str(mail['free_draw_material'])\
           + "\t物品:"+item_str\
           + "\t宠物:"+mon_str


def gm_action_delete_mail(action_dict):
    return "编号:"+action_dict['version']


# ---------------------------BUG管理-------------------------------
def gm_action_add_bug_mail(action_dict):
    mail = eval(action_dict['mail'])
    if mail['item']:
        item_name = item_id_name[int(mail['item'])]
        item_str = item_name.encode('utf-8')+str(mail['item_num'])+"个"
    else:
        item_str = "无"
    if mail['monster']:
        mon_name = monster_id_name[int(mail['monster'])]
        mon_str = mon_name.encode('utf-8')+str(mail['monster_star_level'])+"星"
    else:
        mon_str = "无"
    return "服务器ID:"+str(mail['server_id'])+"\t目标玩家:"+str(mail['target_user_uid'])+"\t邮件内容:"+str(mail['title'])\
           + "\t开始日期:"+mail['send_time'].strftime('%Y-%m-%d %H:%M:%S')+"\t有效日期:"+mail['indate'].strftime('%Y-%m-%d %H:%M:%S')\
           + "\t金币:"+str(mail['gold'])+"\t钻石:"+str(mail['stone'])+"\t免费抽奖材料:"+str(mail['free_draw_material'])\
           + "\t物品:"+item_str\
           + "\t宠物:"+mon_str


def gm_action_delete_bug(action_dict):
        bug = eval(action_dict['bug'])
        name = bug['player_name'].decode('utf-8')
        return "玩家uid:"+str(bug['user_uid'])+"\topen_uid:"+str(bug['user_open_id'])+"\t名字:"+name.encode('utf-8')+"\t处理结果:"+str(bug['handle'])


def gm_action_delete_bug_all(action_dict):
    return "清空bug"


# ---------------------------运营活动-------------------------------
def gm_action_change_activity(action_dict):
    data = eval(action_dict['data'])
    return str(data)


# ---------------------------配置信息-------------------------------
def gm_action_publish_config(action_dict):
    return "文件名:"+str(action_dict['file'])


def gm_action_remove_config(action_dict):
    return "文件名:"+str(action_dict['file'])


def gm_action_change_server_version(action_dict):
    server = all_server_dict[int(action_dict['server_id'])]
    return "服务器:"+server.encode('utf-8')+"\t版本:"+str(action_dict['old'])+"-->"+str(action_dict['new'])


def gm_action_change_server_config(action_dict):
    return str(action_dict['config'])

