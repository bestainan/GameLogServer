#-*- coding: utf-8 -*-
from production import *
import os

DEBUG = True

BASE_ROOT = os.getenv('PWD')
BASE_URL = 'http://182.254.133.100'

MEDIA_ROOT = BASE_ROOT + '/static'
MEDIA_URL = BASE_URL + '/static/'

TEMPLATE_DIRS = (
    BASE_ROOT + '/apps/templates',
)

LOGIC_CFG = BASE_ROOT + '/apps/config/logic.conf'
MODEL_CFG = BASE_ROOT + '/apps/config/model.conf'
STORAGE_CFG = BASE_ROOT + '/apps/config/storage_dev.conf'
CACHE_CFG = BASE_ROOT + '/apps/config/cache_dev.conf'
CHECKER_ADDR = '127.0.0.1:11211'


