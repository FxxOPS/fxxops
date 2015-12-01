# -*- coding: utf-8 -*-
__author__ = 'Abbott'

from DbSession import GetSession
from . import tables, logger


def SelectProject(arvg='None'):
    """
    @note 查询所有项目
    :param arvg:
    :return: None: 返回列表值   其他值: 返回字典值
    """
    project_list = []
    with GetSession() as db_ses:

        project_dic = {}
        project_name_dic = {}
        prj_keys_list = []

        project = db_ses.query(tables.Project).all()
        for prj in project:
            project_dic[str(prj.id)] = str(prj.project_keys)

            project_name_dic[str(prj.id)] = {'prj_name': prj.name, 'prj_keys': prj.project_keys}

            prj_dic = {'prj_id': prj.id, 'prj_name': prj.name, 'prj_keys': prj.project_keys}

            prj_keys_list.append(prj.project_keys)
            project_list.append(prj_dic)
    if arvg == 'None':
        return project_list
    elif arvg == 'ProjectDic':
        return project_dic
    elif arvg == 'PrjKeysList':
        return prj_keys_list
    elif arvg == 'PrjNameDic':
        return project_name_dic
    else:
        return project_list
