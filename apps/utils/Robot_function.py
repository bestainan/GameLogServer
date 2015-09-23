#coding:utf-8

def get_dict_key_with_value(mydict, vals):
    for key,val in mydict.items():
        if val == vals:
            return key

    return False