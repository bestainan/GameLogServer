# -*- coding:utf-8 -*-
"""
    充值查询 当天查mysql 非当天读文件
"""
import datetime
from apps.game_manager.mysql.mysql_connect import mysql_connection
from apps.game_manager.util import dat_log_util
from apps.logs import daily_log_dat
from apps.game_manager.views.log import daily_log

READ_FILE_FLODER = 'tables'
READ_FILE_NMAE = 'RECHARGE_LST'
# 全局变量大写区分
CUR_SERVER_ID = CUR_UID_ID = 0


def get_table(search_start_date, search_end_date, server_id=-1, uid=-1):
    # 声明全局变量来接收参数 省去函数参数
    global CUR_SERVER_ID, CUR_UID_ID
    CUR_SERVER_ID = int(server_id)
    try:
        CUR_UID_ID = int(uid)
    except:
        CUR_UID_ID = 0
    # 取当天时间 并转换时间戳
    now_date = datetime.date.today().strftime("%m/%d/%Y")
    now_date = datetime.datetime.strptime(now_date, "%m/%d/%Y").date()
    table_lst = []

    # ##情况一 只是当天 只读mysql
    if search_start_date == search_end_date and search_end_date == now_date:
        tmp_list = mysql_filter(mysql_search(now_date, now_date))
        table_lst.extend(tmp_list)

    # ##情况二 同一天不是当天 只读一天文件
    elif search_start_date == search_end_date and search_end_date != now_date:
        tmp_dict = file_search(search_end_date, search_end_date)
        table_lst = file_filter(tmp_dict)

    # ##情况三 多天到当天 先读文件到昨天+再读mysql今天
    elif search_start_date < search_end_date and search_end_date == now_date:
        tmp_dict = file_search(search_start_date, (search_end_date - datetime.timedelta(days=1)))
        table_lst.extend(file_filter(tmp_dict))

        tmp_list = mysql_search(now_date, now_date)
        table_lst.extend(mysql_filter(tmp_list))

    # ##情况四 多天不到当天 只读文件
    elif search_start_date < search_end_date and search_end_date != now_date:
        tmp_dict = file_search(search_start_date, search_end_date)
        table_lst = file_filter(tmp_dict)

    return table_lst


# 读mysql
def mysql_search(start_date_date, end_date_date):
    """
    查询时间段内的所有数据
    """
    global CUR_SERVER_ID, CUR_UID_ID
    if CUR_UID_ID:
        connect = mysql_connection.get_log_mysql_connection()
        sql = "select * from EVENT_ACTION_RECHARGE_PLAYER_{date} where '{start_time}' <= log_time and log_time <= date_add('{end_time}', interval 1 day) and uid = '{uid_id}';"\
            .format(
                date=str(end_date_date).replace('-', ''),
                start_time=start_date_date,
                end_time=end_date_date,
                uid_id=int(CUR_UID_ID),
            )
        # print sql

    # 情况二 无效UID 输出全部表
    else:
        print()
        connect = mysql_connection.get_log_mysql_connection()
        sql = "select * from EVENT_ACTION_RECHARGE_PLAYER_{date} where '{start_time}' <= log_time and log_time <= date_add('{end_time}', interval 1 day);"\
            .format(
                date=str(end_date_date).replace('-', ''),
                start_time=start_date_date,
                end_time=end_date_date,
            )
        # print sql

    return connect.query(sql)


# 读文件
def file_search(start_date, end_date):
    global CUR_SERVER_ID
    # 时间判定路径
    new_log_dict = dat_log_util.read_file_with_filename_dict(READ_FILE_NMAE, start_date, end_date, CUR_SERVER_ID, READ_FILE_FLODER)

    return new_log_dict


# 过滤mysql
def mysql_filter(mysql_dist):
    global CUR_SERVER_ID, CUR_UID_ID
    temp_lst = []

    # if CUR_CHANNEL_ID >= 0:
    #     log_dist = daily_log_dat.filter_logs(log_dist, function=lambda x: x['platform_id'] == CUR_CHANNEL_ID)
    if CUR_SERVER_ID >= 0:
        mysql_dist = daily_log_dat.filter_logs(mysql_dist, function=lambda x: x['server_id'] == CUR_SERVER_ID)
    if -1 == CUR_SERVER_ID:
        mysql_dist = mysql_dist

    ser_lst, platform_lst = daily_log._get_server_list(None, None)
    for each_item in mysql_dist:
        user_log_time = each_item['log_time'].strftime("%Y-%m-%d %H:%M:%S")
        user_uid = int(each_item['uid'])
        user_add_rmb = each_item['add_rmb']
        user_order_id = each_item['order_id']
        user_old_rmb = int(each_item['old_rmb'])
        user_server_id = int(each_item['server_id'])
        user_platform_id = int(each_item['platform_id'])

        if user_old_rmb == 0:
            user_first_cost = "是"
        else:
            user_first_cost = "否"
        # 取服务器 平台名字
        user_ser_str, user_platform_str = "", ""
        for each_ser_dict, each_plat_dict in zip(ser_lst, platform_lst):
            if user_platform_id == int(each_plat_dict['id']):
                user_platform_str = each_plat_dict['name']
            if user_server_id == int(each_ser_dict['id']):
                user_ser_str = each_ser_dict['name']
        if CUR_UID_ID:
            if user_uid == CUR_UID_ID:
                row_lst = [
                    user_log_time,
                    user_uid,
                    user_add_rmb,
                    user_order_id,
                    user_first_cost,
                    user_ser_str,
                    user_platform_str,
                ]
                temp_lst.append(row_lst)
        else:
            row_lst = [
                user_log_time,
                user_uid,
                user_add_rmb,
                user_order_id,
                user_first_cost,
                user_ser_str,
                user_platform_str,
            ]
            temp_lst.append(row_lst)

    return temp_lst


# 过滤日志
def file_filter(log_dist):
    global CUR_SERVER_ID, CUR_UID_ID
    temp_lst = []
    if CUR_UID_ID:
        temp_lst = log_dist.get(CUR_UID_ID, [])
    else:
        for key, value in log_dist.items():
            for index in value:
                temp_lst.append(index)

    return temp_lst

# mysql_search(datetime.date(2015,06,24),datetime.date(2015,06,24))
# print get_table(datetime.date(2015,07,01),datetime.date(2015,07,01),10003,-1,1)