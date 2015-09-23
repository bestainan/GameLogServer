# -*- coding:utf-8 -*-

from django.conf.urls import patterns, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# 后台接口
urlpatterns = patterns('',
    (r'^Tyranitar6/', include('game_manager.urls')),
)

urlpatterns += staticfiles_urlpatterns()

handler404 = 'views.main.not_found'
handler500 = 'views.main.internal_server_error'
