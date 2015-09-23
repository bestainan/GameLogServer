# -*- coding: utf-8 -*-

"""
    记录兑换码所属礼包
    create table gift_package(
        id int not null primary key auto_increment,
        platform_id int not null default '0',
        server_ids char(255) not null default '',
        time datetime not null,
        endtime datetime not null,
        name char(255) not null default '',
        item_id1 int not null default '0',
        item_num1 int not null default '0',
        item_id2 int not null default '0',
        item_num2 int not null default '0',
        item_id3 int not null default '0',
        item_num3 int not null default '0',
        gold int not null default '0',
        stone int not null default '0'
    );
Alter table gift_package add column item_type1  int not null default '0';
Alter table gift_package add column item_type2  int not null default '0';
Alter table gift_package add column item_type3  int not null default '0';
"""

import os
import csv
from apps import utils
from django.conf import settings as _settings
import datetime
from apps.game_manager.mysql.mysql_connect import mysql_connection


OUTPUT_PATH = _settings.MEDIA_ROOT + '/mysql_dump/'
OUTPUT_FILE_NAME = "gift_package.csv"

def edit(server_ids,platform_id, endtime, name,  item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone,id):
    """
        修改礼包
    """
    sql = "UPDATE gift_package SET " \
          "server_ids = '%s', " \
          "platform_id = %s, " \
          "endtime = '%s', " \
          "name = '%s', " \
          "item_id1 = %s, " \
          "item_num1 = %s, " \
          "item_id2 = %s, " \
          "item_num2 = %s, " \
          "item_id3 = %s, " \
          "item_num3 = %s, " \
          "gold = %s, " \
          "stone = %s " \
          "WHERE id = %s" %\
          (server_ids, platform_id, endtime, name,  item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone,id)
    mysql_connection.get_game_manager_mysql_connection().execute(sql)

def insert(server_ids, platform_id, endtime, name,  item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone):
    """
        插入兑换码
    """
    _insert_table(server_ids, platform_id, endtime, name,  item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone)


def _insert_table(server_ids='',platform_id=0, endtime="", name="",  item_id1=0, item_num1=0, item_id2=0, item_num2=0, item_id3=0, item_num3=0, gold=0, stone=0):

    now_datetime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sql = "INSERT INTO gift_package(server_ids,platform_id,time, endtime, name,item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone) VALUES ('%s',%s,'%s','%s','%s',%s,%s,%s,%s,%s,%s,%s,%s)"\
          % (server_ids,platform_id,now_datetime,endtime, name,item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone)

    mysql_connection.get_game_manager_mysql_connection().execute(sql)

def clear_all():
    """
        清楚gift_package
    """
    mysql_connection.get_game_manager_mysql_connection().execute("DELETE FROM gift_package")

def get_all_gift():
    """
        获取当前礼包列表
    """
    dat_lst = mysql_connection.get_game_manager_mysql_connection().query("SELECT * FROM gift_package")
    gift_dict = dict()
    for item in dat_lst:
        act = dict()
        id = int(item['id'])
        platform_id = int(item['platform_id'])
        server_int_lst = utils.string_split_to_int_list(item['server_ids'],',')
        time = item['time'].date()
        endtime = item['endtime'].date()
        name = item['name']
        item_id1 = int(item['item_id1'])
        item_num1 = int(item['item_num1'])
        item_id2 = int(item['item_id2'])
        item_num2 = int(item['item_num2'])
        item_id3 = int(item['item_id3'])
        item_num3 = int(item['item_num3'])
        gold = int(item['gold'])
        stone = int(item['stone'])

        act["id"] = id
        act["platform_id"] = platform_id
        act["server_int_lst"] = server_int_lst
        act["time"] = time
        act["endtime"] = endtime
        act["name"] = name
        act["item_id1"] = item_id1
        act["item_num1"] = item_num1
        act["item_id2"] = item_id2
        act["item_num2"] = item_num2
        act["item_id3"] = item_id3
        act["item_num3"] = item_num3
        act["gold"] = gold
        act["stone"] = stone

        gift_dict[id] = act
    return gift_dict

def get_gift(id):
    """
        获取礼包
    """
    gift_dict = get_all_gift()
    return gift_dict[id]

def delete(id):
    """
        删除礼包码
    """
    mysql_connection.get_game_manager_mysql_connection().execute("DELETE FROM gift_package WHERE id = %s" % id)




