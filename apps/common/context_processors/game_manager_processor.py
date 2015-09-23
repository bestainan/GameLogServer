#-*- coding: utf-8 -*-
import re
from apps.game_manager.models.game_manager import GameManager


def processor(request):
    """
        内容的processor
    """
    game_manager = GameManager.get_by_request(request)
    if game_manager:
        btn_lst = game_manager.check_admin_permission()
        try:
            path = request.path.split('/')[2]
        except:
            pass
        return {'btn_lst': btn_lst, 'permissions':game_manager.permissions,'account': game_manager.account, 'path':path }
    return {}

