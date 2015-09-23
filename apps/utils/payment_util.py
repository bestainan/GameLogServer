# -*- coding:utf-8 -*-


import ctypes
import os
from django.conf import settings
import hashlib
"""
    支付部分
"""

def valid_sign_haima(data, sign, key):
    """
        验签
        Arg:
            data 同步过来的具体数据
            sign 同步过来的签名后数据
            key 应用密钥
    """

    BASE_ROOT = settings.BASE_ROOT
    lib_haima = BASE_ROOT + '/rklib/platform/haima.so'
    cdll = ctypes.CDLL(lib_haima)
    result = cdll.validsign(key, data.encode('UTF-8'), len(data), sign.encode('UTF-8'), len(sign))
    if result == 0:
        return True
    else:
        return False

def valid_sign_iapple(sign_string_buff,sign, secret_key):
    """
        ipple验签
        Arg:
            data 同步过来的具体数据
            sign 同步过来的签名后数据
            secret_key 应用密钥
    """
    if not sign_string_buff or not sign or not secret_key:
        return False

    data_md5 = hashlib.md5(sign_string_buff).hexdigest()
    private_data = data_md5 + secret_key
    # print("private_data: "+str(private_data))
    string_val_md5 = hashlib.md5(private_data).hexdigest()
    # print(string_val_md5)
    if string_val_md5 != sign:
        return False
    return True

def valid_sign_anysdk(enhanced_sign_buff, sign_string_buff, sign, enhanced_sign,private_key, enhanced_key):
    """
        anysdk验签
        Arg:
            data 同步过来的具体数据
            sign 同步过来的签名后数据
            key 应用密钥
    """
    if not enhanced_sign_buff or not enhanced_sign_buff or not private_key:
        return False

    data_md5 = hashlib.md5(enhanced_sign_buff).hexdigest()

    private_data = data_md5 + enhanced_key
    string_val_md51 = hashlib.md5(private_data).hexdigest()

    if string_val_md51 != enhanced_sign:
        return False

    sign_data_md5 = hashlib.md5(sign_string_buff).hexdigest()

    private_data = sign_data_md5 + private_key
    string_val_md52 = hashlib.md5(private_data).hexdigest()

    if string_val_md52 != sign:
        return False

    return True