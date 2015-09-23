# -*- coding:utf-8 -*-
from apps.game_manager.mysql.mysql_connect import mysql_connection
from apps.utils import game_define
import datetime
import pickle
import os
CATCH_LOGS_DAT ='/opt/GameLogParse'
if os.path.exists(CATCH_LOGS_DAT):
    out_put_file = open(CATCH_LOGS_DAT, 'r')
    dat_dict = pickle.load(out_put_file)

    # last_catch_logs_date = dat_dict['last_catch_logs_date']
    # self.last_catch_logs_line_num = dat_dict['last_catch_logs_line_num']
    out_put_file.close()