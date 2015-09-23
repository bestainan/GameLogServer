# -*- coding: utf-8 -*-

import random
import game_define

"""
    礼包码生成类
"""
import string,random

def mkcode(length):
    list = string.uppercase + string.lowercase + "0123456789"
    # print list
    code = string.join(random.sample(list,length),sep='')
    return code

def exchange_code(num):
    code_list = []
    for index in xrange(num):
        code = mkcode(game_define.EXCHANGE_CODE_LEN)
        code_list.append(code)
    return code_list

