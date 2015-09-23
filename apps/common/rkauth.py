#-*- coding: utf8 -*-
import time

from django.conf import settings

from apps.game_manager.models.game_manager import GameManager


# def get_rkauth_signature(rk_uid, openid, openkey, timestamp, server_id):
#     """生成rkauth签名"""
#     rkauth_fields = {}
#     rkauth_fields['rk_uid'] = rk_uid
#     rkauth_fields['openid'] = openid
#     rkauth_fields['openkey'] = openkey
#     rkauth_fields['ts'] = timestamp
#     rkauth_fields['SECRET_KEY'] = settings.SECRET_KEY
#     rkauth_fields['server_id'] = server_id
#
#     return GameManager.build_rkauth_signature(rkauth_fields)
#
# def get_user_from_cookie(cookies):
#     """验证rkauth签名，并且返回验证后的用户ID"""
#     # print("cookies: "+str(cookies))
#     rkauth_signature = cookies.get('rkauth_token')
#
#     rkauth_fields = {}
#     rkauth_fields['rk_uid'] = cookies.get('rk_uid')
#     rkauth_fields['openid'] = cookies.get('tx_openid')
#     rkauth_fields['openkey'] = cookies.get('tx_openkey')
#     rkauth_fields['ts'] = cookies.get('ts') # 登录时间
#     rkauth_fields['SECRET_KEY'] = settings.SECRET_KEY
#     rkauth_fields['server_id'] = cookies.get('server_id')
#
#     built_signature = build_rkauth_signature(rkauth_fields)
#     from apps.platform.platform import conf
#     # return {'rk_uid': rkauth_fields['rk_uid'], 'openid': rkauth_fields['openid'], 'openkey': rkauth_fields['openkey'], 'ts': rkauth_fields['ts']}
#     if rkauth_signature == built_signature and rkauth_fields['server_id'] == str(conf['server_id']):
#         return {'rk_uid': rkauth_fields['rk_uid'], 'openid': rkauth_fields['openid'], 'openkey': rkauth_fields['openkey'], 'ts': rkauth_fields['ts']}
#     else:
#         return None
#
# def get_user_from_context(request_context):
#     """验证rkauth签名，并且返回验证后的用户ID"""
#     rkauth_signature = request_context.get_parameter('rkauth_token')
#     rkauth_fields = {}
#     rkauth_fields['rk_uid'] = request_context.get_parameter('rk_uid')
#     rkauth_fields['openid'] = request_context.get_parameter('tx_openid')
#     # rkauth_fields['openkey'] = request_context.get('tx_openkey')
#     rkauth_fields['ts'] = request_context.get_parameter('ts') # 登录时间
#     rkauth_fields['SECRET_KEY'] = settings.SECRET_KEY
#     rkauth_fields['server_id'] = request_context.get_parameter('server_id')
#
#     built_signature = build_rkauth_signature(rkauth_fields)
#     from apps.platform.platform import conf
#     if rkauth_signature == built_signature and rkauth_fields['server_id'] == str(conf['server_id']):
#         return {'rk_uid': rkauth_fields['rk_uid'], 'openid': rkauth_fields['openid'], 'ts': rkauth_fields['ts']}
#     else:
#         return None

# def auth_cookie(request_context, is_company):
#     """基于cookie的用户认证"""
#     # print("request_context: "+str(request_context))
#     user_cookie = get_user_from_cookie(request_context.cookies)
#     # print("auth_cookie = " + str(user_cookie))
#     if request_context.path == '/':
#         openid = request_context.params.get('openid')
#         openkey = request_context.params.get('openkey')
#
#         if is_company:  # 如果是自己公司IP用于测试的默认是0 避免干扰统计
#             platform_id = 0
#
#         if openid is None or openkey is None:
#             return None
#
#         openid = str(openid)
#         openkey = str(openkey)
#
#         # cookie中的时间戳超过一个小时，强制重新认证
#         if isinstance(user_cookie, dict) and ((int(time.time()) - int(user_cookie['ts'])) > 3600):
#             user_cookie = None
#
#         if isinstance(user_cookie, dict) and openid == user_cookie['openid'] and openkey == user_cookie['openkey']:
#             # user_cookie['platform_id'] = platform_id
#             return user_cookie
#         else:
#             rk_uid = AccountMapping.get_user_id(openid)
#             return {'rk_uid': rk_uid, 'openid': openid, 'openkey': openkey} # , 'platform_id': platform_id
#     else:
#         return user_cookie

