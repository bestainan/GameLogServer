#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys

from django.core.management import execute_from_command_line

cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(cur_dir, ".."))

def get_settings_mod(args):
    try:
        subcommand = sys.argv[1]
    except Exception:
        sys.stderr.write("Usage: python apps/manage.py shell|runserver|runfcgi [options] [args]\n")
        sys.exit(1)

    if subcommand not in ['shell', 'runserver', 'runfcgi', 'collectstatic']:
        sys.stderr.write("Usage: python apps/manage.py shell|runserver|runfcgi [options] [args]\n")
        sys.exit(1)

    if subcommand == 'shell':
        settings_mapping = {
            'prd': 'apps.settings.production',
            'stg': 'apps.settings.staging',
            'dev': 'apps.settings.test'
        }

        try:
            shell_env = args.pop()
            settings_mod = settings_mapping[shell_env]
        except Exception:
            sys.stderr.write("Usage: python apps/manage.py shell dev|stg|prd\n")
            sys.exit(1)
    else:
        serrver_env = [arg for arg in args if '--settings=' in arg]

        if serrver_env:
            settings_mod = serrver_env[0].split('=')[1]
        else:
            sys.stderr.write("Usage: python apps/manage.py runserver|runfcgi --settings=apps.settings.development|apps.settings.staging|apps.settings.production\n")
            sys.exit(1)

    return settings_mod


# def init_app(settings):

    # from rklib.core import app
    # app.init(storage_cfg_file=settings.STORAGE_CFG, logic_cfg_file=settings.LOGIC_CFG,
    #          model_cfg_file=settings.MODEL_CFG, cache_cfg_file=settings.CACHE_CFG)


if __name__ == "__main__":
    settings_mod = get_settings_mod(sys.argv)
    try:
        exec 'import %s as settings' % settings_mod
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_mod)

    except ImportError,e:
        print e
        sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
        sys.exit(1)
    # init_app(settings)
    execute_from_command_line(sys.argv)
