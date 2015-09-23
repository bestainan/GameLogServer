#-*- coding: utf8 -*-
import json

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
# from rklib.utils import rkjson as json

from apps.common.middlewares import middleware_exception
from apps.utils import server_util

class RKAuthMiddleware(object):
    @middleware_exception
    def process_request(self, request):

        """用户认证中间件"""
        client_ip = server_util.get_client_ip(request)
        is_company =True
        if request.path.startswith('/Tyranitar6'):
            if not is_company:
                return HttpResponse(json.dumps({'rc': 0, 'mc': 403}), content_type='application/json')
            else:
                return

    @middleware_exception
    def process_response(self, request, response):

        return response