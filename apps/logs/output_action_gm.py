# -*- coding:utf-8 -*-

from statistics import output_gm
from apps.logs.action_gm import action_super_manager_register
from apps.logs.action_gm import action_delete_manager
from apps.logs.action_gm import action_manager_register
from apps.logs.action_gm import action_manager_login
from apps.logs.action_gm import action_update_password
from apps.logs.action_gm import action_update_manager_info
from apps.logs.action_gm import action_edit_player
from apps.logs.action_gm import action_create_monster
from apps.logs.action_gm import action_change_monster
from apps.logs.action_gm import action_delete_monster
from apps.logs.action_gm import action_add_item
from apps.logs.action_gm import action_change_item
from apps.logs.action_gm import action_delete_item
from apps.logs.action_gm import action_add_equip
from apps.logs.action_gm import action_change_equip
from apps.logs.action_gm import action_delete_equip
from apps.logs.action_gm import action_insert_server
from apps.logs.action_gm import action_update_server
from apps.logs.action_gm import action_delete_server
from apps.logs.action_gm import action_insert_version_notice
from apps.logs.action_gm import action_update_version_notice
from apps.logs.action_gm import action_delete_version_notice
from apps.logs.action_gm import action_insert_gift
from apps.logs.action_gm import action_edit_gift
from apps.logs.action_gm import action_update_notice
from apps.logs.action_gm import action_delete_notice
from apps.logs.action_gm import action_add_mail
from apps.logs.action_gm import action_delete_mail
from apps.logs.action_gm import action_add_bug_mail
from apps.logs.action_gm import action_delete_bug
from apps.logs.action_gm import action_delete_bug_all
from apps.logs.action_gm import action_change_activity
from apps.logs.action_gm import action_insert_exchange_code
from apps.logs.action_gm import action_publish_config
from apps.logs.action_gm import action_remove_config
from apps.logs.action_gm import action_change_server_version
from apps.logs.action_gm import action_change_server_config


def insert_action_super_manager_register(gm):
    """
        超级管理员注册
    """
    log = action_super_manager_register.log(gm)
    output_gm.output(log)


def insert_action_delete_manager(gm, del_id):
    """
        删除一个管理员
    """
    log = action_delete_manager.log(gm, del_id)
    output_gm.output(log)


def insert_action_manager_register(gm):
    """
        管理员注册
    """
    log = action_manager_register.log(gm)
    output_gm.output(log)


def insert_action_manager_login(gm):
    """
        游戏管理员登陆
    """
    log = action_manager_login.log(gm)
    output_gm.output(log)


def insert_action_update_password(gm):
    """
        修改管理员密码
    """
    log = action_update_password.log(gm)
    output_gm.output(log)


def insert_action_update_manager_info(gm, account, name, permission_name, description):
    """
        修改管理员信息
    """
    log = action_update_manager_info.log(gm, account, name, permission_name, description)
    output_gm.output(log)


def insert_action_edit_player(manager, server_id, user_id, key, old_value, value):
    """
        修改玩家信息
    """
    log = action_edit_player.log(manager, server_id, user_id, key, old_value, value)
    output_gm.output(log)


def insert_action_create_monster(manager, server_id, user_id, monster_uid, monster_tid, star_level, level):
    """
        添加宠物
    """
    log = action_create_monster.log(manager, server_id, user_id, monster_uid, monster_tid, star_level, level)
    output_gm.output(log)


def insert_action_change_monster(manager, server_id, user_id, monster_uid, monster_tid, change_key, old_value, new_value):
    """
        修改宠物信息
    """
    log = action_change_monster.log(manager, server_id, user_id, monster_uid, monster_tid, change_key, old_value, new_value)
    output_gm.output(log)


def insert_action_delete_monster(manager, server_id, user_id, monster_uid, monster_tid, star_level, level):
    """
        删除宠物
    """
    log = action_delete_monster.log(manager, server_id, user_id, monster_uid, monster_tid, star_level, level)
    output_gm.output(log)


def insert_action_add_item(manager, server_id, user_id, item_tid, num):
    """
        添加物品
    """
    log = action_add_item.log(manager, server_id, user_id, item_tid, num)
    output_gm.output(log)


def insert_action_change_item(manager, server_id, user_id, item_id, old_value, value):
    """
        修改物品
    """
    log = action_change_item.log(manager, server_id, user_id, item_id, old_value, value)
    output_gm.output(log)


def insert_action_delete_item(manager, server_id, user_id, item_tid, del_num):
    """
        删除物品
    """
    log = action_delete_item.log(manager, server_id, user_id, item_tid, del_num)
    output_gm.output(log)


def insert_action_add_equip(manager, server_id, user_uid, equip_uid, equip_tid, equip_level):
    """
        添加装备
    """
    log = action_add_equip.log(manager, server_id, user_uid, equip_uid, equip_tid, equip_level)
    output_gm.output(log)


def insert_action_change_equip(manager, server_id, user_uid, equip_uid, equip_tid, will_edit_tid, equip_level, will_edit_tid_level):
    """
        修改装备
    """
    log = action_change_equip.log(manager, server_id, user_uid, equip_uid, equip_tid, will_edit_tid, equip_level, will_edit_tid_level)
    output_gm.output(log)


def insert_action_delete_equip(manager, server_id, user_uid, equip_uid, equip_tid, equip_level):
    """
        删除装备
    """
    log = action_delete_equip.log(manager, server_id, user_uid, equip_uid, equip_tid, equip_level)
    output_gm.output(log)


def insert_action_insert_server(manager, server_id, url, name, server_state, server_hidden, version, open_server_time):
    """
        添加服务器
    """
    log = action_insert_server.log(manager, server_id, url, name, server_state, server_hidden, version, open_server_time)
    output_gm.output(log)


def insert_action_update_server(manager, server_id, url, name, server_state, server_hidden, version, open_server_time):
    """
        更新服务器
    """
    log = action_update_server.log(manager, server_id, url, name, server_state, server_hidden, version, open_server_time)
    output_gm.output(log)


def insert_action_delete_server(manager, server_id):
    """
        删除服务器
    """
    log = action_delete_server.log(manager, server_id)
    output_gm.output(log)


def insert_action_insert_version_notice(manager, version, notice):
    """
        添加版本公告
    """
    log = action_insert_version_notice.log(manager, version, notice)
    output_gm.output(log)


def insert_action_update_version_notice(manager, version, notice):
    """
        更新版本公告
    """
    log = action_update_version_notice.log(manager, version, notice)
    output_gm.output(log)


def insert_action_delete_version_notice(manager, version):
    """
        删除版本公告
    """
    log = action_delete_version_notice.log(manager, version)
    output_gm.output(log)


def insert_action_insert_gift(manager, server_id, platform_id, endtime, name,  item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone):
    """
        添加礼包
    """
    log = action_insert_gift.log(manager, server_id, platform_id, endtime, name,  item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone)
    output_gm.output(log)


def insert_action_edit_gift(manager, server_id, platform_id, endtime, name,  item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone, gift_id):
    """
        编辑礼包
    """
    log = action_edit_gift.log(manager, server_id, platform_id, endtime, name,  item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone, gift_id)
    output_gm.output(log)


def insert_action_update_notice(manager, notice):
    """
        编辑广播
    """
    log = action_update_notice.log(manager, notice)
    output_gm.output(log)


def insert_action_delete_notice(manager, notice_uid):
    """
        删除广播
    """
    log = action_delete_notice.log(manager, notice_uid)
    output_gm.output(log)


def insert_action_add_mail(manager, mail):
    """
        添加系统邮件
    """
    log = action_add_mail.log(manager, mail)
    output_gm.output(log)


def insert_action_delete_mail(manager, version):
    """
        删除系统邮件
    """
    log = action_delete_mail.log(manager, version)
    output_gm.output(log)


def insert_action_add_bug_mail(manager, mail):
    """
        添加回复bug系统邮件
    """
    log = action_add_bug_mail.log(manager, mail)
    output_gm.output(log)


def insert_action_delete_bug(manager, del_bug):
    """
        删除玩家提的bug
    """
    log = action_delete_bug.log(manager, del_bug)
    output_gm.output(log)


def insert_action_delete_bug_all(manager):
    """
        清空玩家提的bug
    """
    log = action_delete_bug_all.log(manager)
    output_gm.output(log)


def insert_action_change_activity(manager, activity_id, server_id, begin_time, time_length, time_distance, is_forced_open, new, item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone, free, exp, equip, monster, star, discount, title, detail, label, title2, label2, detail2):
    """
        编辑运营活动
    """
    log = action_change_activity.log(manager, activity_id, server_id, begin_time, time_length, time_distance, is_forced_open, new, item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone, free, exp, equip, monster, star, discount, title, detail, label, title2, label2, detail2)
    output_gm.output(log)


def insert_action_insert_exchange_code(manager, gift_id, num):
    """
        插入兑换码
    """
    log = action_insert_exchange_code.log(manager, gift_id, num)
    output_gm.output(log)


def insert_action_publish_config(manager, file_name):
    """
        上传配置文件
    """
    log = action_publish_config.log(manager, file_name)
    output_gm.output(log)


def insert_action_remove_config(manager, file_name):
    """
        删除配置文件
    """
    log = action_remove_config.log(manager, file_name)
    output_gm.output(log)


def insert_action_change_server_version(manager, server_id, old_version, new_version):
    """
        修改服务器版本信息
    """
    log = action_change_server_version.log(manager, server_id, old_version, new_version)
    output_gm.output(log)


def insert_action_change_server_config(manager, need_update_config_dict):
    """
        修改游戏配置信息
    """
    log = action_change_server_config.log(manager, need_update_config_dict)
    output_gm.output(log)
