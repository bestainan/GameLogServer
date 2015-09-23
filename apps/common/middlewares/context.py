#-*- coding: utf8 -*-

from apps.common.middlewares import middleware_exception
from apps.utils.django import DjangoRequestContext



class RKContextMiddleware(object):
    @middleware_exception
    def process_request(self, request):
        request.request_context = DjangoRequestContext(request)  # 初始化web框架无关的request_context实例


    @middleware_exception
    def process_response(self, request, response):

        return response
