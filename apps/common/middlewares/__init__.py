#-*- coding: utf8 -*-
from apps.views.main import internal_server_error

def middleware_exception(func):
    def _func(self, request, *args, **kwargs):
        try:
            return func(self, request, *args, **kwargs)
        except Exception:
            return internal_server_error(request, mail_admin=True)
    return _func
