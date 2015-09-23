# -*- coding:utf-8 -*-

"""
    获取对应memcache数据
"""

import pickle
from apps.lib.memcache_client import MemcacheClient


def get_cmem_val(server_url, key):
    """
        获取数据值
    """
    cmem = MemcacheClient(server_url)
    val = cmem.get(key)
    if val:
        return pickle.loads(val)
    else:
        return val

def get_cmem_val_no_pick(server_url, key):
    """
        获取数据值 不腌制
    """
    cmem = MemcacheClient(server_url)
    val = cmem.get(key)
    return val

def put_cmem_val_no_pick(server_url, key, val):
    """
        保存CMEM值 不腌制
    """
    cmem = MemcacheClient(server_url)
    old_val = pickle.loads(cmem.get(key))
    legality = _check_legality(old_val, val)
    if legality:
        val = cmem.set(key, val)
        return val
    else:
        return False

def put_cmem_val(server_url, key, val):
    """
        保存CMEM值
    """
    cmem = MemcacheClient(server_url)
    old_val = pickle.loads(cmem.get(key))
    legality = _check_legality(old_val, val)
    if legality:
        val = cmem.set(key, pickle.dumps(val))
        return val
    else:
        return False


def _check_legality(old_val, new_val):
    """
        检测数值合法性
        1. 所有的key保持一致
        2. 值类型保持一致
    """
    if not isinstance(old_val, dict) or not isinstance(new_val, dict):
        print old_val,new_val
        return False
    old_key = old_val.keys()
    new_key = new_val.keys()
    if len(old_key) != len(new_key):
        return False
    for _key in old_key:
        if _key not in new_key:
            return False
        old_val_type = type(old_val[_key])
        new_val_type = type(new_val[_key])
        if old_val_type != new_val_type:
            return False
    return True











