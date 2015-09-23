# -*- coding:utf-8 -*-

"""
    游戏管理员账号数据类
    create table admin_manager(
        id int not null primary key auto_increment,
        account char(200) unique not null default '',
        password char(200) not null default '',
        name char(200) not null default '',
        permissions char(200) not null default '',
        last_login_ip char(20) default '',
        last_login_time datetime default null,
        description char(200) default ''
    );
"""
import hashlib
from apps.game_manager.models.game_manager import GameManager
from apps.game_manager.mysql.mysql_connect.mysql_connection import get_game_manager_mysql_connection


def get_super_manager():
    """
        获取超级管理员
    """
    sql = "SELECT * FROM admin_manager WHERE permissions='%s'" % str('Super')
    data = get_game_manager_mysql_connection().get(sql)
    if data:
        _gm = GameManager()
        _gm.uid = data['id']
        _gm.account = data['account']
        _gm.username = data["password"]
        _gm.name = data["name"]
        _gm.description = data["description"]
        _gm.permissions = data["permissions"]
        _gm.last_login_ip = data["last_login_ip"]
        _gm.last_login_time = data["last_login_time"]
        print("super = "  + str(_gm))
        return _gm
    else:
        return None


def insert_game_manager(game_manager):
    """
        插入一个管理员
    """
    sql = "INSERT INTO admin_manager(account, password, name, permissions,description) VALUES('%s','%s','%s','%s','%s')" %\
          (game_manager.account,
           hashlib.md5(game_manager.password).hexdigest(),
           game_manager.name,
           game_manager.permissions,
           game_manager.description,
           )
    get_game_manager_mysql_connection().execute(sql)


def update_game_manager_login_dat(uid, login_ip, login_time):
    """
        更新管理员登录ip和时间
    """
    sql = "UPDATE admin_manager SET last_login_ip='%s',last_login_time='%s' WHERE id=%s " % (login_ip, login_time.strftime("%Y-%m-%d %H:%M:%S"), uid)
    get_game_manager_mysql_connection().execute(sql)


def get_game_manager(account):
    """
        获取游戏管理员账号
    """
    sql = "SELECT * FROM admin_manager WHERE account='%s'" % account
    data = get_game_manager_mysql_connection().get(sql)
    if data:
        _gm = GameManager()
        _gm.uid = data['id']
        _gm.account = data['account']
        _gm.password = data["password"]
        _gm.name = data["name"]
        _gm.description = data["description"]
        _gm.permissions = data["permissions"]
        return _gm
    else:
        return None

