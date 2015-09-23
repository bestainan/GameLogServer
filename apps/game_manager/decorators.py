#-*- coding:utf-8 -*-
from django.http import HttpResponseRedirect

from apps.game_manager.models.game_manager import GameManager

def require_permission(view_func):
    """
    装饰器，用于判断管理后台的帐号是否有权限访问
    """
    def wrapped_view_func(request, *args, **kwargs):
        path = request.path
        moderator = GameManager.get_by_request(request)

        # # 管理员信息失效
        if moderator is None:
            return HttpResponseRedirect("/Tyranitar6/login/")
        # 查询权限
        if not moderator.is_allow(path):
            return HttpResponseRedirect("/Tyranitar6/login/")
        else:
            re = view_func(request, *args, **kwargs)
            return re


    return wrapped_view_func


