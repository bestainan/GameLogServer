# -*- coding: utf-8 -*-
"""
    加密解密
"""

FIRST_KEY = 'zgamecn_pocketmon_'

import base64

def encrypt(content, uid):
    """
          加密
        Arg:
            content 加密内容
    """
    content = str(content)
    content_byte_array = bytearray(content)

    key = bytearray(FIRST_KEY + str(uid))

    content_length = len(content_byte_array)
    key_length = len(key)
    for i in xrange(content_length):
        content_byte_array[i] = content_byte_array[i] ^ key[i % key_length]

    return base64.b64encode(str(content_byte_array))

def decrypt(content, uid):
    """
        解密
        Arg:
            content 解密内容
    """
    # lens = len(content)
    # lenx = lens - (lens % 4 if lens % 4 else 4)
    # try:
    #     content = base64.decodestring(content[:lenx])
    # except:
    #   pass

    content = base64.b64decode(str(content))

    content_byte_array = bytearray(str(content))

    key = bytearray(FIRST_KEY + str(uid))

    content_length = len(content_byte_array)
    key_length = len(key)
    for i in xrange(content_length):
        content_byte_array[i] = content_byte_array[i] ^ key[i % key_length]
    return str(content_byte_array)

def decrypt_split(content, uid, sep=','):
    """
        解密并拆分
    """
    str_de = decrypt(content, uid)
    str_lst = str_de.split(sep)
    return str_lst

