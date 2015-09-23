# -*- coding:utf-8 -*-

"""
    游戏错误日志保存
"""

import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler


GAME_ERR_NAME = '/opt/GameServer/logs/game_err.log'



game_err_handler = TimedRotatingFileHandler(GAME_ERR_NAME, 'midnight')
game_stream_handler = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(message)s', datefmt='%Y-%m-%d %H:%M')

game_stream_handler.setFormatter(formatter)
game_err_handler.setFormatter(formatter)
err_log = logging.getLogger('game_err')
err_log.setLevel(logging.DEBUG)
err_log.addHandler(game_err_handler)
err_log.addHandler(game_stream_handler)