#-*- coding: utf-8 -*-
import os
import sys

cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(cur_dir, ".."))

file_list = ['import_test', 'manage', 'production', 'staging', 'development', 'test']

def run_dir(py_dir):
    for root, dirs, files in os.walk(py_dir):
        if root.find('.svn')==-1:
            for f in files:
                name, ext = os.path.splitext(f)
                if ext == '.py' and name not in file_list:
                    root = root.replace(py_dir, '').replace('/', '.').replace('\\', '.')
                    print root, name
                    if root:
                        __import__(root, globals(), locals(), [name], -1)
                    else:
                        __import__(name, globals(), locals(), [], -1)

if __name__ == '__main__':
    settings_mapping = {
        'prd': 'apps.settings.production',
        'stg': 'apps.settings.staging',
        'dev': 'apps.settings.development',
        'test': 'apps.settings.test',
        
        'apps.settings.production': 'apps.settings.production',
        'apps.settings.staging': 'apps.settings.staging',
        'apps.settings.development': 'apps.settings.development',
        'apps.settings.test': 'apps.settings.test',
    }
    try:
        subcommand = sys.argv[1]
    except Exception:
        sys.stderr.write("Usage: python apps/import_test.py apps.settings.development|apps.settings.staging|apps.settings.production|apps.settings.test\n")
        sys.exit(1)

    exec 'import %s as settings' % settings_mapping[subcommand]
    # from rklib.core import app
    # app.init(storage_cfg_file=settings.STORAGE_CFG, logic_cfg_file=settings.LOGIC_CFG,
    #          model_cfg_file=settings.MODEL_CFG, cache_cfg_file=settings.CACHE_CFG)
    #
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_mapping[subcommand])
    # run_dir(settings.BASE_ROOT+'/apps/')
