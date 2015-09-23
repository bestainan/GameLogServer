# -*- coding:utf-8 -*-

import thread
import datetime
import os
import urllib2

import traceback
from apps.utils import game_define
from apps.logs.parse_action import log_parse


OUTPUT_PATH = '/data/scribe/log/'
OUTPUT_FILE_NAME = "PIKA_pc_event_%s/PIKA_pc_event_%s_00000"


TIME_DIS = 120

class _Load_Log_Dat(object):
    """
        服务器数据
    """
    def __init__(self):
        super(_Load_Log_Dat, self).__init__()
        self.log_dat = dict()
        self.cur_refresh_time = None
        self.is_loading = False


    def get_log_dat(self, log_date):
        return self.log_dat.get(log_date, None)

    def set_log_dat(self, log_date, dat):
        self.log_dat[log_date] = dat

    def is_contain(self, log_date):
        return log_date in self.log_dat

    def get_refresh_time(self):
        """
            获取刷新时间
        """
        return self.cur_refresh_time

    def set_refresh_time(self, _time):
        self.cur_refresh_time = _time

    # def is_need_refresh(self):
    #     if self.cur_refresh_time:
    #         now = datetime.datetime.now()
    #         dis = now - self.cur_refresh_time
    #         print("refresh " + str(dis.total_seconds()))
    #         if dis.total_seconds() > TIME_DIS:
    #             return True
    #         return False
    #     else:
    #         return True

# 日志抓取 10分钟一次 频率太高会卡
load_log_dat = _Load_Log_Dat()

def get_all_log(to_date):
    """
        获取指定日期范围日志
    """
    # 本地写入的开始日期
    log_start_date = datetime.datetime.strptime(game_define.LOCAL_LOG_START_DATE, '%Y-%m-%d').date()
    now_date = datetime.date.today()
    now_datetime = datetime.datetime.now()
    # start_date_date = from_date
    # if from_date < log_start_date:
    #     start_date_date = log_start_date

    end_date_date = to_date
    if to_date > now_date:
        end_date_date = now_date

    log_dat_lst = []
    dis_days = (end_date_date - log_start_date).days + 1
    need_refresh = load_log_dat.is_need_refresh()
    # 设置是否在加载 防止重复加载
    load_log_dat.set_refresh_time(now_datetime)
    print("need_refresh " +str(need_refresh))
    if need_refresh:
        # 更新文件
        thread.start_new_thread(_new_thread_get_from_local,(log_start_date, dis_days))
    # 遍历所有日期
    for _d in xrange(dis_days):
        _log_date = log_start_date + datetime.timedelta(days=_d)        # print("---------------加载日志日期 " + str(_log_date))
        print("从缓存加载")
        _dat_lst = load_log_dat.get_log_dat(_log_date)
        if _dat_lst:
            log_dat_lst.extend(_dat_lst)

        # # 遍历所有日期
        # for _d in xrange(dis_days):
        #     _log_date = log_start_date + datetime.timedelta(days=_d)        # print("---------------加载日志日期 " + str(_log_date))
        #
        #     if not load_log_dat.is_contain(_log_date):
        #         _dat_lst = _open_log_from_local(_log_date)
        #         print("本地加载")
        #         # 插入缓存
        #         load_log_dat.set_log_dat(_log_date, _dat_lst)
        #     elif need_refresh:
        #         _dat_lst = _open_log_from_local(_log_date)
        #         print("本地加载")
        #         # 插入缓存
        #         load_log_dat.set_log_dat(_log_date, _dat_lst)
        #     else:
        #         # 从缓存加载
        #         print("从缓存加载")
        #     _dat_lst = load_log_dat.get_log_dat(_log_date)
        #     if _dat_lst:
        #         log_dat_lst.extend(_dat_lst)

    return log_dat_lst


def _new_thread_get_from_local(log_start_date, dis_days):
    """
        开启新线程更新文件
    """
    print("线程开始加载本地文件")
    now_date = datetime.date.today()
    for _d in xrange(dis_days):
        _log_date = log_start_date + datetime.timedelta(days=_d)        # print("---------------加载日志日期 " + str(_log_date))
        if _log_date == now_date or not load_log_dat.is_contain(_log_date):
            print("线程加载本地文件 " + str(_log_date))
            # todo 未来用增量模式
            _dat_lst = _open_log_from_local(_log_date)
            load_log_dat.set_log_dat(_log_date, _dat_lst)
    thread.exit_thread()

def _open_log_from_local(log_date):
    """
        从本地加载日志文件
    """
    local_log_lst = []
    print("open log: " + str(OUTPUT_PATH + OUTPUT_FILE_NAME % (log_date, log_date)))
    if os.path.exists(OUTPUT_PATH + OUTPUT_FILE_NAME % (log_date, log_date)):
        read_file = open(OUTPUT_PATH + OUTPUT_FILE_NAME % (log_date, log_date), 'r')
        try:
            for line in read_file:
                line = line.strip('\n')
                result = log_parse(str(line))
                local_log_lst.append(result)

        except Exception:
            print("Err: read_local_log_parse error " + traceback.format_exc())
            return None
        finally:
            if read_file:
                read_file.close()
        return local_log_lst
    return local_log_lst


# def _open_log_from_log_server(log_date):
#     """
#         从日志服务器上加载日志
#         http://115.159.77.250:8086/PIKA_pc_event_2015-05-21/PIKA_pc_event_2015-05-21_00000
#     """
#     url = "http://115.159.77.250:8086/"+"PIKA_pc_event_%s/PIKA_pc_event_%s_00000" % (log_date, log_date)
#     response = None
#     read_log_lst = []
#     try:
#         response = urllib2.urlopen(url, timeout=5)
#         file_lines = response.readlines()
#         for line in file_lines:
#             line = line.strip('\n')
#             result = log_parse(str(line))
#             read_log_lst.append(result)
#
#     except urllib2.URLError as e:
#         # if hasattr(e, 'code'):
#         #     print 'Error code:', e.code
#         # elif hasattr(e, 'reason'):
#         #     print 'Reason:', e.reason
#         return None, None
#     finally:
#         if response:
#             response.close()
#     return read_log_lst, file_lines



def _write_log_lst_to_local(log_date, log_lst):
    """
        日志写入本地
    """
    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)
    write_file = open(OUTPUT_PATH + OUTPUT_FILE_NAME + '_' + str(log_date) + '.txt', 'w')
    try:
        write_file.writelines(log_lst)
    finally:
        if write_file:
            write_file.close()

def write_local_log_module_event(log_date):
    """
        日志写到本地
        log_date:2015-04-22
    """
    url = "http://115.159.77.250:8083/"+"PIKA_pc_event_%s/PIKA_pc_event_%s_00000" % (log_date, log_date)

    response = None
    read_stream = None
    try:
        response = urllib2.urlopen(url, timeout=5)
        read_stream = response.readlines()
    except urllib2.URLError as e:
        if hasattr(e, 'code'):
            print 'Error code:', e.code
        elif hasattr(e, 'reason'):
            print 'Reason:', e.reason
    finally:
        if response:
            response.close()

    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    try:
        wfile = open(OUTPUT_PATH + OUTPUT_FILE_NAME + '_' + str(log_date) + '.txt', 'w')
        print(wfile)
        wfile.writelines(read_stream)
    finally:
        if wfile:
            wfile.close()