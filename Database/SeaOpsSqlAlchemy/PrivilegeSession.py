# -*- coding: utf-8 -*-
__author__ = 'Abbott'

from DbSession import GetSession
from . import tables, logger
from WebApp.config import *

def SelectMenuPrivilege(strUserId):
    """
    @note 查询用户所有菜单权限
    :param strUserId:
    :return:菜单ID列表
    """
    menus_list=[]
    with GetSession() as db_ses:
        menu_list = db_ses.query(tables.MenuPrivilege.mid).filter(tables.MenuPrivilege.uid == strUserId).distinct().all()
        for menu in menu_list:
            menus_list.append(menu[0])
    return menus_list