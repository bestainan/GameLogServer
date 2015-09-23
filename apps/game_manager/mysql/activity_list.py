# -*- coding: utf-8 -*-

"""
游戏运营活动
INSERT INTO activity_list (id,activity_id,server_id,  begin_time,time_length,time_distance,is_forced_open) VALUEs(1, 0, '','2015-04-30 00:00:00',500,10000, 1);
INSERT INTO activity_list (id,activity_id,server_id,  begin_time,time_length,time_distance,is_forced_open) VALUEs(2, 1, '10001','2015-04-18 00:00:00',200,100000, 0);
INSERT INTO activity_list (id,activity_id,server_id,  begin_time,time_length,time_distance,is_forced_open) VALUEs(3, 2, '10001','2015-04-18 00:00:00',200,10000, 2);
INSERT INTO activity_list (id,activity_id,server_id,  begin_time,time_length,time_distance,is_forced_open) VALUEs(4, 3, '10001','2015-05-04 00:00:00',200,10000, 2);

INSERT INTO activity_list (id,activity_id,server_id,  begin_time,time_length,time_distance,is_forced_open) VALUEs(6, 5, '10001','2015-05-05 00:00:00',3,10000, 1);
INSERT INTO activity_list (id,activity_id,server_id,  begin_time,time_length,time_distance,is_forced_open) VALUEs(7, 6, '10001','2015-05-05 00:00:00',3,10000, 1);
INSERT INTO activity_list (id,activity_id,server_id,  begin_time,time_length,time_distance,is_forced_open) VALUEs(8, 7, '10001','2015-05-05 00:00:00',3,10000, 1);
INSERT INTO activity_list (id,activity_id,server_id,  begin_time,time_length,time_distance,is_forced_open) VALUEs(9, 8, '10001','2015-05-05 00:00:00',3,10000, 1);
INSERT INTO activity_list (id,activity_id,server_id,  begin_time,time_length,time_distance,is_forced_open) VALUEs(10, 9, '10001','2015-05-05 00:00:00',3,10000, 1);
INSERT INTO activity_list (id,activity_id,server_id,  begin_time,time_length,time_distance,is_forced_open) VALUEs(11, 10, '10001','2015-05-05 00:00:00',3,10000, 1);
INSERT INTO activity_list (id,activity_id,server_id,  begin_time,time_length,time_distance,is_forced_open) VALUEs(12, 11, '10001','2015-05-05 00:00:00',3,10000, 1);
INSERT INTO activity_list (id,activity_id,server_id,  begin_time,time_length,time_distance,is_forced_open) VALUEs(13, 12, '10001','2015-05-05 00:00:00',3,10000, 1);
INSERT INTO activity_list (id,activity_id,server_id,  begin_time,time_length,time_distance,is_forced_open) VALUEs(14, 13, '10001','2015-05-05 00:00:00',3,10000, 1);
INSERT INTO activity_list (id,activity_id,server_id,  begin_time,time_length,time_distance,is_forced_open) VALUEs(20, 19, '10001','2015-05-05 00:00:00',3,10000, 1);
1.记录所有游戏活动list
create table activity_list(
        id int not null primary key,
        server_id char(200) not null default '',
        activity_id int not null default '0',
        begin_time datetime not null,
        time_length int not null default '0',
        time_distance int not null default '0',
        is_forced_open int not null default '0',

        gold int not null default '0',
        stone int not null default '0',

        free int not null default '0',
        exp int not null default '0',
        equip int not null default '0',
        monster int not null default '0',
        star int not null default '0',

        item_id1 int not null default '0',
        item_num1 int not null default '0',
        item_id2 int not null default '0',
        item_num2 int not null default '0',
        item_id3 int not null default '0',
        item_num3 int not null default '0'

    );
Alter table activity_list add column title char(100) not null default '';
Alter table activity_list add column label char(100) not null default '';
Alter table activity_list add column detail varchar(500) not null default '';
Alter table activity_list modify column detail notice text not null;
Alter table activity_list modify column new  char(250) not null default '20150618101';

Alter table activity_list add column title2 char(100) not null default '';
Alter table activity_list add column label2 char(100) not null default '';
Alter table activity_list add column detail2 varchar(500) not null default '';
Alter table table_name modify column id int not null primary key;


create table user_detail(
             id int not null primary key auto_increment,
            uid char(200) not null default '',
            install datetime not null,
             server_id int not null default '0',
             platform_id int not null default '0',
             level smallint  not null default '0',
             vip_level smallint  not null default '0',
             last_play_time datetime not null,
             gold int not null default '0',
             stone int not null default '0',
             emblem int not null default '0',
             gym_point int not null default '0',
             world_boss_point int not null default '0',
             device_id varchar(50) not null default ''
             );

    Alter table activity_list add column item_id1,item_num1,item_id2,item_num2,item_id3,item_num3,gold,stone int not null default '0';

    Alter table activity_list add column free id int not null primary key auto_increment,
    Alter table activity_list add column exp int not null default '0';
    Alter table activity_list add column equip int not null default '0';
    Alter table activity_list add column monster int not null default '0';
    Alter table activity_list add column star int not null default '0';

    Alter table activity_list add column discount int not null default '10';
    Alter table activity_list add column new bool not null;



    id 主键
    server_id 服务器条件
    activity_id 活动ID
    begin_time 开启时间
    time_length 长度
    time_distance 间隔
    is_forced_open 强制状态
"""
import datetime
from apps import utils
from apps.game_manager.mysql.mysql_connect import mysql_connection

TIME_DIS = 300  # 1 分钟查询一次

class _ActivityListDat(object):
    """
        活动列表
    """
    def __init__(self):
        super(_ActivityListDat, self).__init__()
        self.activity_dict = None
        # { id:{ dat ...}, id:{ dat ...}}


        self.cur_refresh_time = None

    def get_activity_dict(self):
        """
            获取活动数据
        """
        return self.activity_dict

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

ActivityListDat = _ActivityListDat()

def insert_activity(server_id_lst, begin_time, time_length, time_distance, is_forced_open):
    """
        插入新活动
        id int not null primary key auto_increment,
        server_id int not null default '0',//服务器id
        content char(100) not null,//活动内容
        begin_time datetime not null default '0',//开始时间
        time_length int not null default '0',//时间长度
        time_distance int not null default '0',//时间间隔
        is_forced_open int not null default False //是否强制开启
    """
    # now_datetime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sql = "INSERT INTO activity_list (server_id, begin_time,time_length,time_distance,is_forced_open) VALUES ('%s','%s',%s,%s, %s)" % (server_id_lst, str(begin_time), time_length, time_distance,is_forced_open)
    # print(sql)
    mysql_connection.get_game_manager_mysql_connection().execute(sql)


def change_activity(activity_id, server_id_lst,  begin_time, time_length, time_distance, is_forced_open, new, item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone, free, exp, equip, monster, star, discount, title, detail,label,title2,label2, detail2):
    """
    free int not null default '0',
        exp int not null default '0',
        equip int not null default '0',
        monster int not null default '0',
        star int not null default '0',
        修改新活动
    """
    sql = "UPDATE activity_list SET " \
          "server_id = '%s', " \
          "begin_time = '%s', " \
          "time_length = %s, " \
          "time_distance = %s, " \
          "is_forced_open = %s, " \
          "new = '%s', " \
          "item_id1 = %s, " \
          "item_num1 = %s, " \
          "item_id2 = %s, " \
          "item_num2 = %s, " \
          "item_id3 = %s, " \
          "item_num3 = %s, " \
          "gold = %s, " \
          "stone = %s, " \
          "free = %s, " \
          "exp = %s, " \
          "equip = %s, " \
          "monster = %s, " \
          "star = %s, " \
          "discount = %s, " \
          "title = '%s', " \
          "label = '%s', " \
          "detail = '%s', " \
          "title2 = '%s', " \
          "label2 = '%s', " \
          "detail2 = '%s' " \
          "WHERE activity_id = %s" %\
          (server_id_lst, str(begin_time), time_length, time_distance, is_forced_open, new, item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone,free, exp, equip, monster, star, discount, title,label, detail, title2,label2, detail2, activity_id)
    # print(sql)
    mysql_connection.get_game_manager_mysql_connection().execute(sql)

def get_all_activity(refresh=False):
    """
        获取当前活动列表
    """
    if ActivityListDat.is_need_refresh() or refresh:
        dat_lst = mysql_connection.get_game_manager_mysql_connection().query("SELECT * FROM activity_list")

        ActivityListDat.activity_dict = dict()

        for item in dat_lst:
            act = dict()
            id = int(item['id'])
            act_id = int(item['activity_id'])
            server_int_lst = utils.string_split_to_int_list(item['server_id'],',')

            begin_date = item['begin_time'].date()
            time_length = int(item['time_length'])
            time_distance = int(item['time_distance'])
            is_forced_open = int(item['is_forced_open'])
            item_id1 = int(item['item_id1'])
            item_num1 = int(item['item_num1'])
            item_id2 = int(item['item_id2'])
            item_num2 = int(item['item_num2'])
            item_id3 = int(item['item_id3'])
            item_num3 = int(item['item_num3'])
            gold = int(item['gold'])
            stone = int(item['stone'])
            free = int(item['free'])
            exp = int(item['exp'])
            equip = int(item['equip'])
            monster = int(item['monster'])
            star = int(item['star'])
            discount = int(item['discount'])
            title = item['title']
            label = item['label']
            detail = item['detail']
            title2 = item['title2']
            label2 = item['label2']
            detail2 = item['detail2']
            new = item['new']

            act["id"] = id
            act["activity_id"] = act_id
            act["server_int_lst"] = server_int_lst
            act["begin_date"] = begin_date
            act["time_length"] = time_length
            act["time_distance"] = time_distance
            act["is_forced_open"] = is_forced_open
            act["item_id1"] = item_id1
            act["item_num1"] = item_num1
            act["item_id2"] = item_id2
            act["item_num2"] = item_num2
            act["item_id3"] = item_id3
            act["item_num3"] = item_num3
            act["gold"] = gold
            act["stone"] = stone
            act["free"] = free
            act["exp"] = exp
            act["equip"] = equip
            act["monster"] = monster
            act["star"] = star
            act["discount"] = discount
            act["title"] = title
            act["label"] = label
            act["detail"] = detail
            act["title2"] = title2
            act["label2"] = label2
            act["detail2"] = detail2
            act["new"] = new

            ActivityListDat.activity_dict[act_id] = act

        ActivityListDat.cur_refresh_time = datetime.datetime.now()

        return ActivityListDat.activity_dict
    else:
        return ActivityListDat.activity_dict

def get_activity(activity_id, refresh=False):
    """
        获取运营活动
    """
    get_all_activity(refresh)
    return ActivityListDat.activity_dict[activity_id]
