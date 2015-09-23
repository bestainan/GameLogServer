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
    sql_con = get_game_manager_mysql_connection()
    data = sql_con.query(sql)[0]
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
        return _gm
    else:
        return None

def insert_game_manager(game_manager):
    """
        插入一个管理员
    """
    sql = "INSERT INTO admin_manager(account, password, name, description, permissions ) VALUES('%s','%s','%s','%s','%s')" % (game_manager.account, hashlib.md5(game_manager.password).hexdigest(), game_manager.name, game_manager.description, game_manager.permissions)
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
        _gm.last_login_ip = data["last_login_ip"]
        _gm.last_login_time = data["last_login_time"]
        return _gm
    else:
        return None


def get_game_manager_with_id(manager_id):
    """
        用ID 获取管理员
    """
    sql = "SELECT * FROM admin_manager WHERE id=%s" % manager_id
    data = get_game_manager_mysql_connection().get(sql)
    if data:
        _gm = GameManager()
        _gm.uid = data['id']
        _gm.account = data['account']
        _gm.password = data["password"]
        _gm.name = data["name"]
        _gm.description = data["description"]
        _gm.permissions = data["permissions"]
        _gm.last_login_ip = data["last_login_ip"]
        _gm.last_login_time = data["last_login_time"]
        return _gm
    else:
        return None

def update_admin_password(game_manager):
    '''
    单纯修改密码
    '''
    sql = "update admin_manager set password = '{password}' where id = '{uid}';".\
    format(password = hashlib.md5(game_manager.password).hexdigest(),
           uid = game_manager.uid)
    get_game_manager_mysql_connection().execute(sql)


def update_game_manager(game_manager):
    """
    修改一个管理员
    """
    sql = "update admin_manager set account = '{account}' ,password = '{password}', name ='{name}', permissions = '{permission}', description='{description}' where account = '{account}';".\
        format(account = game_manager.account,
               password = hashlib.md5(game_manager.password).hexdigest(),
               name = game_manager.name.encode('utf8'),
               description = game_manager.description.encode('utf8'),
               permission = game_manager.permissions,
               )
    get_game_manager_mysql_connection().execute(sql)

def update_game_infomation(game_manager):
    """
    修改一个管理员信息
    """
    sql = "update admin_manager set account = '{account}' , name ='{name}', permissions = '{permission}', description='{description}' where account = '{account}';".\
        format(account = game_manager.account,
               password = hashlib.md5(game_manager.password).hexdigest(),
               name = game_manager.name.encode('utf8'),
               description = game_manager.description.encode('utf8'),
               permission = game_manager.permissions,
               )
    get_game_manager_mysql_connection().execute(sql)


def del_admin_by_id(id):
    sql = "delete from admin_manager where id = {id}".format(id = id)
    sql_con = get_game_manager_mysql_connection()
    try:
        sql_con.query(sql)
    except:
        pass


def get_manager_account_name():
    """
        获取游戏管理员账号
    """
    sql = "SELECT account,name FROM admin_manager"
    data = get_game_manager_mysql_connection().query(sql)
    if data:
        return data
    else:
        return None
