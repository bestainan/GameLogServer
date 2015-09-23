# -*- coding: utf-8 -*-

"""
游戏服务器公告
1.记录一条显示在玩家服务器选择页面上的服务器消息
create table server_notice(
        notice text not null
    );
    Alter table server_notice add column version char(100) not null default '';
    Alter table server_notice drop column id;
"""
import datetime
from apps.game_manager.mysql.mysql_connect import mysql_connection
TIME_DIS = 60  # 1 分钟查询一次

class _ServerNotice(object):
    """
        服务器数据
    """
    def __init__(self):
        super(_ServerNotice, self).__init__()
        self.cur_server_notice = ''
        self.cur_refresh_time = None

    def get_server_notice(self):
        """
            获取服务器数据
        """
        return self.cur_server_notice

    def get_refresh_time(self):
        """
            获取刷新时间
        """
        return self.cur_refresh_time

    def is_need_refresh(self):
        if self.cur_refresh_time:
            now = datetime.datetime.now()
            dis = now - self.cur_refresh_time
            if dis.seconds > TIME_DIS:
                return True
            return False
        else:
            return True

ServerNotice = _ServerNotice()

def get_all_notice():
    """
        获取服务器公告
    """
    if ServerNotice.is_need_refresh():
        sql = "SELECT * FROM server_notice"
        notice = mysql_connection.get_game_manager_mysql_connection().query(sql)
        if notice:
            ServerNotice.cur_server_notice = notice
        else:
            ServerNotice.cur_server_notice = ''
        return ServerNotice.cur_server_notice
    else:
        return ServerNotice.cur_server_notice


def update_version_notice(notice, version):
    """
        更新公告
    """
    sql = "SELECT * FROM server_notice WHERE version = '%s' " %version
    dat = mysql_connection.get_game_manager_mysql_connection().get(sql)
    # print("dat: "+str(dat)+"notice: "+str(notice)+"version: "+str(version))
    if dat:
        mysql_connection.get_game_manager_mysql_connection().execute("UPDATE server_notice SET  notice = '%s'  WHERE  version = '%s' " %(notice,version))
    else:
        mysql_connection.get_game_manager_mysql_connection().execute("INSERT INTO server_notice(notice,version) VALUES('%s','%s')" % (notice,version))
    return dat

def get_version_notice(version):
    """
        获取服务器公告
    """
    if ServerNotice.is_need_refresh():
        sql = "SELECT * FROM server_notice WHERE version = '%s'" %version
        notice = mysql_connection.get_game_manager_mysql_connection().query(sql)
        if notice:
            ServerNotice.cur_server_notice = notice[0]
        else:
            ServerNotice.cur_server_notice = None
        return ServerNotice.cur_server_notice
    else:
        return ServerNotice.cur_server_notice

def delete_version_notice(version):
    """
        移除公告
    """
    sql = "DELETE FROM server_notice WHERE version = '%s' " %version
    mysql_connection.get_game_manager_mysql_connection().execute(sql)