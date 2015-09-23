# -*- coding:utf-8 -*-

"""
    所有游戏服务器的配置管理
"""
import os
import hashlib
import httplib
import urllib
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from apps.game_manager.util import memcache
from django.template import RequestContext
from apps.utils import server_define
from apps.utils import model_define
from apps.game_manager.models.game_manager import *
from apps.logs.output_action_gm import *


def view(request, select_server_id=10001):
    """
        查看配置
    """
    head_lst = [
        {'width': 300, 'name': u'配置文件'},
        {'width': 700, 'name': u'版本号'}
    ]
    server_name_lst = server_define.SERVER_NAME_LST
    # 本地获取所有配置文件
    local_config_lst = _get_all_config_dat()
    # 获取所有服务器的配置信息
    config_compare_lst =[]
    for _server_id, _cmem_url in server_define.CMEM_MAP.items():
        cmem_state,need_update_config_dict, config_time, version = get_need_update_config_dict(_cmem_url, local_config_lst)
        server_compare_result = dict()
        server_compare_result['id'] = _server_id
        server_compare_result['update_files'] = need_update_config_dict
        server_compare_result['cmem'] = cmem_state
        server_compare_result['time'] = config_time
        server_compare_result['version'] = version
        config_compare_lst.append(server_compare_result)
    return render_to_response("server/config/view.html", locals(), RequestContext(request))

def publish(request):
    """
        发布游戏配置
    """
    head_lst = [
        {'width': 300, 'name': u'配置文件'},
        {'width': 700, 'name': u'版本号'},
        {'width': 100, 'name': u'操作'},
    ]
    if request.method == 'GET':

        # 获取所有配置文件
        config_lst = _get_all_config_dat()

        return render_to_response("server/config/publish.html", locals(), RequestContext(request))
    else:
        upload_file = request.FILES.get('upload_file', None)
        upload_file_name = upload_file.name
        status = 0
        is_zip = upload_file_name.endswith('.zip')
        is_py = upload_file_name.endswith('.py')
        if not upload_file or (not is_py and not is_zip):
            status = 1

        # 保存文件
        file_name = '/tmp/%s' % upload_file_name
        if os.path.exists(file_name):
            os.remove(file_name)
        new_file = open(file_name, 'wb')
        for chunk in upload_file.chunks():
            new_file.write(chunk)
        new_file.close()

        # 如果是PY文件就直接替换掉
        if is_py:
            #覆盖同名文件
            result = os.system('cp /tmp/%s /opt/GameServerConfig/%s'% (upload_file_name, upload_file_name))
            # print(" cmd " + str('cp /tmp/%s /opt/GameServerConfig/%s'% (upload_file_name, upload_file_name)))
            if result:
                status = 2
        elif is_zip:
            # 解压缩
            # 判断目录是否存在
            unzip_path = '/tmp/game_config_unzip/'
            if os.path.exists(unzip_path):
                result = os.system('rm -rf %s' % unzip_path)
            result = os.system('mkdir %s' % unzip_path)
            result = os.system('unzip -d %s /tmp/%s' % (unzip_path, upload_file_name))
            result = os.system('cp %s/* /opt/GameServerConfig/' % unzip_path)

        config_lst = _get_all_config_dat()

        # 操作日志记录
        manager = GameManager.get_by_request(request)
        insert_action_publish_config(manager, file_name)

        return render_to_response("server/config/publish.html", locals(), RequestContext(request))


def change_server_version(request):
    """
        修改服务器版本信息
    """
    # 本地获取所有配置文件
    local_config_lst = _get_all_config_dat()
    if request.method == 'POST':
        server_id = int(request.POST.get('server_id2'))
        new_version = request.POST.get('new_version')
        cmem_url = server_define.CMEM_MAP[server_id]
        config_result = memcache.get_cmem_val(cmem_url, model_define.CONFIG_MODEL)
        # config_version_dict = config_result.get('config_version_dict', None)
        # config_time = config_result.get('game_config_publish_time', 0)
        # version = config_result.get('version', 0)
        old_version = config_result['version']
        config_result['version'] = new_version
        memcache.put_cmem_val(cmem_url,model_define.CONFIG_MODEL, config_result)

        # 操作日志记录
        manager = GameManager.get_by_request(request)
        insert_action_change_server_version(manager, server_id, old_version, new_version)

    # return HttpResponseRedirect("/Tyranitar6/server/server_config/view/")
        return view(request, server_id)


def change_server_config(request):
    """
        修改游戏配置信息
    """
    # 本地获取所有配置文件
    local_config_lst = _get_all_config_dat()
    if request.method == 'POST':
        server_id = int(request.POST.get('server_id'))
        cmem_state,need_update_config_dict, config_time, version = get_need_update_config_dict(server_define.CMEM_MAP[server_id], local_config_lst)
        # 获取对应服务器URL
        from apps.game_manager.mysql.server_list import get_server
        server_dat = get_server(server_id)
        server_url_full = server_dat['url']
        server_url = server_url_full[server_url_full.index(':') + 3 : server_url_full.rindex(':')]
        for _key in need_update_config_dict.keys():
            http_status, http_data = _send_to_game_server_to_update_file(server_url, _key)
            if http_data != 'TRUE':
                # 更新文件发生错误
                print("更新文件发生错误 " + str(_key))
        # 更新服务器的配置时间戳
        http_status, http_data = _send_to_game_server_to_update_config_time(server_url)
        if http_data != 'TRUE':
                # 更新文件发生错误
                print("更新配置时间戳错误 ")

        # 操作日志记录
        manager = GameManager.get_by_request(request)
        insert_action_change_server_config(manager, need_update_config_dict)

        return view(request, server_id)
        # return HttpResponseRedirect("/Tyranitar6/server/server_config/view/")


def remove_local_config(request):
    if request.method == 'POST':
        config_name = request.POST.get('config_name')
        result = os.system('rm /opt/GameServerConfig/%s' % config_name)
        print result

        # 操作日志记录
        manager = GameManager.get_by_request(request)
        insert_action_remove_config(manager, config_name)

        return HttpResponseRedirect("/Tyranitar6/server/server_config/publish/")

def get_need_update_config_dict(cmem_url, local_config_lst):
    """
        获取需要更新的配置文件信息
    """
    need_update_config_dict = dict()
    config_time = 0
    version = 0
    cmem_state = True
    if cmem_url:
        config_result = memcache.get_cmem_val(cmem_url, model_define.CONFIG_MODEL)
        config_version_dict = config_result.get('config_version_dict', None)
        config_time = config_result.get('game_config_publish_time', 0)
        version = config_result.get('version', 0)
        # 有配置版本信息
        if config_version_dict:
            for _dat in local_config_lst:
                _file_name = _dat['name']
                if _file_name in config_version_dict:
                    game_server_config_version = config_version_dict[_file_name]
                    local_config_version = _dat['version']
                    if game_server_config_version != local_config_version:
                        # print("game_server_config_version " + str(game_server_config_version))
                        # print("local_config_version " + str(local_config_version))
                        need_update_config_dict[_file_name] = game_server_config_version
                    else:
                        pass
                else:
                    need_update_config_dict[_file_name] = u'无版本信息'
        else:
            # 没有配置版本信息代表没发布配置
            # 所有的文件都是需要更新的
            for _dat in local_config_lst:
                _file_name = _dat['name']
                need_update_config_dict[_file_name] = u'无版本信息'
    else:
        cmem_state = False
    return cmem_state, need_update_config_dict, config_time, version

def _send_to_game_server_to_update_file(server_url, config_name):
    """
        下载后台服务器上的配置表到本地
    """
    print("游戏服务器开始更新配置文件： %s " % config_name)
    try:
        game_manager_conn = httplib.HTTPConnection(server_url, 8083)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = urllib.urlencode({'name': config_name})
        game_manager_conn.request('POST', '/game_config/update_config_file', data, headers=headers)
        http_res = game_manager_conn.getresponse()
        status = http_res.status
        data = http_res.read()
    except:
        print("更新错误!")
    finally:
        if game_manager_conn:
            game_manager_conn.close()
    return status, data


def _send_to_game_server_to_update_config_time(server_url):
    """
        下载后台服务器上的配置表到本地
    """
    print("游戏服务器开始更新配置时间戳")
    try:
        game_manager_conn = httplib.HTTPConnection(server_url, 8083)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        game_manager_conn.request('POST', '/game_config/update_config_time', headers=headers)
        http_res = game_manager_conn.getresponse()
        status = http_res.status
        data = http_res.read()
    except:
        print("更新错误!")
    finally:
        if game_manager_conn:
            game_manager_conn.close()
    return status, data


def _get_all_config_dat():
    """
        获取当前 保存的所有配置
    """
    # 获取所有配置文件
    config_path = '/opt/GameServerConfig/'
    config_file_lst = os.listdir(config_path)
    config_lst = []
    for _file in config_file_lst:
        if not _file.startswith('.'):
            _file_path = config_path + _file
            _file_ok, _file_version = _get_file_version(_file_path)
            # 文件加载成功
            if _file_ok:
                dat = dict()
                dat['name'] = _file
                dat['version'] = _file_version
                config_lst.append(dat)
    return config_lst



def _get_file_version(str_path):
    file = None
    b_result = False
    str_md5 = ""
    str_version = ""

    try:
        file = open(str_path, "rb")
        _file_time = int(os.path.getmtime(str_path))
        str_read = file.read()
        md5 = hashlib.md5(str_read)
        b_result = True
        str_md5 = md5.hexdigest()
        str_version = str_md5
    except:
        b_result = False
    finally:
        if file:
            file.close()

    return b_result, str_version
