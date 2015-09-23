#-*- coding: utf-8 -*-
import sys
import traceback
import datetime
import json

from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

# from rklib.utils import rkjson as json
# from rklib.web.logic import gateway
# from rklib.web.logic import ApiMethodNotExists
# from apps.common import rkauth
# from apps.utils import api_result_cache
# from apps.logs.game_error_log import err_log
# from apps.models.common import common_dat
# from apps.logics.error_message import ErrorMessage
# from apps.platform import platform

# def api(request):
#     request_context = request.request_context
#     rk_user = request_context.rk_user
#     json_result = api_result_cache.get(request_context)
#
#     if not json_result:
#         try:
#             result = check_version(request_context)
#             # result = False
#             if not result:
#                 # 打印输出 业务前
#                 result = gateway.process(request_context)     # 调用业务代码的接口
#                 # 打印输出 业务后
#                 # print("result "+ str(result))
#         except ApiMethodNotExists:
#             result = dict()
#             result['mc'] = ErrorMessage['ApiNotExist']
#             json_result = json.dumps(result)
#             return HttpResponse(json_result, content_type='application/json')
#         except Exception:
#             err_log.error(str(rk_user.uid) + " " + str(request_context.path) + " "+str(request_context.params) + str(traceback.format_exc()))
#         json_result = json.dumps(result)
#         api_result_cache.put(request_context, json_result)
#         pass
#
#     return HttpResponse(json_result, content_type='application/json')
#
#
# def index(request):
#     """应用首页"""
#     try:
#
#         config_model = common_dat.get_config()
#
#         rk_user = request.request_context.rk_user
#         platform_id = request.request_context.params.get('platid')
#         server_time = int(time.time())
#         data = dict()
#         data['openid'] = rk_user.openid
#         data['openkey'] = rk_user.openkey
#         data['uid'] = rk_user.uid
#         data['server_time'] = server_time
#
#         version_data = dict()
#         version_data['cv'] = config_model.config_version
#         version_data['gv'] = config_model.version
#         data['version'] = version_data
#
#         response = HttpResponse(json.dumps(data),  content_type='application/json; charset=UTF-8')
#
#         domain = platform.conf['domain']
#         _set_cookies(response, rk_user, domain, server_time, conf['server_id'])
#
#         # 记录玩家登录时间
#         rk_user.last_login_cookie_time = server_time
#         rk_user.platform_id = platform_id
#         rk_user.put()
#     except Exception:
#         print(traceback.format_exc())
#         err_log.error(str(rk_user.uid) + " " + str(request.request_context.path) + " "+str(request.request_context.params) + str(traceback.format_exc()))
#     return response
#
#
# def check_version(request):
#     """
#         检测游戏版本
#     """
#     config_model = common_dat.get_config()
#
#     # 判断版本
#     client_version = request.get_parameter('gv')
#     config_version = request.get_parameter('cv')
#
#     server_config_version = '0'
#     if isinstance(config_model.config_version, datetime.datetime):
#         server_config_version = str(int(time.mktime(config_model.config_version.timetuple())))
#     # print("检测游戏版本:" + str(client_version) + "  服务器端版本: " + str(config_version))
#     # print("config_version:" + str(config_version) + "  config_model.version: " + str(config_model.version))
#     # print("config_version:" + str(config_version) + "  server_config_version: " + str(server_config_version))
#     # print("game_version:" + str(client_version) + "|  server_game_version:" + str(config_model.version) + "|")
#     # print("game_version_type:" + str(type(client_version)) + "|  server_game_version_type:" + str(type(config_model.version)) + "|")
#     if client_version != config_model.version and client_version:
#         result = dict()
#         result['mc'] = ErrorMessage['ClientVersionOld']
#         return result
#     elif config_version != server_config_version and config_version:
#         result = dict()
#         result['mc'] = ErrorMessage['ClientConfigVersionOld']
#         return result
#     return None

# def _set_cookies(response, rk_user, domain, timestamp, server_id):
#     """设置客户端cookie"""
#
#     rkauth_token = rkauth.get_rkauth_signature(rk_user.uid, rk_user.openid, rk_user.openkey, timestamp, server_id)
#
#     response.set_cookie('rk_uid', value=rk_user.uid, domain=domain)
#     response.set_cookie('tx_openid', value=rk_user.openid, domain=domain)
#     response.set_cookie('tx_openkey', value=rk_user.openkey, domain=domain)
#     response.set_cookie('ts', value=timestamp, domain=domain)
#     response.set_cookie('rkauth_token', value=rkauth_token, domain=domain)
#     response.set_cookie('server_id', value=server_id, domain=domain)

def not_found(request):
    """404 Not Found handler.
    """
    request_context = request.request_context

    if request_context.path == '/api/':
        return HttpResponse(json.dumps({'rc': 0, 'mc': 404}), content_type='application/json')
    else:
        return render_to_response('404.html', {}, context_instance=RequestContext(request))

def internal_server_error(request, mail_admin=False):
    """500 Internal Server Error handler.
    """
    exc_info = sys.exc_info()

    if settings.DEBUG:
        from django.views import debug
        return debug.technical_500_response(request, *exc_info)

    try:
        request_repr = repr(request)
    except Exception:
        request_repr = "Request repr() unavailable"

    subject = 'Error (%s IP): %s' % ((request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS and 'internal' or 'EXTERNAL'), request.path)
    message = "%s\n\n%s" % ('\n'.join(traceback.format_exception(*exc_info)), request_repr)

    if mail_admin:
        from django.core.mail import mail_admins
        mail_admins(subject, message, fail_silently=True)

    print >> sys.stderr, "#" * 80
    print >> sys.stderr, 'err time: ' + str(datetime.datetime.now())
    print >> sys.stderr, "-" * 80
    print >> sys.stderr, subject
    print >> sys.stderr, "-" * 80
    print >> sys.stderr, message
    print >> sys.stderr, "#" * 80
    print >> sys.stderr
    print >> sys.stderr

    request_context = request.request_context

    if request_context.path == '/api/':
        return HttpResponse(json.dumps({'rc': 0, 'mc': 500}), content_type='application/json')
    elif request_context.path == '/' or request_context.path == '/home/':
        openid = request_context.params.get('openid')
        openkey = request_context.params.get('openkey')
        return render_to_response('qz/500.html', {'openid': openid, 'openkey': openkey}, context_instance=RequestContext(request))
    else:
        return render_to_response('500.html', {}, context_instance=RequestContext(request))
