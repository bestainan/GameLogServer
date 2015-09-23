#coding:utf-8

from apps.game_manager.mysql.mysql_connect import mysql_connection

def search(start_date_date,end_date_date):
    '''
    查询时间段内的所有数据

    '''
    connect = mysql_connection.get_log_mysql_connection()
    sql = "select uid,add_rmb from EVENT_ACTION_RECHARGE_PLAYER where" \
          " '{start_time}' <= log_time and log_time <= date_add('{end_time}', interval 1 day);"\
        .format(
        start_time = start_date_date,
        end_time = end_date_date,
    )
    return connect.query(sql)

def get_table(start_date_date,end_date_date):
    row_list = {}
    all_sreach_day_dic = search(start_date_date,end_date_date)
    for dic_list in all_sreach_day_dic:
        if dic_list['uid'] not in row_list:
            row_list[dic_list['uid']] = dic_list['add_rmb']
        else:
            row_list[dic_list['uid']] += dic_list['add_rmb']

    row_list = sorted(row_list.items(),key = lambda d:d[1], reverse=True)
    top_num = xrange(1,len(row_list))
    new_list_row = []
    for row,num in zip(row_list,top_num):
        new_list_row.append((num,row[0],row[1]))

    return new_list_row













