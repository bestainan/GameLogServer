# -*- coding:utf-8 -*-

"""
    后台定义
"""
#权限定义 (一个项目对应一个权限)
MANAGER_PERMISSION = [
    {
        "code": "Super",
        "description": u"超级管理权限"
    },
    {
        "code": "Program",
        "description": u"程序权限"
    },
    {
        "code": "Design",
        "description": u"策划权限"
    },
    {
        "code": "Operations",
        "description": u"运营权限"
    }
]

MANAGER_PERMISSION_EN_TO_CN ={
        "Super": u"超级管理权限",
        "Program": u"程序权限",
        "Design": u"策划权限",
        "Operations": u"运营权限",
}

# url 与权限映射
VIEW_PERMISSION = [
    {
        # 管理员帐号管理
        "path": r'^/Tyranitar6/super_man/',
        "permissions": ['Super']
    },
    {
        # 服务器列表编辑
        "path": r'^/Tyranitar6/server_lst/',
        "permissions": ['Super', 'Program']
    },
    {
        # 服务器列表编辑
        "path": r'^/Tyranitar6/server/server_config/',
        "permissions": ['Super', 'Program', 'Design']
    },
    {
        # 主页
        "path": r'^/Tyranitar6/main/',
        "permissions": ['All']
    },
    {
        # 修改密码
        "path": r'^/Tyranitar6/updata_password/',
        "permissions": ['All']
    },
    {
        # 修改密码
        "path": r'^/Tyranitar6/super_man/updata_password/',
        "permissions": ['All']
    },

    {
        # 日志部分查询
        "path": r'^/Tyranitar6/log/',
        "permissions": ['All']
    },
    {
        # GM游戏内数据查询部分
        "path": r'^/Tyranitar6/gm/',
        "permissions": ['All']
    },
    {
        # 游戏内数据编辑部分
        "path": r'^/Tyranitar6/data_edit/',
        "permissions": ['Program']
    },
    {
        # Ajax POST
        "path": r'^/Tyranitar6/post/',
        "permissions": ['All']
    },

]

# 权限和按键之间关系
VIEW_BUTTON = {
    "All": [
        'btn_game_logs', # 日志部分按键
        'btn_gm_function',  #  GM后台查询
    ],

    "Super": [
        'btn_super',
        'server_super' # 服务器信息管理

    ],

    "Program": [
        'server_super', # 服务器信息管理
        'btn_search',       # 数据后台按键

    ],
    "Design": [
        'server_super' # 服务器信息管理
    ],
    "Operations": [

    ],
}


# 管理后台安全校验码
ADMIN_SECRET_KEY = 's3avlj$=vk16op_s1g!xyilse9azcu&oh#wln8_@!b+_p7-+@='

MAIN_URL = '/Tyranitar6'


GM_ACTION_SUPER_REGISTER = 0
GM_ACTION_DELETE_MANAGER = 1
GM_ACTION_MANAGER_REGISTER = 2
GM_ACTION_MANAGER_LOGIN = 3
GM_ACTION_UPDATE_PASSWORD = 4
GM_ACTION_UPDATE_MANAGER_INFO = 5
GM_ACTION_EDIT_PLAYER = 6
GM_ACTION_CREATE_MONSTER = 7
GM_ACTION_CHANGE_MONSTER = 8
GM_ACTION_DELETE_MONSTER = 9
GM_ACTION_ADD_ITEM = 10
GM_ACTION_CHANGE_ITEM = 11
GM_ACTION_DELETE_ITEM = 12
GM_ACTION_ADD_EQUIP = 13
GM_ACTION_CHANGE_EQUIP = 14
GM_ACTION_DELETE_EQUIP = 15
GM_ACTION_INSERT_SERVER = 16
GM_ACTION_UPDATE_SERVER = 17
GM_ACTION_DELETE_SERVER = 18
GM_ACTION_INSERT_VERSION_NOTICE = 19
GM_ACTION_UPDATE_VERSION_NOTICE = 20
GM_ACTION_DELETE_VERSION_NOTICE = 21
GM_ACTION_INSERT_GIFT = 22
GM_ACTION_EDIT_GIFT = 23
GM_ACTION_UPDATE_NOTICE = 24
GM_ACTION_DELETE_NOTICE = 25
GM_ACTION_ADD_MAIL = 26
GM_ACTION_DELETE_MAIL = 27
GM_ACTION_ADD_BUG_MAIL = 28
GM_ACTION_DELETE_BUG = 29
GM_ACTION_DELETE_BUG_ALL = 30
GM_ACTION_CHANGE_ACTIVITY = 31
GM_ACTION_INSERT_EXCHANGE_CODE = 32
GM_ACTION_PUBLISH_CONFIG = 33
GM_ACTION_REMOVE_CONFIG = 34
GM_ACTION_CHANGE_SERVER_VERSION = 35
GM_ACTION_CHANGE_SERVER_CONFIG = 36

GM_LOG_ACTION_DICT = {
    GM_ACTION_SUPER_REGISTER: '0-超级管理员注册',
    GM_ACTION_DELETE_MANAGER: '1-删除管理员',
    GM_ACTION_MANAGER_REGISTER: '2-游戏管理员注册',
    GM_ACTION_MANAGER_LOGIN: '3-游戏管理员登录',
    GM_ACTION_UPDATE_PASSWORD: '4-修改管理员密码',
    GM_ACTION_UPDATE_MANAGER_INFO: '5-修改管理员信息',
    GM_ACTION_EDIT_PLAYER: '6-修改玩家信息',
    GM_ACTION_CREATE_MONSTER: '7-添加宠物',
    GM_ACTION_CHANGE_MONSTER: '8-修改宠物信息',
    GM_ACTION_DELETE_MONSTER: '9-删除宠物',
    GM_ACTION_ADD_ITEM: '10-添加物品',
    GM_ACTION_CHANGE_ITEM: '11-修改物品',
    GM_ACTION_DELETE_ITEM: '12-删除物品',
    GM_ACTION_ADD_EQUIP: '13-添加装备',
    GM_ACTION_CHANGE_EQUIP: '14-修改装备',
    GM_ACTION_DELETE_EQUIP: '15-删除装备',
    GM_ACTION_INSERT_SERVER: '16-添加服务器',
    GM_ACTION_UPDATE_SERVER: '17-更新服务器',
    GM_ACTION_DELETE_SERVER: '18-删除服务器',
    GM_ACTION_INSERT_VERSION_NOTICE: '19-添加版本公告',
    GM_ACTION_UPDATE_VERSION_NOTICE: '20-更新版本公告',
    GM_ACTION_DELETE_VERSION_NOTICE: '21-删除版本公告',
    GM_ACTION_INSERT_GIFT: '22-添加礼包',
    GM_ACTION_EDIT_GIFT: '23-编辑礼包',
    GM_ACTION_UPDATE_NOTICE: '24-编辑广播',
    GM_ACTION_DELETE_NOTICE: '25-删除广播',
    GM_ACTION_ADD_MAIL: '26-添加系统邮件',
    GM_ACTION_DELETE_MAIL: '27-删除系统邮件',
    GM_ACTION_ADD_BUG_MAIL: '28-添加回复bug邮件',
    GM_ACTION_DELETE_BUG: '29-删除玩家提的bug',
    GM_ACTION_DELETE_BUG_ALL: '30-清空所有bug',
    GM_ACTION_CHANGE_ACTIVITY: '31-编辑运营活动',
    GM_ACTION_INSERT_EXCHANGE_CODE: '32-插入兑换码',
    GM_ACTION_PUBLISH_CONFIG: '33-上传配置文件',
    GM_ACTION_REMOVE_CONFIG: '34-删除配置文件',
    GM_ACTION_CHANGE_SERVER_VERSION: '35-修改服务器版本信息',
    GM_ACTION_CHANGE_SERVER_CONFIG: '36-修改游戏配置信息',
}

GM_LOG_ACTION_NAME_DICT = {
    GM_ACTION_SUPER_REGISTER: 'gm_action_super_register',
    GM_ACTION_DELETE_MANAGER: 'gm_action_delete_manager',
    GM_ACTION_MANAGER_REGISTER: 'gm_action_manager_register',
    GM_ACTION_MANAGER_LOGIN: 'gm_action_manager_login',
    GM_ACTION_UPDATE_PASSWORD: 'gm_action_update_password',
    GM_ACTION_UPDATE_MANAGER_INFO: 'gm_action_update_manager_info',
    GM_ACTION_EDIT_PLAYER: 'gm_action_edit_player',
    GM_ACTION_CREATE_MONSTER: 'gm_action_create_monster',
    GM_ACTION_CHANGE_MONSTER: 'gm_action_change_monster',
    GM_ACTION_DELETE_MONSTER: 'gm_action_delete_monster',
    GM_ACTION_ADD_ITEM: 'gm_action_add_item',
    GM_ACTION_CHANGE_ITEM: 'gm_action_change_item',
    GM_ACTION_DELETE_ITEM: 'gm_action_delete_item',
    GM_ACTION_ADD_EQUIP: 'gm_action_add_equip',
    GM_ACTION_CHANGE_EQUIP: 'gm_action_change_equip',
    GM_ACTION_DELETE_EQUIP: 'gm_action_delete_equip',
    GM_ACTION_INSERT_SERVER: 'gm_action_insert_server',
    GM_ACTION_UPDATE_SERVER: 'gm_action_update_server',
    GM_ACTION_DELETE_SERVER: 'gm_action_delete_server',
    GM_ACTION_INSERT_VERSION_NOTICE: 'gm_action_insert_version_notice',
    GM_ACTION_UPDATE_VERSION_NOTICE: 'gm_action_update_version_notice',
    GM_ACTION_DELETE_VERSION_NOTICE: 'gm_action_delete_version_notice',
    GM_ACTION_INSERT_GIFT: 'gm_action_insert_gift',
    GM_ACTION_EDIT_GIFT: 'gm_action_edit_gift',
    GM_ACTION_UPDATE_NOTICE: 'gm_action_update_notice',
    GM_ACTION_DELETE_NOTICE: 'gm_action_delete_notice',
    GM_ACTION_ADD_MAIL: 'gm_action_add_mail',
    GM_ACTION_DELETE_MAIL: 'gm_action_delete_mail',
    GM_ACTION_ADD_BUG_MAIL: 'gm_action_add_bug_mail',
    GM_ACTION_DELETE_BUG: 'gm_action_delete_bug',
    GM_ACTION_DELETE_BUG_ALL: 'gm_action_delete_bug_all',
    GM_ACTION_CHANGE_ACTIVITY: 'gm_action_change_activity',
    GM_ACTION_INSERT_EXCHANGE_CODE: 'gm_action_insert_exchange_code',
    GM_ACTION_PUBLISH_CONFIG: 'gm_action_publish_config',
    GM_ACTION_REMOVE_CONFIG: 'gm_action_remove_config',
    GM_ACTION_CHANGE_SERVER_VERSION: 'gm_action_change_server_version',
    GM_ACTION_CHANGE_SERVER_CONFIG: 'gm_action_change_server_config',
}

GM_ACTION_VALUE = {
    'log_time': u'时间',
    'uid': u'管理员序号',
    'account': u'账户名',
    'name': u'名字',
    'description': u'描述',
    'permission': u'权限',
    'last_login_ip': u'上次登录IP',
    'last_login_time': u'上次登录时间',
    'action': u'事件',
    'del_gm': u'被删除管理员序号',
    'new_account': u'新账户名',
    'new_name': u'新名字',
    'new_permission': u'新权限',
    'new_description': u'新描述',
    'server_id': u'服务器序号',
    'user_id': u'用户ID',
    'mon_uid': u'宠物UID',
    'mon_tid': u'宠物TID',
    'star_level': u'星级',
    'level': u'等级',
    'key': u'属性',
    'old': u'修改前',
    'new': u'修改后',
}

GM_ACTION_CHANGE_KEY = {
    'evo_sun_stone': '所吃进化石数量',
    'evo_level': '怪进化阶',
    'evo_fail_count': '怪进化一阶失败次数',
    'starLevel': '星级',
    'star_level_exp': '星级经验',
    'level': '等级',
    'maxLevel': '等级上限',
    'sex': '性别',
    'exp': '经验值',
    'effort': '努力值',
    'personality': '性格',
    'individual': '个体值',
    'skillsLevel': '技能等级',
    'skillsExp': '技能经验',
}

