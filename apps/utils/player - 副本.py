#!usr/bin/env python
# encoding: utf-8

import datetime
from apps.config import game_config
from apps.models.base.player_base_model import PlayerBaseModel
from apps.logics import formula
from apps.models.name_mapping import NameMapping
from apps.utils import game_define


class Player(PlayerBaseModel):

    def modify_name(self, name):
        """
            修改名字
        """
        if NameMapping.get_user_uid(self.name):
            NameMapping.delete_user_name_uid_mapping(self.name)
        NameMapping.set_user_name_uid_mapping(name, self.uid)
        self.name = name

    def modify_icon(self, icon):
        """
            修改头像
        """
        self.role_id = icon

    def get_change_name_count(self):
        """
            获取改名次数
        """
        return self.change_name_count

    def add_change_name_count(self):
        """
            改名次数加1
        """
        self.change_name_count += 1

    def get_has_change_name_reward(self):
        """
            获取是否获得了改名奖励
        """
        return self.has_change_name_reward

    def set_has_change_name_reward(self):
        """
            设置改名奖励已经获得
        """
        self.has_change_name_reward = True

    def update_stamina(self):
        """
            更新玩家体力
        """
        #获取体力最大值
        _player_level_config = game_config.get_player_level_config(self.level)
        _player_max_stamina = _player_level_config['maxPower']

        # 在消费体力时候判断如果是不满的 就更新到当前时间
        if self.stamina < _player_max_stamina:  # 更新
            _stamina_recover_time = game_config.get_game_config_val_int('PlayerStaminaRecover')
            now = datetime.datetime.now()
            time_dis = now - self.last_stamina_time
            recover_stamina_count = int(time_dis.total_seconds()  / _stamina_recover_time)
            # print("_player_max_stamina " + str(_player_max_stamina) + "  " + str(self.stamina))
            if recover_stamina_count:
                #保存未计算时间
                self.last_stamina_time += datetime.timedelta(seconds=_stamina_recover_time * recover_stamina_count)
                self.stamina += recover_stamina_count
                # 体力满 不计算体力增加
                if self.stamina >= _player_max_stamina:
                    self.stamina = _player_max_stamina

        return self.last_stamina_time

    def cost_stamina(self, num):
        """
        消耗体力
        Arg：
            num 体力数量
        Return：
            bool 成功 失败
        """
        if self.stamina >= num:
            _player_level_config = game_config.get_player_level_config(self.level)
            _player_max_stamina = _player_level_config['maxPower']
            if self.stamina >= _player_max_stamina:
                self.last_stamina_time = datetime.datetime.now()
            self.stamina -= num
            return True
        else:
            return False

    def cost_reset_individual_count(self):
        """
        消耗洗练次数
        Arg：
            num 洗练点
        Return：
            bool 成功 失败
        """
        if self.monster_reset_individual_count > 0:
            #金币洗练次数恢复上限
            _reset_individual_times_max = game_config.get_game_config_val_int('GoldResetTimesMax')
            if self.monster_reset_individual_count >= _reset_individual_times_max:
                self.monster_last_reset_time = datetime.datetime.now()
            self.monster_reset_individual_count -= 1
            return True
        else:
            return False

    def update_reset_individual(self):
        """
            更新宠物洗练次数 洗练时间
        """
        #金币洗练次数恢复上限
        _reset_individual_times_max = game_config.get_game_config_val_int('GoldResetTimesMax')
        if self.monster_last_reset_time and self.monster_reset_individual_count <_reset_individual_times_max:  # 更新
            _reset_individual_recover_time = game_config.get_game_config_val_int('GoldResetCDTime')
            now = datetime.datetime.now()
            time_dis = now - self.monster_last_reset_time
            recover_individual_count = int(time_dis.total_seconds() / _reset_individual_recover_time)
            if recover_individual_count:
                #保存未计算时间
                self.monster_last_reset_time += datetime.timedelta(seconds=_reset_individual_recover_time * recover_individual_count)
                self.monster_reset_individual_count += recover_individual_count
                # 洗练点满 不计算洗练点增加
                if self.monster_reset_individual_count >= _reset_individual_times_max:
                    self.monster_reset_individual_count = _reset_individual_times_max
        return self.monster_last_reset_time

    def get_stamina(self):
        return self.stamina

    def get_last_stamina_time(self):
        return self.last_stamina_time

    def is_stamina_enough(self, num):
        """
        体力足够
        Arg:
            num 体力足够
        """
        return self.stamina >= num

    def update_fishing_count(self):
        """
            更新钓鱼次数
        """
        # print game_config.get_vip_config(self.vip_level)
        # print game_config.get_vip_config(self.vip_level)['fishingTimes']
        # print type(game_config.get_vip_config(self.vip_level)['fishingTimes'])

        # 合法检测
        self.check_fish_time()

        now = datetime.datetime.now()
        # 获取最大值
        max_count = game_config.get_vip_config(self.vip_level)['fishingTimes']

        if self.cur_fishing_left_count < max_count:
            dis_time = now - self.last_fishing_refresh_time
            recover_count = int(dis_time.total_seconds() / game_define.FISHING_REFRESH_TIME)
            if recover_count:
                self.cur_fishing_left_count += recover_count
                self.last_fishing_refresh_time += datetime.timedelta(seconds=game_define.FISHING_REFRESH_TIME * recover_count)
                # 恢复满
                if self.cur_fishing_left_count > max_count:
                    self.cur_fishing_left_count = max_count


    def check_fish_time(self):
        """
            检测钓鱼时间
        """
        # 获取最大值
        max_count = game_config.get_vip_config(self.vip_level)['fishingTimes']
        if self.cur_fishing_left_count >= max_count:
            self.last_fishing_refresh_time = datetime.datetime.now()
        elif (not isinstance(self.last_fishing_refresh_time, datetime.datetime)) and self.cur_fishing_left_count < max_count:
            # VIP增加钓鱼最大次数后 时间要获得
            self.last_fishing_refresh_time = datetime.datetime.now()


    def cost_fishing_count(self, count=1):
        """
        消耗次数
        """
        if self.cur_fishing_left_count >= count:
            self.cur_fishing_left_count -= count
            return True

        return False

    def is_can_fishing(self):
        """
        可以钓鱼
        """
        return self.cur_fishing_left_count > 0


    def get_client_fishing_left_time(self):
        """
        获取钓鱼恢复时间剩余秒数
        """
        max_count = game_config.get_vip_config(self.vip_level)['fishingTimes']
        if self.cur_fishing_left_count < max_count:
            total_sec = (datetime.datetime.now() - self.last_fishing_refresh_time).total_seconds()
            return game_define.FISHING_REFRESH_TIME - int(total_sec)  # 剩余时间(秒)
        else:
            return 0

    def get_client_finger_guess_left_time(self):
        """
        武藏猜拳剩余时间
        """
        if self.last_finger_guess_time:
            return game_define.FINGER_REFRESH_TIME - int((datetime.datetime.now() - self.last_finger_guess_time).total_seconds())   # 剩余时间(秒)
        else:
            return 0

    def add_gold(self, gold):
        """
        添加金币
        """
        _max_gold = game_config.get_game_config_val_int('PlayerMaxGold')
        self.gold += gold
        if self.gold > _max_gold:
            self.gold = _max_gold
        return self.gold

    def get_gold(self):
        return self.gold

    def cost_gold(self, gold):
        """
            消费金币
        """
        if gold < self.gold:
            self.gold -= gold
            self.total_cost_gold += gold
            return True
        return False

    def add_honour(self, honour):
        """
            增加荣誉值
        """
        _max_honour = game_config.get_game_config_val_int('HonorPointsMax')
        self.honour_point += honour
        self.honour_point = int(self.honour_point)
        if self.honour_point > _max_honour:
            self.honour_point = _max_honour
        return self.honour_point

    def add_stone(self, count):
        """
        添加灵石
        """
        new_stone_count = self.stone + count
        _max_stone = game_config.get_game_config_val_int('PlayerMaxStone')
        if new_stone_count > _max_stone:
            new_stone_count = _max_stone
        self.stone = new_stone_count
        return self.stone

    def get_stone(self):
        return self.stone

    def cost_stone(self, num):
        if self.stone >= num:
            self.stone -= num
            self.total_cost_stone += num # 玩家总共消耗钻石数
            return True
        else:
            return False


    def add_free_draw_material(self, count):
        """
            添加免费抽奖材料
        """
        self.free_draw_material += count

        return self.free_draw_material

    def get_free_draw_material(self):
        return self.free_draw_material

    def cost_free_draw_material(self, count):
        """
            扣除玩家的免费抽奖材料
        """
        if self.free_draw_material >= count:
            self.free_draw_material -= count
            return True
        else:
            return False

    def add_exp(self, exp):
        """
        玩家获得经验值
        Arg：
            exp 经验值 int
        Return:
            is_level_up bool
        """
        is_level_up = False
        # cur_exp = self.exp
        self.exp += exp
        cur_level_max_exp = game_config.get_player_level_config(self.level)['exp']
        lv_num = 0
        while self.exp >= cur_level_max_exp:
            self.level += 1
            lv_num += 1
            if self.level > game_config.get_game_config_val_int('PlayerMaxLevel'):
                self.level = game_config.get_game_config_val_int('PlayerMaxLevel')
                self.exp = 0
                return is_level_up,lv_num
            self.exp -= cur_level_max_exp
            _player_level_config = game_config.get_player_level_config(self.level)
            cur_level_max_exp = _player_level_config['exp']
            #体力回复
            _recover_stamina = _player_level_config['recoverPower']
            self.update_stamina()
            self.stamina += _recover_stamina
            is_level_up = True

            # #人物升级log
            # event_log.insert_action_level_up(self.level - 1, cur_exp, self.level, self.exp)
        return is_level_up,lv_num

    def get_client_stamina_left_time(self):
        """
            获取客户端需要的剩余时间
        """
        if self.last_stamina_time:
            return int((datetime.datetime.now() - self.last_stamina_time).total_seconds())   # 剩余时间(秒)
        else:
            return 0

    def add_stamina(self, stamina_count):
        """
        增加玩家的体力
        @return  返会增加后玩家的体力值
        """
        self.stamina += stamina_count
        return self.stamina

    def add_month_card_30(self):
        """
            增加玩家的月卡天数
        """
        add_day = 30
        now_date = datetime.datetime.now().date()
        # 未购买过月卡
        if not self.month_50_indate:
            self.month_50_indate = now_date + datetime.timedelta(days=add_day - 1)
        else:   # 在有效期内
            self.month_50_indate += datetime.timedelta(days=add_day)     # 实际获取
        return self.month_50_indate

    def update_month_card_indate(self):
        """
            更新有效期
        """
        if self.month_50_indate and not isinstance(self.month_50_indate, datetime.date):
            self.month_50_indate = None

        now = datetime.datetime.now().date()
        # 有月卡 并且 超过有效期
        if self.month_50_indate and now > self.month_50_indate:
            self.month_50_indate = None

    def recharge(self, rmb):
        """
        设置玩家充值后的vip level
        返会玩家的rmb， vip_level
        """
        self.rmb += rmb
        #计算VIP等级
        vip_level = game_config.get_vip_level_by_rmb(self.rmb)
        if self.vip_level != vip_level:
            self.vip_level = vip_level
        # 更新钓鱼时间
        self.check_fish_time()
        return vip_level

    def update_vip_level(self):
        """
        设置玩家充值后的vip level
        返会玩家的rmb， vip_level
        """
        #计算VIP等级
        vip_level = game_config.get_vip_level_by_rmb(self.rmb)
        if self.vip_level != vip_level:
            self.vip_level = vip_level
        # 更新钓鱼时间
        self.check_fish_time()
        return vip_level


    def update_buy_stamina_times(self):
        """
        如果跨过时间点重置体力购买次数
        """
        now = datetime.datetime.now()

        if not self.reset_buy_stamina_datetime:
            self.buy_stamina_times = 0
            self.reset_buy_stamina_datetime = now
            self.put()
            return

        reset_time = game_config.get_game_config_val_int_array('ResetTime1', ':')   # hour : min
        reset_time = datetime.datetime(now.year, now.month, now.day, reset_time[0], reset_time[1])
        # 跨过更新时间点
        # print(" " + str(self.reset_buy_stamina_datetime) + "  " + str(reset_time) + " " + str(now) + "   " + str(self.buy_stamina_times))
        if self.reset_buy_stamina_datetime < reset_time <= now:
            self.buy_stamina_times = 0
            self.reset_buy_stamina_datetime = now
            self.put()
            return

    def update_buy_gold_times(self):
        """
            重置金币购买次数
        """
        now = datetime.datetime.now()
        if not self.reset_buy_gold_datetime:
            self.buy_gold_times = 0
            self.reset_buy_gold_datetime = now
            self.put()
            return

        reset_time = game_config.get_game_config_val_int_array('ResetTime1', ':')
        reset_time = datetime.datetime(now.year, now.month, now.day, reset_time[0], reset_time[1])

        if self.reset_buy_gold_datetime < reset_time <= now:
            self.buy_gold_times = 0
            self.reset_buy_gold_datetime = now
            self.put()
            return

    def update_reward_login_series(self):
        """
            更新累积登录奖励
        """
        now_date = datetime.datetime.now().date()
        # 日期不同 并且可以刷新
        if self.reward_login_series_time != now_date and self.reward_login_series_refresh:
            self.reward_login_series_refresh = False
            if self.reward_login_series_id %30 == 0:
                # 需要替换新一组
                reward_len = game_config.get_reward_login_series_config_len()
                # 获取适合的组
                for i in xrange(1, reward_len, 7):
                    new_config = game_config.get_reward_login_series_config(i)
                    if new_config['levelMini'] <= self.level <= new_config['levelMax']:
                        self.reward_login_series_id = i
                        break
            else:
                self.reward_login_series_id += 1


    def update_team_combat_power(self, user):
        """
            更新玩家队伍战斗力
        """
        team_power = formula.GetMonsterTeamCombatPowerWithEffect(user)
        self.team_combat_power = team_power
        if self.cur_max_team_combat_power < team_power:
            self.cur_max_team_combat_power = team_power


    def get_team_combat_power(self):
        return self.team_combat_power


    def get_special_draw_pink_times(self):
        return self.special_draw_pink_times

    def cost_special_draw_pink_times(self, count):
        self.special_draw_pink_times -= count
        if self.special_draw_pink_times <= 0:
            self.special_draw_pink_times = 0

    def set_special_draw_pink_times(self, count):
        self.special_draw_pink_times = count
        if self.special_draw_pink_times <= 0:
            self.special_draw_pink_times = 0


    def add_world_boss_score(self, score):
        """
            增加世界BOSS积分
        """
        self.world_boss_score += score

    def cost_world_boss_score(self, score):
        """
            消耗积分
            Return:
                bool 是否成功
        """
        if self.world_boss_score >= score:
            self.world_boss_score -= score
            return True
        return False

    @classmethod
    def upgrade_data_version_to_v1(cls, player_model):
        """
            更新玩家数据
        """
        if player_model.title == 0:
            player_model.title = 1

    @classmethod
    def upgrade_data_version_to_v2(cls, player_model):
        """
             修改玩家VIP奖励
        """
        if isinstance(player_model.get_vip_level_gift, int):
            player_model.get_vip_level_gift = range(1, player_model.get_vip_level_gift + 1)

    @classmethod
    def upgrade_data_version_to_v3(cls, player_model):
        """
             修改玩家VIP奖励
        """
        # 激活首冲礼包

        if player_model.rmb != 0 and not player_model.is_first_recharge_gift_active:
            player_model.is_first_recharge_gift_active = True


    @classmethod
    def upgrade_data_version_to_v4(cls, player_model):
        """
            修正队伍解锁等级修改带来的 宠物没办法下阵的问题
        """
        pass
        # open_level = game_config.get_game_config_val_int_array("TeamOpenLevel")
        # cur_lv = player_model.level
        # for i in range(5):
        #     # 不合法
        #     if cur_lv < open_level[i]:
        #         player_model.team1[i] = None
        #         player_model.team2[i] = None
        #         player_model.team3[i] = None
        #         player_model.team4[i] = None
        #         player_model.team5[i] = None

    @classmethod
    def upgrade_data_version_to_v5(cls, player_model):
        """
            修正玩家默认头像id 10001
        """
        if int(player_model.role_id) < game_define.PLAYER_ROLE_ID:
            player_model.role_id = game_define.PLAYER_ROLE_ID

    def add_stage_normal_count(self):
        """
            普通副本挑战次数加1
        """
        self.stage_normal_total_count += 1


    def add_stage_hero_count(self):
        """
            困难副本挑战次数加1
        """
        self.stage_hero_total_count += 1


    def add_stage_exp_count(self):
        """
            经验副本挑战次数加1
        """
        self.stage_exp_total_count += 1


    def add_stage_gold_count(self):
        """
            金币副本挑战次数加1
        """
        self.stage_gold_total_count += 1
