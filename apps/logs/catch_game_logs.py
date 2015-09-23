# -*- coding:utf-8 -*-

"""
    抓取日志
    要伴随服务器开启而开启
"""
import datetime
import os
import time
import pickle
import datetime
import urllib2

# 日志保存路径
LOG_SERVER_PATH = "http://115.159.77.250:8086/PIKA_pc_event_%s/PIKA_pc_event_%s_00000"
PARSE_OUT_FILE = os.getcwd() + "/parse/"
LOCAL_LOG_START_DATE = '2015-05-21'

class CatchData(object):
    # 抓取间隔时间
    catch_dis_time = 300
    #最后抓取日期
    last_catch_logs_date = None
    # 按照日期拆分的日志
    date_logs_dict = dict()
    # 按照日志拆分的用户uid日志
    date_uid_dict = dict()
    # 按照日志拆分的设备ID日志
    date_device_id_dict = dict()
    #按照日志拆分的账号日志
    date_account_id_dict = dict()

    def put(self):
        """
            保存配置
        """
        out_put_file = open(PARSE_OUT_FILE, 'w')
        dat_dict = dict()
        dat_dict['last_catch_logs_date'] = self.last_catch_logs_date
        dat_dict['last_catch_logs_line_num'] = self.last_catch_logs_line_num
        pickle.dump(dat_dict, out_put_file)
        out_put_file.close()

    def load(self):
        """
            加载
        """
        if os.path.exists(PARSE_OUT_FILE):
            out_put_file = open(PARSE_OUT_FILE, 'r')
            dat_dict = eval(pickle.load(out_put_file))
            self.last_catch_logs_date = dat_dict['last_catch_logs_date']
            self.last_catch_logs_line_num = dat_dict['last_catch_logs_line_num']
            out_put_file.close()

# 开启新进程执行
def start_catch_logs():
    catch_data = CatchData()
    catch_data.load()
    while True:
        #计算起始日期
        if not catch_data.last_catch_logs_date:
            catch_data.last_catch_logs_date = datetime.datetime.strptime(LOCAL_LOG_START_DATE, "%Y-%m-%d").date()
        print("抓取日期 %s 日志" % catch_data.last_catch_logs_date)
        url_path = LOG_SERVER_PATH % (catch_data.last_catch_logs_date, catch_data.last_catch_logs_date)
        url = urllib2.urlopen(url_path)
        if url.msg == 'OK':
            log_lines = url.readlines()
            total_lines = len(log_lines)
            # 解析获取日志并添加
            log_lines = log_lines[catch_data.last_catch_logs_line_num : total_lines]
            parse_game_log(log_lines)

            #如果不是今天 说明日志已经结束下次加载第二天
            if catch_data.last_catch_logs_date != datetime.date.today():
                catch_data.last_catch_logs_date += datetime.timedelta(days=1)
                catch_data.last_catch_logs_line_num = 0
            else:
                # 是今天就记录已经加载的行数 下次增量更新
                catch_data.last_catch_logs_line_num = total_lines
            # 保存抓取状态信息
            # catch_data.put()
        time.sleep(60)


def parse_game_log(log_lines):
    """
        解析
    """
    print("准备解析日志 " + str(len(log_lines)))
    pass
    # from apps.logs import daily_log_dat
    # from apps.logs.parse_action import log_parse
    # for _log in log_lines:
    #     _log = _log.strip()
    #     log_instance = log_parse(_log)
    #     daily_log_dat.all_log_lst.append(log_instance)
    # print("解析后日志数量 " + str(daily_log_dat.all_log_lst))





