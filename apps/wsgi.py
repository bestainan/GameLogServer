#!usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import manage

reload(sys)
sys.setdefaultencoding('utf8')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apps.settings.test")

from django.core.handlers.wsgi import WSGIHandler
from django.conf import settings
# manage.init_app(settings)
application = WSGIHandler()