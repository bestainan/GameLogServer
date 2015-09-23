#coding=utf-8
import sys, time
from django.conf import settings
from scribeutil import ScribeClient, SCRIBE_AVAILABLE

output = None

def scribesender(host, port, category_prefix=None):

    scribe_client = ScribeClient(host, port)
    def sender(data):
        today = time.strftime('%Y-%m-%d')
        category = category_prefix + '_' + today if category_prefix else today
        scribe_client.log(category, data)
    return sender


SCRIBE_SERVER = getattr(settings, 'SCRIBE_SERVER', '127.0.0.1')
SCRIBE_PORT = getattr(settings, 'SCRIBE_PORT', 8250)

CATEGORY_PREFIX_EVENT = getattr(settings, 'CATEGORY_PREFIX_EVENT', 'game_manager')

output = scribesender(SCRIBE_SERVER, SCRIBE_PORT, CATEGORY_PREFIX_EVENT)
