# -*- coding=utf-8 -*-


"""
    持久层定义
    CAS : 就是这个Model有读取锁,在存储时要先获得锁在保存
"""

# 逻辑服务器配置保存game_config
CONFIG_MODEL ='zgame|apps.models.common.config.Config|game_config'

CAS_PREFIX = 'cas|'

# 玩家邮件
PLAYER_MAIL_BOX_MODEL = 'zgame|apps.models.mail.player_mail_box.PlayerMailBox|{user_id}'
# 玩家提交的BUG数据
PLAYER_COMMIT_BUGS_MODEL = 'zgame|apps.models.common.player_commit_bug_model.PlayerCommitBugModel|player_commit_bugs'
#系统邮件存储
SYSTEM_MAIL_BOX_MODEL = 'zgame|apps.models.common.system_mail_box.SystemMailBox|game_system_mail_box'
# 广播存储
NOTICE_MODEL = 'zgame|apps.models.common.notice.Notice|game_notice'
# 聊天存储
CHAT_MODEL = 'zgame|apps.models.common.chat.chat_list.ChatListDat|server_chat'
# 联盟聊天存储
UNION_CHAT_MODEL = 'zgame|apps.models.union.union_chat.UnionChat|{union_id}'
# 用户信息
USER_MODEL = 'zgame|apps.models.user.User|{user_id}'
# 账号-uid映射
ACCOUNT_MAPPING_MODEL = 'zgame|apps.models.account_mapping.AccountMapping|{open_id}'
# 名字-uid 映射 hashlib.md5(name).hexdigest().upper()
PLAYER_NICK_NAME_MODEL = "PlayerName_{player_nick_md5}"
# 角色信息
PLAYER_MODEL = 'zgame|apps.models.player.Player|{user_id}'
# 玩家宠物数据
MONSTER_MODEL = 'zgame|apps.models.monster.Monster|{user_id}'
# 玩家区域数据
ZONE_MODEL = 'zgame|apps.models.zone.Zone|{user_id}'
# 玩家关卡数据
STAGE_MODEL = 'zgame|apps.models.stage.Stage|{user_id}'  # 李培庆
# 物品数据
ITEM_MODEL = 'zgame|apps.models.items.Items|{user_id}'
# 玩家邮件数据
MAIL_MODEL = 'zgame|apps.models.mail.player_mail_box.PlayerMailBox|{user_id}'   #李亚冲在做
# 玩家装备数据
EQUIP_MODEL = 'zgame|apps.models.monster_equip.MonsterEquip|{user_id}'             #韩仕杰
# 玩家图鉴
HAND_BOOK_MODEL = 'zgame|apps.models.hand_book.HandBook|{user_id}'         #颖芳
# 玩家竞技场战报
ARENA_BATTLE_REPORT_MODEL = 'zgame|apps.models.player_arena_battle_report.PlayerArenaBattleReport|{user_id}'     #李亚冲在做
# 每日VIP奖励
DAILY_VIP_REWARD_MODEL = 'zgame|apps.models.daily_vip_reward.DailyVipReward|{user_id}'      #李培庆
# 玩家钻石商场
PLAYER_STONE_SHOP_MODEL = 'zgame|apps.models.player_stone_shop.PlayerStoneShop|{user_id}'  #李亚冲
# 玩家PVP商场
PLAYER_PVP_SHOP_MODEL = 'zgame|apps.models.player_pvp_shop.PlayerPvpShop|{user_id}'   #李亚冲
# 玩家试炼数据
PLAYER_TRIAL_MODEL = 'zgame|apps.models.player_trial_battle.PlayerTrialBattle|{user_id}' #李亚冲
# 玩家充值每日奖励
DAILY_RECHARGE_REWARD_MODEL = 'zgame|apps.models.daily_recharge_reward.DailyRechargeReward|{user_id}'   #李亚冲
# 玩家累计充值奖励
SUM_RECHARGE_REWARD_MODEL = 'zgame|apps.models.sum_recharge_reward.SumRechargeReward|{user_id}'          #李亚冲
# 玩家问答活动数据
PLAYER_QUIZ_MODEL = 'zgame|apps.models.player_quiz.PlayerQuiz|{user_id}' #韩仕杰   因需求问题 暂时不做
# 玩家邀请部分数据
PLAYER_INVITATION_MODEL = 'zgame|apps.models.player_invitation.PlayerInvitation|{user_id}'   #李亚冲
# 玩家世界BOSS KYUREM
PLAYER_WORLD_BOSS_KYUREM_MODEL = 'zgame|apps.models.player_world_boss.player_world_boss_kyurem.PlayerWorldBossKyurem|{user_id}'   #李亚冲
# 玩家世界BOSS snorlax
PLAYER_WORLD_BOSS_SNORLAX_MODEL = 'zgame|apps.models.player_world_boss.player_world_boss_snorlax.PlayerWorldBossSnorlax|{user_id}'    #李亚冲
# 玩家世界BOSS商店
PLAYER_WORLD_BOSS_SHOP_MODEL = 'zgame|apps.models.player_world_boss.player_world_boss_shop.PlayerWorldBossShop|{user_id}'    #李亚冲
# 玩家充值数据
PLAYER_PAYMENT_MODEL = 'zgame|apps.models.player_payment.PlayerPayment|{user_id}' #李亚冲
# 百变怪商城
DITTO_SHOP_MODEL = 'zgame|apps.models.ditto_shop.DittoShop|{user_id}'   #李亚冲
# 玩家领取过的礼包码
GIFT_BAG_MODEL = 'zgame|apps.models.common.gift_bag.GiftBag|{user_id}'   #李亚冲 #无数据，先不做了吧！！！
# 玩家每日任务
DAILY_TASK_MODEL = 'zgame|apps.models.daily_task.DailyTask|{user_id}'   #李亚冲
# 30天签到
SIGN_30_MODEL = 'zgame|apps.models.player_sign_30.PlayerSign30|{user_id}'  #全勇男
# 7天登录
LOGIN_7_MODEL = 'zgame|apps.models.player_login_7.PlayerLogin7|{user_id}' #全勇男
# 抓宠副本
CATCH_MONSTER_MODEL = 'zgame|apps.models.player_catch_monster.PlayerCatchMonster|{user_id}'  # 李培庆
# 玩家宝物
TREASURE_ITEM_MODEL = 'zgame|apps.models.treasure.player_treasure_item.PlayerTreasureItem|{user_id}' #全勇男
# 道馆
GYM_MODEL = 'zgame|apps.models.gym.player_gym.PlayerGym|{user_id}' #李亚冲
# 道馆商店
GYM_SHOP_MODEL = 'zgame|apps.models.gym.player_gym_shop.PlayerGymShop|{user_id}'  #李亚冲
# 队伍
TEAM_MODEL = 'zgame|apps.models.player_team.PlayerTeam|{user_id}'  # 李培庆
# 玩家开服7天等级
PLAYER_REWARD_SEVEN_LEVEL_MODEL = 'zgame|apps.models.player_reward_seven_level.PlayerRewardSevenLevel|{user_id}'  #韩仕杰
# 玩家开服7天战力
PLAYER_REWARD_SEVEN_POWER_MODEL = 'zgame|apps.models.player_reward_seven_power.PlayerRewardSevenPower|{user_id}'  #韩仕杰
# 活动： 普通副本次数奖励
PLAYER_ACTIVITY_NORMAL_STAGE_MODEL =  'zgame|apps.models.activity.player_activity_normal_stage.PlayerActivityNormalStage|{user_id}'  # 李培庆
# 活动： 运营活动困难副本
PLAYER_ACTIVITY_HARD_STAGE_MODEL =  'zgame|apps.models.activity.player_activity_hard_stage.PlayerActivityHardStage|{user_id}'   # 李培庆
# 运营活动竞技场 次数奖励
PLAYER_ACTIVITY_ARENA_MODEL =   'zgame|apps.models.activity.player_activity_arena.PlayerActivityArena|{user_id}'   #李亚冲
# 运营活动道馆 次数奖励
PLAYER_ACTIVITY_GYM_MODEL =   'zgame|apps.models.activity.player_activity_gym.PlayerActivityGym|{user_id}'      # 李培庆
# 运营活动夺宝 次数奖励
PLAYER_ACTIVITY_TREASURE_MODEL =   'zgame|apps.models.activity.player_activity_treasure.PlayerActivityTreasure|{user_id}'  # 李培庆
# 运营活动钓鱼 次数奖励
PLAYER_ACTIVITY_FISHING_MODEL =   'zgame|apps.models.activity.player_activity_fishing.PlayerActivityFishing|{user_id}'  # 李培庆

# 联盟部分
# 联盟全部信息
UNION_SEARCH_MODEL = 'zgame|apps.models.union.union_search.UnionSearch|union_search'
# 联盟名字和uid映射 union_name_md5 = hashlib.md5(name).hexdigest().upper()
UNION_NAME_MODEL = 'UnionName_{union_name_md5}'
# 联盟部分数据(这个先别做)
UNION_CAS_MODEL = 'zgame|apps.models.union.union.Union|{union_id}'
# 联盟关卡部分数据
UNION_STAGE_CAS_MODEL = 'zgame|apps.models.union.union_stage.UnionStage|{union_id}'    #韩仕杰  暂时不做

# 玩家猜拳活动数据
PLAYER_ACTIVITY_FINGER_GUESS_MODEL = 'zgame|apps.models.activity.player_activity_finger_guess.PlayerActivityFingerGuess|{user_id}' # 庆
# 运营活动短期限时充值 次数奖励
PLAYER_ACTIVITY_RECHARGE_SHORT_MODEL = 'zgame|apps.models.activity.player_activity_recharge_short.PlayerActivityRechargeShort|{user_id}' # 庆
# 运营活动长期限时充值 次数奖励
PLAYER_ACTIVITY_RECHARGE_LONG_MODEL = 'zgame|apps.models.activity.player_activity_recharge_long.PlayerActivityRechargeLong|{user_id}' # 庆
# 运营活动单笔金额 次数奖励
PLAYER_ACTIVITY_ONE_RECHARGE_MODEL = 'zgame|apps.models.activity.player_activity_one_charge.PlayerActivityOneCharge|{user_id}' # 庆
# 运营活动微信分享奖励
PLAYER_ACTIVITY_WEIXIN_SHARE_MODEL = 'zgame|apps.models.activity.player_activity_weixin_share.PlayerActivityWeiXinShare|{user_id}' # 庆
# 运营活动豪华充值奖励
PLAYER_ACTIVITY_REGIST_RECHARGE_MODEL = 'zgame|apps.models.activity.player_activity_regist_recharge.PlayerActivityRegistRecharge|{user_id}' # 庆
# 活动玩家消耗钻石次数
PLAYER_ACTIVITY_STONE_CONSUMPTION_MODEL = 'zgame|apps.models.activity.player_activity_stone_consumption.PlayerActivityStoneConsumption|{user_id}' # 庆
# 玩家假日商店
PLAYER_ACTIVITY_HOLIDAY_SHOP_MODEL = 'zgame|apps.models.activity.player_activity_holiday_shop.PlayerActivityHolidayShop|{user_id}' # 庆
# 玩家便利商店
PLAYER_ACTIVITY_TIME_LIMITED_SHOP_MODEL = 'zgame|apps.models.activity.player_activity_time_limited_shop.PlayerActivityTimeLimitedShop|{user_id}' # 庆
# 玩家友好商店
PLAYER_ACTIVITY_TIME_LIMITED_SHIFT_SHOP_MODEL = 'zgame|apps.models.activity.player_activity_time_limited_shift_shop.PlayerActivityTimeLimitedShiftShop|{user_id}' # 庆
# 玩家碎片商店
PLAYER_FRAGMENT_SHOP_MODEL = 'zgame|apps.models.player_fragment_shop.PlayerFragmentShop|{user_id}'
# 玩家熔炼精华
PLAYER_TRIAL_ESSENCE_MODEL = 'zgame|apps.models.player_trial_essence.PlayerTrialEssence|{user_id}'      #韩仕杰

# 玩家的联盟数据(这个先别做)
UNION_USER_CAS_MODEL = 'zgame|apps.models.union.union_user.UnionUser|{user_id}'
# 玩家好友(这个先别做)
USER_BUDDY_CAS_MODEL = 'zgame|apps.models.buddy.user_buddy.BuddyUser|{user_id}'
# 玩家好友通讯数据(这个先别做)
BUDDY_CONTACT_CAS_MODEL = 'zgame|apps.models.buddy.buddy_contact.BuddyContact|{user_id}'
# 玩家夺宝
TREASURE_CAS_MODEL = 'zgame|apps.models.treasure.player_treasure.PlayerTreasure|{user_id}'  # 李培庆

# 玩家联盟商店
UNION_SHOP_MODEL = 'zgame|apps.models.union.union_shop.UnionShop|{user_id}'    # Robot
# 玩家私信
PRIVATE_MAIL_MODEL = 'zgame|apps.models.mail.player_private_mail.PlayerPrivateMail|{user_id}'  # Robot

# 玩家竞技场荣誉值
PLAYER_ARENA_HONOUR_CAS_MODEL = 'zgame|apps.models.player_arena_honour.PlayerArenaHonour|{user_id}'
# 问答活动
SERVER_QUIZ_CAS_MODEL = 'zgame|apps.models.common.server_quiz.ServerQuiz|server_quiz'
# 世界boss酋雷姆
SERVER_WORLD_BOSS_KYUREM_CAS_MODEL = 'zgame|apps.models.common.server_world_boss_kyurem.ServerWorldBossKyurem|server_world_boss_kyurem'
# 世界boss卡比兽
SERVER_WORLD_BOSS_SNORLAX_CAS_MODEL = 'zgame|apps.models.common.server_world_boss_snorlax.ServerWorldBossSnorlax|server_world_boss_snorlax'
#夺宝服务器数据
SERVER_TREASURE_CAS_MODEL = 'zgame|apps.models.treasure.server_treasure.ServerTreasure|server_treasure'
#服务器道馆排行
SERVER_GYM_CAS_MODEL = 'zgame|apps.models.gym.server_gym.ServerGym|server_gym'
#更新联盟搜索数据
UPDATE_UNION_SEARCH_ACTION_CAS_MODEL = 'zgame|apps.models.thread_action.update_union_search_action.UpdateUnionSearchAction|update_union_search_action'
#更新联盟关卡排行数据
UPDATE_UNION_STAGE_RANK_ACTION_CAS_MODEL = 'zgame|apps.models.thread_action.update_union_stage_rank_action.UpdateUnionStageRankAction|update_union_stage_rank_action'
#更新联盟等级排行数据
UPDATE_UNION_LEVEL_RANK_ACTION_CAS_MODEL = 'zgame|apps.models.thread_action.update_union_level_rank_action.UpdateUnionLevelRankAction|update_union_level_rank_action'
#更新获取玩家好友搜索
UPDATE_BUDDY_SEARCH_ACTION_CAS_MODEL = 'zgame|apps.models.thread_action.update_buddy_search_action.UpdateBuddySearchAction|update_buddy_search_action'
#更新玩家通讯部分数据
UPDATE_USER_CONTACT_ACTION_CAS_MODEL = 'zgame|apps.models.thread_action.update_user_contact_action.UpdateUserContactAction|update_user_contact_action'
#竞技场事件
ARENA_BATTLE_ACTION_CAS_MODEL = 'zgame|apps.models.thread_action.arena_battle_action.ArenaBattleAction|arena_battle_action'




