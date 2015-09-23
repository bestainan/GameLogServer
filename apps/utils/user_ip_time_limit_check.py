# -*- coding:utf-8 -*-

"""
    限制玩家发送消息的频率 发送过快的返回False
"""
import time

# 接受请求间隔时间
IP_LIMIT_TIME = 0.05

ip_time_dict = dict()


def check_ip_time_limit(user_ip):
    cur_time = time.time()
    last_time = ip_time_dict.get(user_ip, 0)

    if cur_time - last_time > IP_LIMIT_TIME:
        ip_time_dict[user_ip] = cur_time
        return True

    return False



