#-*- coding: utf-8 -*-
import os

APP_ID="11122"
DEBUG = False
ENABLE_TEST = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = False
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

CONFIG_PATH = '/opt/GameServerConfig'
BASE_ROOT = os.getenv('PWD')
BASE_URL = 'http://prd.zgame.com'

TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-cn'
SITE_ID = 1
USE_I18N = False
USE_L10N = False

ALLOWED_HOSTS = ['*']

MEDIA_ROOT = BASE_ROOT + '/static'
MEDIA_URL = BASE_URL + '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 's3avlj$=vk16op_s1g!xyilse9azcu&oh#wln8_@!b+_p7-+@='

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'apps.common.middlewares.timeview.TimeviewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'apps.common.middlewares.context.RKContextMiddleware',
    'apps.common.middlewares.auth.RKAuthMiddleware',

)

#

ROOT_URLCONF = 'apps.urls'

TEMPLATE_DIRS = (
    BASE_ROOT + '/apps/templates',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'apps.common.context_processors.game_manager_processor.processor',
)

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'apps.common',
    'apps.game_manager',
)

STATICFILES_DIRS = (
    '/game_manager/static/',
)

STATIC_URL = '/static/'
STATIC_ROOT = '/opt/GameLogServer/apps/static'

# 应用相关配置
STORAGE_CFG = BASE_ROOT + '/apps/config/storage.conf'
LOGIC_CFG = BASE_ROOT + '/apps/config/logic.conf'
MODEL_CFG = BASE_ROOT + '/apps/config/model.conf'
CACHE_CFG = BASE_ROOT + '/apps/config/cache.conf'
CHECKER_ADDR = '127.0.0.1:11211'
CONFIG_RELOAD_KEY = 'config_reload'
CONFIG_VERSION = 0

BUILD_CONFIG_SCRIPT_PATH = '/opt/sites/design/BuildGameData/build.sh'

