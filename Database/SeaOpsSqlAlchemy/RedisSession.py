# -*- coding: utf-8 -*-
__author__ = 'Abbott'

from DbSession import GetSession
from . import tables, logger
from WebApp.const import *
from CommonSession import SelectProject

def SelectRedisInfo(strUserId):
    """
    @note 查询redis信息表所有信息
    :return: 以列表形式返回redis所有信息
    """
    redis_list = []
    with GetSession() as db_ses:
        redis_result_info = db_ses.query(tables.Redis, tables.User, tables.Datadict).join(tables.User,
                                                                                          tables.Redis.apply_user_id == tables.User.id).join(
            tables.Datadict, tables.Redis.status == tables.Datadict.value).filter(
            tables.Datadict.pre_id == REDIS_STATUS_PRE_ID, tables.Redis.apply_user_id == strUserId)

        for redisTmp, userTmp, datadictTmp in redis_result_info:
            redis_dic = {'redis_id': redisTmp.redis_id, 'command': redisTmp.command, 'status': datadictTmp.name,
                         'apply_user_id': userTmp.name, 'init_time': redisTmp.init_time,
                         'project_name': redisTmp.project_name, 'redis_filename': redisTmp.redis_filename}
            redis_list.append(redis_dic)

    return redis_list


def InsertRedisInfo(strProjectName, strCommand, strApplyUserId, strRedisFilePath='', strRedisFilename=''):
    """
    @note redis执行信息插入表里
    :param strProjectName:
    :param strCommand:
    :param strApplyUserId:
    :param strRedisFilePath:
    :param strRedisFilename:
    :return:
    """
    with GetSession() as db_ses:
        project_list = SelectProject('None')
        for prj in project_list:
            if strProjectName == prj['prj_keys']:
                redis_insert = tables.Redis(project_id=prj['prj_id'], project_name=prj['prj_name'], status=1, command=strCommand,
                                            apply_user_id=strApplyUserId, redis_file_path=strRedisFilePath,
                                            redis_filename=strRedisFilename)
                db_ses.add(redis_insert)
    return