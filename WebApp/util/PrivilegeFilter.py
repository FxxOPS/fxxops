# -*- coding: utf-8 -*-
__author__ = 'Abbott'
from .. import WebApp
from ..const import *


@WebApp.template_filter('Showlev1MenuName')
def Showlev1MenuName(MenuPreID):
    """
    @note 将页面对应的菜单ID以菜单名字显示
    :param MenuPreID:
    :return:
    """

    return MENU_ID_DIC[MenuPreID]['menu_name']