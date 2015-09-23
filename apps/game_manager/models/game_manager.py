# -*- coding: utf-8 -*-

"""
    游戏管理员数据
"""
import time
import re
import urllib
import hashlib
from apps.game_manager import game_manage_define
from django.shortcuts import render_to_response

ADMIN_SECRET_KEY = 's3avlj$=vk16op_s1g!xyilse9azcu&oh#wln8_@!b+_p7-+@='

class GameManager(object):
    def __init__(self):
        super(GameManager, self).__init__()
        self.uid = 0  # 管理员标志
        self.account = ''  # 管理员账号
        self.password = ''  # 管理员密码
        self.name = ''  # 邮件
        self.last_login_ip = "0.0.0.0"
        self.last_login_time = ''
        self.permissions = ''  # 管理员可用权限
        self.description = ''  # 描述

    def is_has_permission(self, view_path):
        """
            拥有权限
        """
        pass

    def is_allow(self, url):
        """
            是否可以访问
        """
        for _url_dat in game_manage_define.VIEW_PERMISSION:
            url_pattern = re.compile(_url_dat['path'])
            if url_pattern.match(url):
                permissions = _url_dat['permissions']
                if self.permissions in permissions or 'All' in permissions:
                    return True
        return False

    def check_password(self, pass_word):
        """
            检查密码匹配
        """
        return hashlib.md5(pass_word).hexdigest() == self.password


    def check_admin_permission(self):
        """
            检测权限
        """
        btn_lst = game_manage_define.VIEW_BUTTON[self.permissions]
        btn_lst.extend(game_manage_define.VIEW_BUTTON['All'])
        return btn_lst

    def login(self, login_time, login_ip, response):
        """
            登录
        """
        self.last_login_ip = login_ip
        self.last_login_time = login_time

        from apps.game_manager.mysql import mysql_game_manager
        mysql_game_manager.update_game_manager_login_dat(self.uid, self.last_login_ip, self.last_login_time)

        last_login_stamp = time.mktime(self.last_login_time.timetuple())
        token = self.build_rkauth_signature({
            "mid": self.uid,
            "last_login": last_login_stamp,
            "secret_key": ADMIN_SECRET_KEY
        })
        cv = "%s|%s|%s" % (self.uid, last_login_stamp, token)
        cv = urllib.quote(cv.encode("ascii"))
        response.set_cookie("moderator",cv)
        return response

    @classmethod
    def create(cls, user_name, password, email, permissions):
        """
            创建
        """
        _game_manager = cls(user_name, password, email, permissions)
        return _game_manager

    @classmethod
    def get_by_request(cls, request):
        """
            获取对应管理
        """
        cv = request.COOKIES.get("moderator")
        if cv is None:
            return None
        else:
            cv = urllib.unquote(cv).decode("ascii")
            mid,login_stamp,token = cv.split('|')
            print mid,login_stamp,token
            from apps.game_manager.mysql import mysql_game_manager
            game_manager = mysql_game_manager.get_game_manager_with_id(mid)
            if game_manager is None:
                return None

            raw_last_login_stamp = time.mktime(game_manager.last_login_time.timetuple())
            new_token = cls.build_rkauth_signature({
                "mid":mid,
                "last_login": raw_last_login_stamp,
                "secret_key":ADMIN_SECRET_KEY
            })

            if new_token == token:
                return game_manager
            return None

    @classmethod
    def build_rkauth_signature(cls, auth_fields):
        """生成rkauth签名"""
        payload = "&".join(k + "=" + str(auth_fields[k]) for k in sorted(auth_fields.keys()) if k != "auth_token")
        return hashlib.md5(payload).hexdigest()






