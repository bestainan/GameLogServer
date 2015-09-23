#coding:utf-8
from apps.game_manager.mysql.mysql_connect.mysql_connection import get_game_manager_mysql_connection
from apps.game_manager import game_manage_define
def get_table():
    row_list = []
    temp = []
    mysql_connect = get_game_manager_mysql_connection()
    sql = "SELECT id, account, name,permissions, last_login_ip, last_login_time, description FROM admin_manager where permissions != 'Super';"
    results = mysql_connect.query(sql)
    for _dic in results:
        temp.append(_dic['id'])
        temp.append(_dic['account'])
        temp.append(_dic['name'])
        temp.append(game_manage_define.MANAGER_PERMISSION_EN_TO_CN[_dic['permissions']])
        temp.append(_dic['last_login_ip'])
        temp.append(_dic['last_login_time'])
        temp.append(_dic['description'])
        row_list.extend([temp])
        temp = []
    return row_list

