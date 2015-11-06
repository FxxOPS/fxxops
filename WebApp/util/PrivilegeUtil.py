# -*- coding: utf-8 -*-
__author__ = 'Abbott'

from ..const import *
from Database.SeaOpsSqlAlchemy import PrivilegeSession


def BuiltPageMenu(PrivMenuList):
    menu_lev1_list = []
    menu_lev2_list = []
    lev2_list = []
    for menu in PrivMenuList:
        show_list = []
        for priv in menu['menu_pri']:
            for k, v in priv.items():
                if v['r_priv'] == PRIV_TRUE or v['w_priv'] == PRIV_TRUE:
                    show_list.append(TRUE)
                else:
                    show_list.append(FALSE)
        if '1' in list(set(show_list)):
            menu['m_show'] = TRUE
        else:
            menu['m_show'] = FALSE

        if menu['menu_preid'] == PAGE_LEV1_PRE_ID:
            menu_lev1_dic = {'m_lev1_name': menu['menu_name'], 'm_lev1_id': menu['menu_id'],
                             'm_lev1_preid': menu['menu_preid'], 'm_lev1_url': menu['menu_url'],
                             'm_lev1_show': menu['m_show'], 'm_lev2_menu': menu_lev2_list}
            menu_lev1_list.append(menu_lev1_dic)
        else:
            menu_lev2_dic = {'m_lev2_name': menu['menu_name'], 'm_lev2_id': menu['menu_id'],
                             'm_lev2_preid': menu['menu_preid'], 'm_lev2_url': menu['menu_url'],
                             'm_lev2_show': menu['m_show']}
            lev2_list.append(menu_lev2_dic)

    return menu_lev1_list, lev2_list


def IsShowPage(strUserID, strMenuID, strPrivilege='None'):
    user_priv = PrivilegeSession.SelectMenuProjectPrivilege(strUserID, strMenuID)
    if strPrivilege == 'None':
        show_list = []
        for priv in user_priv[0]['menu_pri']:
            for k, v in priv.items():
                if v['r_priv'] == PRIV_TRUE or v['w_priv'] == PRIV_TRUE:
                    show_list.append(TRUE)
                else:
                    show_list.append(FALSE)
            if '1' in list(set(show_list)):
                return TRUE
            else:
                return FALSE

    else:
        priv_list = []
        for priv in user_priv[0]['menu_pri']:
            for k, v in priv.items():
                priv_list.append(v)

        return priv_list


def ReadWirteShowPage(FunctionPrivilege):
    read_list = []
    write_list = []
    funPriv_dic = {}
    for priv in FunctionPrivilege:
        if priv['r_priv'] == '1':
            read_list.append('1')
        else:
            read_list.append('0')

        if priv['w_priv'] == '1':
            write_list.append('1')
        else:
            write_list.append('0')

    if '1' in list(set(read_list)):
        funPriv_dic['r_priv'] = '1'
    else:
        funPriv_dic['r_priv'] = '0'

    if '1' in list(set(write_list)):
        funPriv_dic['w_priv'] = '1'
    else:
        funPriv_dic['w_priv'] = '0'
    return funPriv_dic