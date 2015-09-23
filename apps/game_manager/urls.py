#-*- coding: utf-8 -*-

from django.conf.urls import *


urlpatterns = patterns('game_manager.views.main',
                       (r'^$', 'index'),
                       (r'^login/$', 'login'),
                       (r'^register/$', 'register'),
                       (r'^main/$', 'main'),
                       (r'^updata_password/$', 'view_index'),
                       (r'^super_man/updata_password/$', 'updata_admin_password'),
                       (r'^post/data/$', 'accept_post'),
)

#超级管理员 查询功能
urlpatterns += patterns('game_manager.views.super_manage.super_manage_views',
                        (r'^super_man/select_account/$', 'select_account'),
                        (r'^super_man/register_user/$', 'register_user'),
                        (r'^super_man/add_admin/$', 'add_admin'),
                        (r'^super_man/delete_user/$', 'delete_user'),
                        (r'^super_man/update_user/$', 'update_user'),
                        (r'^super_man/update_data/$', 'update_data'),
)

#数据后台
urlpatterns += patterns('game_manager.views.data_edit',
                        #用户管理
                        url(r'^data_edit/user_info_edit/$', 'user_info_edit.index',
                            {'template': r'data_edit/user_info_edit.html',}),

                        url(r'^data_edit/set_user_memcache/$', 'user_info_edit.set_user_memcache',
                            {'template': r'data_edit/user_info_edit.html',}),

                        #物品数据
                        url(r'^data_edit/items_info/$','items_info.index',
                            {'template':r'data_edit/items_info.html'}),

                        url(r'^data_edit/set_items_info/$','items_info.set_items_info',
                            {'template':r'data_edit/items_info.html'}),

                        # 30天签到
                        url(r'^data_edit/sign_30_model/$','sign_30_model.index',
                            {'template':r'data_edit/sign_30_model.html'}),

                        # 7天登录
                        url(r'^data_edit/login_7_model/$','login_7_model.index',
                            {'template':r'data_edit/login_7_model.html'}),

                        # 玩家宝物
                        url(r'^data_edit/treasure_item_model/$','treasure_item_model.index',
                            {'template':r'data_edit/treasure_item_model.html'}),

                        # 玩家私信
                        url(r'^data_edit/private_mail_model/$','private_mail_model.index',
                            {'template':r'data_edit/private_mail_model.html'}),

                        # 玩家联盟商店
                        url(r'^data_edit/union_shop_model/$','union_shop_model.index',
                            {'template':r'data_edit/union_shop_model.html'}),
)



urlpatterns += patterns('game_manager.views.log.daily_log',
                        # 每日概况
                        (r'^log/statistics_total/$', 'statistics_total'),
                        (r'^log/online_time/$', 'online_time'),
                        (r'^log/amount_analyse/$', 'amount_analyse'),
                        (r'^log/online_time_user_num/$', 'online_time_user_num'),
                        (r'^log/user_retain/$', 'user_retain'),


                        # 付费分析
                        (r'^log/payment_point_analyse/$', 'payment_point_analyse'),
                        (r'^log/payment_level_analyse/$', 'payment_level_analyse'),
                        (r'^log/player_first_recharge_level/$', 'player_first_recharge_level'),
                        (r'^log/recharge_cycle/$', 'recharge_cycle'),
                        (r'^log/new_k_days_income/$', 'new_k_days_income'),
                        (r'^log/user_life_time_value/$', 'user_life_time_value'),


                        # 用户统计
                        (r'^log/vip_distributed/$', 'vip_distributed'),
                        (r'^log/user_first_recharge/$', 'user_first_recharge'),
                        (r'^log/user_recharge_state/$', 'user_recharge_state'),

                        # 流失分析
                        (r'^log/newbie_state/$', 'newbie_state'),
                        (r'^log/guide_state/$', 'guide_state'),
                        (r'^log/user_level_lost_state/$', 'user_level_lost_state'),
                        (r'^log/user_level_state/$', 'user_level_state'),
                        (r'^log/user_structure/$', 'user_structure'),
                        (r'^log/user_life_cycle/$', 'user_life_cycle'),


                        # 首日体验
                        (r'^log/user_first_play_level/$', 'user_first_play_level'),
                        (r'^log/first_play_time/$', 'first_play_time'),

                        # 消费点分析
                        (r'^log/user_first_cost_stone/$', 'user_first_cost_stone'),
                        (r'^log/user_first_cost_gold/$', 'user_first_cost_gold'),
                        (r'^log/daily_consume_distributed_stone/$', 'daily_consume_distributed_stone'),
                        (r'^log/daily_consume_distributed_gold/$', 'daily_consume_distributed_gold'),
                        (r'^log/user_level_consume_stone_state/$', 'user_level_consume_stone_state'),
                        (r'^log/user_level_consume_gold_state/$', 'user_level_consume_gold_state'),

                        (r'^log/user_stone_shop/$', 'user_stone_shop'),

                        # 数值平衡
                        (r'^log/user_generate_gold/$', 'user_generate_gold'),  #金币产出
                        (r'^log/user_generate_stone/$', 'user_generate_stone'),  #钻石产出
                        (r'^log/user_cost_gold/$', 'user_cost_gold'),
                        (r'^log/user_cost_stone/$', 'user_cost_stone'),
                        (r'^log/user_hold_gold/$', 'user_hold_gold'),
                        (r'^log/user_hold_stone/$', 'user_hold_stone'),
                        (r'^log/user_cost_gold_with_vip/$', 'user_cost_gold_with_vip'),
                        (r'^log/user_cost_stone_with_vip/$', 'user_cost_stone_with_vip'),

                        # 活动模块分析
                        (r'^log/fishing/$', 'fishing'),
                        (r'^log/finger_guess/$', 'finger_guess'),
                        (r'^log/question/$', 'question'),
                        (r'^log/tonic/$', 'tonic'),
                        (r'^log/massage/$', 'massage'),

                        # 宠物相关统计
                        (r'^log/create_monster/$', 'create_monster'),
                        (r'^log/remove_monster/$', 'remove_monster'),
                        (r'^log/monster_reset_individual/$', 'monster_reset_individual'),

                        # 装备相关统计
                        (r'^log/create_equipment/$', 'create_equipment'),
                        (r'^log/consume_equipment/$', 'consume_equipment'),

                        # 物品相关统计
                        (r'^log/create_item/$', 'create_item'),
                        (r'^log/consume_item/$', 'consume_item'),
                        (r'^log/cost_stamina/$', 'cost_stamina'),

                        # 副本进度
                        (r'^log/stage_normal/$', 'stage_normal'),
                        (r'^log/stage_hard/$', 'stage_hard'),
                        (r'^log/stage_exp/$', 'stage_exp'),
                        (r'^log/stage_gold/$', 'stage_gold'),
                        (r'^log/stage_trial/$', 'stage_trial'),
                        (r'^log/stage_gym/$', 'stage_gym'),
                        (r'^log/stage_world_boss/$', 'stage_world_boss'),
                        (r'^log/stage_catch_monster/$', 'stage_catch_monster'),
                        (r'^log/stage_treasure_battle/$', 'stage_treasure_battle'),
)

#联盟
urlpatterns += patterns('game_manager.views.log.union_count',
                        (r'^log/union_count/$', 'union_count_function'),  # 联盟信息
                        (r'^log/union_sign/$', 'union_sign_function'),  #联盟签到
                        (r'^log/union_shop/$', 'union_shop_function'),  #联盟商店
                        (r'^log/union_stage/$', 'union_stage_function'),  #联盟副本
                        (r'^log/union_buy_reward/$', 'union_buy_reward_function'),  #联盟奖励
                        (r'^log/union_hall/$', 'union_hall_function'),
)

# 好友
urlpatterns += patterns('game_manager.views.log.friend_count',
                        (r'^log/friend_count/$', 'friend_count_function'),
)

#豪华签到
urlpatterns += patterns('game_manager.views.log.luxury_sign_daily_log',
                        (r'^log/sign_count/$', 'sign_count_function'),  #2是luxury_sign_daily_log下的函数
                        (r'^log/sign_create/$', 'sign_create_function'),
)

#特殊活动
urlpatterns += patterns('game_manager.views.log.activity',
                        #七天冲级
                        url(r'^log/seven_days_lv/$', 'activity_view',
                            {'template': r'log/seven_days_lv_view.html',
                             'dir_name': 'tables',
                             'file_name': 'SEVEN_DAYS_LV'}),
                        #七天战斗
                        url(r'^log/seven_days_fight/$', 'activity_view',
                            {'template': r'log/seven_days_fight_view.html',
                             'dir_name': 'tables',
                             'file_name': 'SEVENT_DAY_FIGHT'}),
                        #满额福利
                        url(r'^log/max_will/$', 'activity_view',
                            {'template': r'log/max_will_view.html',
                             'dir_name': 'tables',
                             'file_name': 'MAX_WILL'}),

                        #消费有礼物
                        url(r'^log/give_me_give_you/$', 'activity_view',
                            {'template': r'log/give_me_give_you_view.html',
                             'dir_name': 'tables',
                             'file_name': 'GIVE_ME_GIVE_YOU'}),
                        #友好商店
                        url(r'^log/friendly_shop/$', 'activity_view',
                            {'template': r'log/friendly_shop.html', 'file_name': 'FRIENDLY_SHOP',
                             'dir_name': 'tables',
                             'file_name': 'FRIENDLY_SHOP'}),
                        #微信分享
                        url(r'^log/wei_chat/$', 'activity_view',
                            {'template': r'log/wei_chat_share.html',
                             'dir_name': 'tables',
                             'file_name': 'WEI_CHAT_SHARE'}),
)

# 排行榜查询
urlpatterns += patterns('game_manager.views.gm.ranking_list',
                        (r'^gm/sort_rmb/$', 'sort_rmb_view', {'dir_name': 'tables', 'file_name': 'SORT_RMB'}),  # 充值排行榜
                        (r'^gm/expense_sort/$', 'expense_sort_view',
                         {'dir_name': 'tables', 'file_name': 'EXPENSE_SORT'}),  # 消费排行榜
                        (r'^gm/level_rank_list/$', 'level_rank_list'),  # 等级排行榜
)

#充值管理
urlpatterns += patterns('game_manager.views.gm.recharge_manage',
                        (r'^gm/recharge_search/$', 'recharge_search'),  # 充值查询
                        (r'^gm/cost_search/$', 'cost_search'),  # 消费查询
)

#玩家行为查询
urlpatterns += patterns('game_manager.views.gm.player_behavior',
                        (r'^gm/stage_player_behavior/$', 'stage_player_behavior', {'dir_name': 'UID_ACTION_PATH'}),
)

#数据查询
urlpatterns += patterns('game_manager.views.gm.user_data_search',
                        (r'^gm/user_cost/$', 'user_cost'),  # 消费查询
                        (r'^gm/user_get/$', 'user_get'),  # 获得查询
                        (r'^gm/equipment_strengthening_record/$', 'equipment_strengthening_record'),  # 装备强化记录
)

#聊天管理
urlpatterns += patterns('game_manager.views.gm.get_chat_content',
                        (r'^gm/get_chat_content/$', 'get_chat_content'),
                        (r'^gm/get_union_chat_content/$' , 'get_union_chat_content'),
                        (r'^gm/body_forbiden/$','body_forbiden'),

)

#服务器信息管理
urlpatterns += patterns('game_manager.views.server.server_lst',
                        (r'^server/server_lst/$', 'server_lst'),
                        (r'^server/server_add/$', 'server_add'),
                        (r'^server/server_update/$', 'server_update'),
                        (r'^server/server_del_confirm/$', 'server_del_confirm'),
                        (r'^server/server_del/$', 'server_del'),
                        (r'^server/server_edit/$', 'server_edit'),
)

#服务器版本公告
urlpatterns += patterns('game_manager.views.server.version_notice',
                        (r'^server/version_notice_lst/$', 'version_notice_lst'),
                        (r'^server/version_notice_add/$', 'version_notice_add'),
                        (r'^server/version_notice_update/$', 'version_notice_update'),
                        (r'^server/version_notice_del_confirm/$', 'version_notice_del_confirm'),
                        (r'^server/version_notice_del/$', 'version_notice_del'),
                        (r'^server/version_notice_edit/$', 'version_notice_edit'),

)

#服务器活动
urlpatterns += patterns('game_manager.views.server.activity',
                        (r'^server/activity_lst/$', 'activity_lst'),
                        (r'^server/activity_add/$', 'activity_add'),
                        (r'^server/activity_update/$', 'activity_update'),
                        (r'^server/activity_del_confirm/$', 'activity_del_confirm'),
                        (r'^server/activity_del/$', 'activity_del'),
                        (r'^server/activity_edit/$', 'activity_edit'),

)

#服务器礼包package
urlpatterns += patterns('game_manager.views.server.gift_package',
                        (r'^server/gift_package_lst/$', 'gift_package_lst'),
                        (r'^server/gift_package_add/$', 'gift_package_add'),
                        (r'^server/gift_package_update/$', 'gift_package_update'),
                        (r'^server/gift_package_del_confirm/$', 'gift_package_del_confirm'),
                        (r'^server/gift_package_del/$', 'gift_package_del'),
                        (r'^server/gift_package_edit/$', 'gift_package_edit'),

)

#服务器兑换码
urlpatterns += patterns('game_manager.views.server.exchange_code',
                        (r'^server/exchange_code_info/$', 'exchange_code_info'),
                        (r'^server/exchange_code_generate/$', 'exchange_code_generate'),
                        (r'^server/exchange_code_output_csv/$', 'exchange_code_output_csv'),
                      )

#服务器系统广播
urlpatterns += patterns('game_manager.views.server.notice',
                        (r'^server/notice_lst/$', 'notice_lst'),
                        (r'^server/notice_add/$', 'notice_add'),
                        (r'^server/notice_update/$', 'notice_update'),
                        (r'^server/notice_del_confirm/$', 'notice_del_confirm'),
                        (r'^server/notice_del/$', 'notice_del'),

)

#服务器系统邮件
urlpatterns += patterns('game_manager.views.server.system_mail',
                        (r'^server/system_mail_lst/$', 'system_mail_lst'),
                        (r'^server/system_mail_add/$', 'system_mail_add'),
                        (r'^server/system_mail_update/$', 'system_mail_update'),
                        (r'^server/system_mail_del_confirm/$', 'system_mail_del_confirm'),
                        (r'^server/system_mail_del/$', 'system_mail_del'),

)

#服务器游戏BUG管理
urlpatterns += patterns('game_manager.views.server.player_commit_bugs',
                        (r'^server/player_commit_bugs_lst/$', 'player_commit_bugs_lst'),
                        (r'^server/system_mail_update/$', 'system_mail_update'),
                        (r'^server/player_commit_bugs_del_confirm/$', 'player_commit_bugs_del_confirm'),
                        (r'^server/player_commit_bugs_del/$', 'player_commit_bugs_del'),
                        (r'^server/player_commit_bugs_del_all_confirm/$', 'player_commit_bugs_del_all_confirm'),
                        (r'^server/player_commit_bugs_del_all/$', 'player_commit_bugs_del_all'),
                        (r'^server/player_commit_bugs_mail/$', 'player_commit_bugs_mail'),
                        (r'^server/player_commit_bugs_mail_update/$', 'player_commit_bugs_mail_update'),

)

#账号管理
urlpatterns += patterns('game_manager.views.gm.account_manager',
                        (r'^gm/account_release_forbiden/$','acount_release_forbiden'),
                        )

#游戏配置管理
urlpatterns += patterns('game_manager.views.server.server_config',
                        (r'^server/server_config/view/$', 'view'),
                        (r'^server/server_config/publish/$', 'publish'),
                        (r'^server/server_config/change_server_version/$', 'change_server_version'),
                        (r'^server/server_config/change_server_config/$', 'change_server_config'),
                        (r'^server/server_config/remove_local_config/$', 'remove_local_config'),

)

# 管理员操作查询
urlpatterns += patterns('game_manager.views.gm.manager_operation',
                        (r'^gm/manager_operation/$', 'get_manager_operation'),
)

# 宠物查询
urlpatterns += patterns('game_manager.views.data_edit.monster_info_edit',
                        (r'^data_edit/monster_info_edit/$', 'get_monster_lst'),
                        (r'^data_edit/add_monster/$', 'add_monster'),
                        (r'^data_edit/delete_monster_confirm/$', 'delete_monster_confirm'),
                        (r'^data_edit/delete_monster/$', 'delete_monster'),
)

# 角色信息修改
urlpatterns += patterns('game_manager.views.data_edit.player_info_edit',
                        (r'^data_edit/player_info_edit/$','get_player_info'),
                        (r'^data_edit/get_player_data/$','get_player_data'),
                        (r'^data_edit/set_player_data/$','set_player_data'),
                        )

#mail信息
urlpatterns += patterns('game_manager.views.data_edit.mail_info_edit',
                        (r'^data_edit/mail_info_edit/$','get_mail_info'),
                        )


#竞技场信息
urlpatterns += patterns('game_manager.views.data_edit.arena_info_edit',
                        (r'^data_edit/arena_report_info/$','get_arena_report_info'),
                        (r'^data_edit/arena_reward_times_info/$','get_arena_reward_times_info'),
                        )

urlpatterns += patterns('game_manager.views.data_edit',
                        #   玩家关卡管理 ok
                        url(r'^data_edit/player_stage_edit/$', 'player_stage_edit.get_stage_data_function',
                            {'player_stage_edit': r'data_edit/player_stage_edit.html'}),
                        #   每日VIP奖励 ok
                        url(r'^data_edit/everyday_vip_reward/$', 'everyday_vip_reward.get_everyday_vip_reward_function',
                            {'everyday_vip_reward': r'data_edit/everyday_vip_reward.html'}),
                        #   抓宠副本 ok
                        url(r'^data_edit/player_catch_monster/$', 'player_catch_monster.get_player_catch_monster_function',
                            {'player_catch_monster_edit': r'data_edit/player_catch_monster_edit.html'}),
                        #   玩家夺宝 ok 但没有宝石碎片配置表
                        url(r'^data_edit/player_treasure/$', 'player_treasure.get_player_treasure_function',
                            {'player_treasure_edit': r'data_edit/player_treasure_edit.html'}),
                        #   运营玩家普通副本活动 ok
                        url(r'^data_edit/activity_normal_stage/$', 'PlayerActivityNormalStage.get_player_activity_normal_stage_function',
                            {'player_activity_normal_stage': r'data_edit/player_activity_normal_stage.html'}),
                        #   运营玩家困难副本活动 ok
                        url(r'^data_edit/activity_hard_stage/$', 'PlayerActivityHardStage.get_player_activity_hard_stage_function',
                            {'player_activity_hard_stage': r'data_edit/player_activity_hard_stage.html'}),
                        #   运营玩家道馆活动 ok
                        url(r'^data_edit/player_activity_gym/$', 'player_activity_gym_py.get_player_activity_gym_function',
                            {'templates': r'data_edit/player_activity_gym_ht.html'}),
                        #   运营玩家夺宝活动 ok
                        url(r'^data_edit/player_activity_treasure/$', 'player_activity_treasure_py.get_player_activity_treasure_function',
                            {'templates': r'data_edit/player_activity_treasure_ht.html'}),
                        #   运营玩家钓鱼活动 ok
                        url(r'^data_edit/player_activity_fishing/$', 'player_activity_fishing_py.get_player_activity_fishing_function',
                            {'templates': r'data_edit/player_activity_fishing_ht.html'}),
                        #   玩家队伍    ok 但未显示名称，可移除队伍 装备 宠物 宝石
                        url(r'^data_edit/player_team/$', 'player_team.get_player_team_function',
                            {'templates': r'data_edit/player_team.html'}),
                        #   运营玩家猜拳活动 ok
                        url(r'^data_edit/player_activity_finger_guess/$', 'player_activity_finger_guess.get_player_activity_finger_guess_function',
                            {'templates': r'data_edit/player_activity_finger_guess.html'}),
                        #   运营活动短期限时充值 ok
                        url(r'^data_edit/player_activity_recharge_short/$', 'player_activity_recharge_short.get_player_activity_recharge_short_function',
                            {'templates': r'data_edit/player_activity_recharge_short.html'}),
                        #   运营活动长期限时充值 ok
                        url(r'^data_edit/player_activity_recharge_long/$', 'player_activity_recharge_long.get_player_activity_recharge_long_function',
                            {'templates': r'data_edit/player_activity_recharge_long.html'}),
                        #   运营活动单笔充值 ok 但用0 和 1 区分状态 可select
                        url(r'^data_edit/player_activity_one_charge/$', 'player_activity_one_charge.get_player_activity_one_charge_function',
                            {'templates': r'data_edit/player_activity_one_charge.html'}),
                        #   运营活动微信分享奖励 ok 发现数据里'complete'可完成列表没用
                        url(r'^data_edit/player_activity_weixin_share/$', 'player_activity_weixin_share.get_player_activity_weixin_share_function',
                            {'templates': r'data_edit/player_activity_weixin_share.html'}),
                        #   运营活动豪华充值奖励 ok
                        url(r'^data_edit/player_activity_regist_recharge/$', 'player_activity_regist_recharge.get_player_activity_regist_recharge_function',
                            {'templates': r'data_edit/player_activity_regist_recharge.html'}),
                        #   活动玩家消耗钻石次数 ok
                        url(r'^data_edit/player_activity_stone_consumption/$', 'player_activity_stone_consumption.get_player_activity_stone_consumption_function',
                            {'templates': r'data_edit/player_activity_stone_consumption.html'}),
                        #   玩家假日商店 ok
                        url(r'^data_edit/player_activity_holiday_shop/$', 'player_activity_holiday_shop.get_player_activity_holiday_shop_function',
                            {'templates': r'data_edit/player_activity_holiday_shop.html'}),
                        #   玩家便利商店 ok
                        url(r'^data_edit/player_activity_time_limited_shop/$', 'player_activity_time_limited_shop.get_player_activity_time_limited_shop_function',
                            {'templates': r'data_edit/player_activity_time_limited_shop.html'}),
                        #   玩家友好商店 ok
                        url(r'^data_edit/player_activity_time_limited_shift_shop/$', 'player_activity_time_limited_shift_shop.get_player_activity_time_limited_shift_shop_function',
                            {'templates': r'data_edit/player_activity_time_limited_shift_shop.html'}),
                        #   联盟关卡
                        url(r'^data_edit/union_stage/$', 'union_stage.get_union_stage_function',
                            {'templates': r'data_edit/union_stage.html'}),
)
# 后台部分数据编辑_Qing

#玩家区域查询
urlpatterns += patterns('game_manager.views.data_edit',
                        url(r'^data_edit/zone_info_edit/$', 'zone_info_edit.index',
                            {'zone_info_edit':r'data_edit/zone_info_edit.html'}),
                        url(r'^data_edit/set_zone_info_edit/$','zone_info_edit.set_zone_info_edit',
                            {'zone_info_edit':r'data_edit/zone_info_edit.html'}),
)

#玩家装备数据
urlpatterns += patterns('game_manager.views.data_edit',
                        # 显示 编辑 添加 删除
                        url(r'^data_edit/equip_info_edit/$', 'equip_info_edit.index',
                            {'equip_info_edit':r'data_edit/equip_info_edit.html'}),
                        # 选择界面
                        url(r'^data_edit/change_equip/$','equip_info_edit.change_equip_to_html',
                            {'equip_edit':r'data_edit/change_equip.html'}),
                        # 删除界面
                        url(r'^data_edit/delete_equip/$','equip_info_edit.delete_equip_to_html',
                            {'equip_del':r'data_edit/delete_equip.html'}),
                        # 添加界面
                        url(r'^data_edit/add_equip/$','equip_info_edit.add_equip_to_html',
                            {'equip_add':r'data_edit/change_equip.html'}),
                        )
# 图鉴信息
urlpatterns += patterns('game_manager.views.data_edit.handbook_info',
                        (r'^data_edit/handbook_info/$','get_handbook_info'),
                        )

# 试炼信息
urlpatterns += patterns('game_manager.views.data_edit.trial_info',
                        (r'^data_edit/trial_info/$','get_trial_info'),
                        )
#充值信息
urlpatterns += patterns('game_manager.views.data_edit.charge_info',
                        (r'^data_edit/daily_charge_reward_info/$','get_daily_charge_reward_info'),
                        (r'^data_edit/sum_charge_reward_info/$','get_sum_charge_reward_info'),
                        (r'^data_edit/player_charge_info/$','get_charge_info'),
                        )
# 玩家邀请信息
urlpatterns += patterns('game_manager.views.data_edit.player_invitation_info',
                        (r'^data_edit/player_invitation_info/$','get_player_invitation_info'),
                        )

# 世界BOSS信息
urlpatterns += patterns('game_manager.views.data_edit.boss_info',
                        (r'^data_edit/boss_kyurem_info/$','get_boss_kyurem_info'),
                        (r'^data_edit/boss_snorlax_info/$','get_boss_snorlax_info'),
                        )

# 玩家礼包码信息
urlpatterns += patterns('game_manager.views.data_edit.gift_bag_info',
                        (r'^data_edit/gift_bag_info/$','get_gift_bag_info'),
                        )

# 玩家每日任务
urlpatterns += patterns('game_manager.views.data_edit.daily_task_info',
                        (r'^data_edit/daily_task_info/$','get_daily_task_info'),
                        )

# 玩家商店信息
urlpatterns += patterns('game_manager.views.data_edit.shop_info',
                        (r'^data_edit/stone_shop_info/$','get_stone_shop_info'),
                        (r'^data_edit/pvp_shop_info/$','get_pvp_shop_info'),
                        (r'^data_edit/world_boss_shop_info/$','get_world_boss_shop_info'),
                        (r'^data_edit/ditto_shop_info/$','get_ditto_shop_info'),
                        (r'^data_edit/gym_shop_info/$','get_gym_shop_info'),
                        )

# 玩家道馆信息
urlpatterns += patterns('game_manager.views.data_edit.gym_info',
                        (r'^data_edit/gym_info/$','get_gym_info'),
                        (r'^data_edit/set_gym_zone_star/$','set_gym_zone_star'),
                        (r'^data_edit/set_gym_value/$','set_gym_value'),
                        )
#玩家熔炼精华副本
urlpatterns +=patterns('game_manager.views.data_edit.player_trial_essence_info',
                       (r'^data_edit/player_trial_essence_info/$','get_player_trial_essence_info'),
                       )

#玩家开服七天等级
urlpatterns +=patterns('game_manager.views.data_edit.player_reward_seven_level_info',
                       (r'^data_edit/player_reward_seven_level_info/$','get_player_reward_seven_level_info'),
                       )

#玩家开服七天战力
urlpatterns +=patterns('game_manager.views.data_edit.player_reward_seven_power_info',
                       (r'^data_edit/player_reward_seven_power_info/$','get_player_reward_seven_power_info'),
                       )
#联盟关卡部分数据
urlpatterns +=patterns('game_manager.views.data_edit.union_stage_cas_info',
                       (r'^data_edit/union_stage_cas_info/$','get_union_stage_cas_info'),
                       )