#!usr/bin/env python
# encoding: utf-8

"""
关卡数据处理

"""
import datetime

from apps.models.base.stage_base_model import StageBaseModel
from apps.config import game_config


class Stage(StageBaseModel):

    STAGE_NORMAL = 1
    STAGE_HERO = 3
    STAGE_EXP = 4
    STAGE_GOLD = 5
    STAGE_MONSTER = 6

    STAGE_RANK_COPPER = 2
    STAGE_RANK_SLIVER = 1
    STAGE_RANK_GOLD = 0
    STAGE_RANK_NONE = -1

    def get_stage(self,
                  ):
        """
        获取关卡信息
            Return:
                stage 关卡信息 dict
        """

        if stage_id in self.stages.keys():
            stage_dat = self.stages[stage_id]
            # 合法检测
            if 'rank' not in stage_dat:
                stage_dat['rank'] = self.STAGE_RANK_NONE
            if 'buy_count' not in stage_dat:
                stage_dat['buy_count'] = 0
            return stage_dat
        else:
            stage_dat = dict()
            stage_dat['id'] = stage_id
            stage_dat['num'] = 0
            stage_dat['rank'] = self.STAGE_RANK_NONE
            stage_dat['buy_count'] = 0
            self.stages[stage_id] = stage_dat
            return stage_dat

    def set_stage(self, stage_dat):
        """
            设置关卡数据
        """
        self.stages[stage_dat['id']] = stage_dat


    def get_stage_time(self, stage_id):
        """
            获取关卡次数
        """
        stage = self.get_stage(stage_id)
        return stage.get('num', 0)


    def get_stage_buy_time(self, stage_id):
        """
            获取关卡购买次数
        """
        stage = self.get_stage(stage_id)
        return stage.get('buy_count', 0)


    def add_stage_time(self, stage_id):
        """
            增加关卡次数
            Arg:
                stage_id : 关卡id
        """
        stage = self.get_stage(stage_id)
        if stage:
            cur_num = stage.get('num', 0)
            stage['num'] = cur_num + 1

    def reset_stage_time(self, stage_id):
        """
            重置关卡次数
            Arg:
                stage_id : 关卡id
        """
        stage = self.get_stage(stage_id)
        if stage:
            stage['num'] = 0
            cur_num = stage.get('buy_count', 0)
            stage['buy_count'] = cur_num + 1


    def update_stages(self):
        """
        重置所有关卡数据
            Return BOOL 是否重置了
        """
        now_date = datetime.datetime.now().date()
        # 可以更新
        # print("self.last_reset_time " + str(self.last_reset_time) + "  now_date " + str(now_date))
        if self.last_reset_time != now_date:
            self.last_reset_time = now_date
            new_stages_dict = dict()
            for item in self.stages.values():
                #获取表格默认次数
                config = game_config.get_stages_config(item['id'])
                if config:
                    new_stage_dict = dict()
                    new_stage_dict['id'] = item['id']
                    new_stage_dict['num'] = 0
                    new_stage_dict['buy_count'] = 0
                    new_stage_dict['rank'] = item.get('rank', self.STAGE_RANK_NONE)
                    new_stages_dict[item['id']] = new_stage_dict
            self.stages = new_stages_dict
            return True
        return False

    def set_stage_rank(self, stage_id, rank):
        """
        设置关卡的战斗结果级别
            Arg:
                stage_id 关卡id int
                rank 战斗结果 int
        """
        _stage = self.get_stage(stage_id)
        if _stage:
            _stage['rank'] = rank

    def get_stage_rank(self, stage_id):
        """
        获取关卡战斗结果
            Arg：
                stage_id 关卡ID int
        """
        _stage = self.get_stage(stage_id)
        if _stage:
            return _stage.get('rank', self.STAGE_RANK_NONE)

    @classmethod
    def upgrade_data_version_to_v1(cls, stage_model):
        """
            更新玩家数据
        """
        if isinstance(stage_model.stages, list):
            for stage in stage_model.stages:
                if 'buy_count' not in stage:
                    stage['buy_count'] = 0


    @classmethod
    def upgrade_data_version_to_v2(cls, stage_model):
        """
            数据升级 stages列表转字典格式
            主要是为了加快效率 不再遍历的方式获取关卡数据
        """
        if isinstance(stage_model.stages, list):
            new_stage_dict = dict()
            for stage in stage_model.stages:
                stage_id = stage['id']
                new_stage_dict[stage_id] = stage
            stage_model.stages = new_stage_dict

