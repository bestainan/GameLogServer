# -*- coding:utf-8 -*-


from apps.game_manager.mysql import gift_package
from apps.game_manager.mysql import exchange_code
from django.http import HttpResponseRedirect
from apps.utils import game_define
from apps.game_manager.models.game_manager import *
from apps.logs.output_action_gm import *

import string,random
import os
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

def list_to_string(lst):
    """
        把列表转成字符串 [1,2,3] 转换 1,2,3
    """
    lst_str = map(lambda x: str(x), lst)
    return ','.join(lst_str)

def exchange_code_info(request):
    """
    添加礼包类型信息
    """
    data = dict()
    _re_gift = dict()
    all_gift_dict = gift_package.get_all_gift()
    for key, val in all_gift_dict.items():
        _re_gift[val['id']] = val['name']
    data['gift_name_val'] = _re_gift.items()
    return render_to_response("exchange_code/exchange_code.html", data,RequestContext(request))



def mkcode(length):
    list = string.uppercase + string.lowercase + "0123456789"
    # print list
    code = string.join(random.sample(list,length),sep='')
    return code

def _exchange_code(num):
    code_list = []
    for index in xrange(num):
        code = mkcode(game_define.EXCHANGE_CODE_LEN)
        code_list.append(code)
    return code_list

def exchange_code_generate(request):
    """
    编辑礼包类型信息
    """
    gift_id = int(request.REQUEST.get("gift_id"))
    num = int(request.REQUEST.get("num"))
    code_list = _exchange_code(num)
    for code in code_list:
        exchange_code.insert_exchange(code,gift_id)

    # 操作日志记录
    manager = GameManager.get_by_request(request)
    insert_action_insert_exchange_code(manager, gift_id, num)

    return HttpResponseRedirect('/Tyranitar6/server/exchange_code_info/')

def exchange_code_output_csv(request):
    """
    导出CVS
    """
    path = None
    path = exchange_code.output_csv()
    if path:
        wrapper = FileWrapper(file(path))
        response = HttpResponse(wrapper, content_type='application/csv')
        response['Content-Length'] = os.path.getsize(path)
        response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(path)
        return response
    else:
        # 导出失败
        pass
