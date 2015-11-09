# -*- coding: utf-8 -*-
__author__ = 'Abbott'

from DbSession import GetSession
from . import tables, logger
from sqlalchemy.sql import expression
from sqlalchemy import func
import CommonSession


def SelectMenuPrivilege(strUserId):
    """
    @note 查询用户所有菜单权限
    :param strUserId:
    :return:菜单ID列表
    """
    menus_list = []
    with GetSession() as db_ses:
        menu_list = db_ses.query(tables.MenuPrivilege.mid).filter(
            tables.MenuPrivilege.uid == strUserId).distinct().all()
        for menu in menu_list:
            menus_list.append(menu[0])
    return menus_list


def SelectMenu(strArvg='None'):
    """
    @note 查询所有菜单选项
    :param strArvg: 返回什么样的数据取决于这个值
    :return: None：返回菜单列表 format [{'menu_mid': menu.mid, 'menu_name': menu.name, 'menu_url': menu.url, 'menu_keys': menu.keys}]
              MenuIdDic: 返回以菜单ID为主的字典 format {menu.mid : {'menu_name': menu.name, 'menu_url': menu.url, 'menu_keys': menu.keys}}
              如果什么都没有：返回以菜单keys为主的字典 format {'menu.keys': menu.mid}
    """
    menus_list = []
    menu_dic = {}
    menu_id_dic = {}
    with GetSession() as db_ses:
        menu_list = db_ses.query(tables.Menu).all()
        for menu in menu_list:
            menus_dic = {'menu_mid': menu.mid, 'menu_name': menu.name, 'menu_url': menu.url, 'menu_keys': menu.keys}
            menus_list.append(menus_dic)

            menu_id_dic[menu.mid] = {'menu_name': menu.name, 'menu_url': menu.url, 'menu_keys': menu.keys}

            menu_dic[menu.keys] = menu.mid
    if strArvg == 'None':
        return menus_list
    elif strArvg == 'MenuIdDic':
        return menu_id_dic
    else:
        return menu_dic


def SelectMenuProjectPrivilege(strUserId, strMenuID='None'):
    """
    @note 查询用户菜单权限
    :param strUserId:
    :param strMenuID: None 返回此用户所有菜单权限
                       不为None 返回此用户某个菜单ID的菜单权限
    :return:
    """

    project_dic = CommonSession.SelectProject('ProjectDic')

    menu_list = []
    with GetSession() as db_ses:
        if strMenuID == 'None':
            privilege = db_ses.query(tables.MenuPrivilege.mid, tables.Menu.name, tables.Menu.url, tables.Menu.preid,
                                     expression.label('privileges', func.group_concat(tables.MenuPrivilege.pid, ";",
                                                                                      tables.MenuPrivilege.r_priv, ";",
                                                                                      tables.MenuPrivilege.w_priv))).join(
                tables.Menu, tables.MenuPrivilege.mid == tables.Menu.mid).filter(
                tables.MenuPrivilege.uid == strUserId).group_by(tables.MenuPrivilege.mid).all()

        else:
            privilege = db_ses.query(tables.MenuPrivilege.mid, tables.Menu.name, tables.Menu.url, tables.Menu.preid,
                                     expression.label('privileges', func.group_concat(tables.MenuPrivilege.pid, ";",
                                                                                      tables.MenuPrivilege.r_priv, ";",
                                                                                      tables.MenuPrivilege.w_priv))).join(
                tables.Menu, tables.MenuPrivilege.mid == tables.Menu.mid).filter(
                tables.MenuPrivilege.uid == strUserId, tables.MenuPrivilege.mid == strMenuID).group_by(
                tables.MenuPrivilege.mid).all()
        for menu in privilege:
            priv_list = []
            for prjs in str(menu[4]).split(','):

                priv = prjs.split(';')
                prj_dic = {}
                if priv[0] in project_dic.keys():
                    prj_dic[project_dic[priv[0]]] = {'pid': priv[0], 'r_priv': priv[1], 'w_priv': priv[2]}
                    priv_list.append(prj_dic)

            menu_dic = {'menu_id': menu[0], 'menu_name': menu[1], 'menu_url': menu[2], 'menu_preid': menu[3],
                        'menu_pri': priv_list}
            menu_list.append(menu_dic)
    return menu_list


def InsertNewUserPrivilege(strUserID):
    """
    @note 创建用户的时候插入的初始数据权限数据
    :param strUserID:
    :return:
    """
    menu = SelectMenu()
    prj = CommonSession.SelectProject()
    with GetSession() as db_ses:
        for m in menu:
            for p in prj:
                menu = tables.MenuPrivilege(uid=strUserID, mid=m['menu_mid'], pid=p['prj_id'])
                db_ses.add(menu)
    return


def UpdateUserPrivilege(strUserID, strMenuID, PrivilegeList):
    """
    @note 更新权限信息
    :param strUserID: 用户ID
    :param strMenuID: 菜单ID
    :param PrivilegeList: 新的要更新的权限信息
    :return:
    """
    with GetSession() as db_ses:
        for PrivilegeDic in PrivilegeList:
            db_ses.query(tables.MenuPrivilege).filter(tables.MenuPrivilege.uid == strUserID,
                                                      tables.MenuPrivilege.mid == strMenuID,
                                                      tables.MenuPrivilege.pid == PrivilegeDic['pid']).update(
                {"r_priv": PrivilegeDic['R'], "w_priv": PrivilegeDic['W']})

    # 根据2级菜单的使用情况随之而改变的1级菜单的权限
    with GetSession() as db_ses:
        preid = db_ses.query(tables.Menu.preid).filter(tables.Menu.mid == strMenuID).first()
        if preid[0] != 0:
            mid = db_ses.query(tables.Menu.mid).filter(tables.Menu.preid == preid[0]).all()
            mid_list = [m[0] for m in mid]
            menu_list = SelectSingeMenuPrivilege(strUserID, mid_list)
            show_list = []
            for menu in menu_list:
                for priv in menu['menu_pri']:
                    for k, v in priv.items():
                        if v['r_priv'] == '1' or v['w_priv'] == '1':
                            show_list.append('1')
                        else:
                            show_list.append('0')
            if '1' in list(set(show_list)):
                db_ses.query(tables.MenuPrivilege).filter(tables.MenuPrivilege.uid == strUserID,
                                                          tables.MenuPrivilege.mid == preid[0]).update(
                    {"r_priv": 1, "w_priv": 0})
            else:
                db_ses.query(tables.MenuPrivilege).filter(tables.MenuPrivilege.uid == strUserID,
                                                          tables.MenuPrivilege.mid == preid[0]).update(
                    {"r_priv": 0, "w_priv": 0})

    return


def SelectSingeMenuPrivilege(strUserID, MidList):
    """
    @note 查询列表里菜单ID的权限
    :param strUserID:
    :param MidList:
    :return: 返回菜单权限列表
    """
    project_dic = CommonSession.SelectProject('ProjectDic')
    menu_list = []
    with GetSession() as db_ses:
        privilege = db_ses.query(tables.MenuPrivilege.mid, tables.Menu.name, tables.Menu.url, tables.Menu.preid,
                                 expression.label('privileges', func.group_concat(tables.MenuPrivilege.pid, ";",
                                                                                  tables.MenuPrivilege.r_priv, ";",
                                                                                  tables.MenuPrivilege.w_priv))).join(
            tables.Menu, tables.MenuPrivilege.mid == tables.Menu.mid).filter(tables.MenuPrivilege.uid == strUserID,
                                                                             tables.MenuPrivilege.mid.in_(
                                                                                 MidList)).group_by(
            tables.MenuPrivilege.mid).all()
        for menu in privilege:
            priv_list = []
            for prjs in str(menu[4]).split(','):

                priv = prjs.split(';')
                prj_dic = {}
                if priv[0] in project_dic.keys():
                    prj_dic[project_dic[priv[0]]] = {'pid': priv[0], 'r_priv': priv[1], 'w_priv': priv[2]}
                    priv_list.append(prj_dic)

            menu_dic = {'menu_id': menu[0], 'menu_name': menu[1], 'menu_url': menu[2], 'menu_preid': menu[3],
                        'menu_pri': priv_list}
            menu_list.append(menu_dic)
    return menu_list