# -*- coding: utf-8 -*-

"""
    记录兑换码
    create table exchange_code(
        id int not null primary key auto_increment,
        time datetime not null,
        code char(255) not null default '0',
        gift_id int not null default '0'
    );
"""

import os
import csv
from django.conf import settings as _settings
import datetime
from apps.game_manager.mysql.mysql_connect import mysql_connection


OUTPUT_PATH = '/opt/GameLogServer/static/mysql_dump/'
OUTPUT_FILE_NAME = "exchange_code.csv"

def insert_exchange(code,gift_id):
    """
        插入兑换码
    """
    _insert_table(code,gift_id)


def _insert_table(code="",gift_id=0):
    now_datetime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sql = "INSERT INTO exchange_code(time,code,gift_id) VALUES ('%s','%s',%s)"\
          % (now_datetime, code, gift_id)
    mysql_connection.get_game_manager_mysql_connection().execute(sql)

def clear_all():
    """
        清楚指定服务器统计数据
    """
    mysql_connection.get_game_manager_mysql_connection().execute("DELETE FROM exchange_code")

def delete_by_code(code):
    """
        删除兑换码
    """
    mysql_connection.get_game_manager_mysql_connection().execute("DELETE FROM exchange_code WHERE code = '%s' " % code)

def delete(time):
    """
        删除兑换码
    """
    mysql_connection.get_game_manager_mysql_connection().execute("DELETE FROM exchange_code WHERE time = '%s' " % time)

def get_exchange_code(code):
    """
        获取兑换码
    """
    sql = "SELECT * FROM exchange_code WHERE code = '%s' " % code

    dat = mysql_connection.get_game_manager_mysql_connection().query(sql)
    if not dat:
        print("get_exchange_code:not exist ")
        return None
    return dat[0]

def output_csv():
    """
        导出cvs数据
    """
    print OUTPUT_PATH
    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    sql = "SELECT time,code,gift_id FROM exchange_code"

    dat = mysql_connection.get_game_manager_mysql_connection().query(sql)
    output_file = file(OUTPUT_PATH + OUTPUT_FILE_NAME, 'w')
    names = ['time', 'code', 'gift_id']
    csv_writer = csv.DictWriter(output_file, fieldnames=names)
    names_dict = {
        'time': '时间',
        'code': '兑换码',
        'gift_id': '礼包类型'
    }
    csv_writer.writerow(names_dict)
    csv_writer.writerows(dat)
    output_file.close()
    return OUTPUT_PATH + OUTPUT_FILE_NAME


