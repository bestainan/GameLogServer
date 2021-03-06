# -*- coding=utf-8 -*-


"""
    服务器定义
"""

# 服务器id的和名字的映射
SERVER_NAME_MAP = {
    10001:u'内部测试服务器',
    10003:u'IOS 宝石海星',
    10004:u'IOS 飞天螳螂',
    10005:u'IOS 小火龙',
    10006:u'IOS 火恐龙',
    30001:u'Android 梦幻',
    20001:u'IOS 皮卡丘',
}

SERVER_NAME_LST = [
    {'id': 10001, 'name': u'内部测试服务器'},
    {'id': 10003, 'name': u'IOS 海马 宝石海星'},
    {'id': 10004, 'name': u'IOS 海马 飞天螳螂'},
    {'id': 10005, 'name': u'IOS 海马 小火龙'},
    {'id': 10006, 'name': u'IOS 海马 火恐龙'},
    {'id': 30001, 'name': u'Android 梦幻'},
    {'id': 20001, 'name': u'IOS 皮卡丘'},
]

# CMEM持久层映射
CMEM_MAP = {
    10001: '10.66.145.119:9101',
    10003: '10.66.147.252:9101',
    10004: '10.66.147.251:9101',
    10005: '10.66.110.54:9101',
    10006: '10.66.132.110:9101',
    30001: '10.66.140.117:9101',
    20001: '10.66.147.57:9101',
}