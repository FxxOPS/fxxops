# -*- coding: utf-8 -*-
'''
Created on 2014年5月28日

@author: yuan.gao6
'''
import json
from contextlib import contextmanager
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from . import tables, logger
from WebApp.config import *

@contextmanager
def GetSession():
    """
    @note 生成session
    @return: Session类实例
    """
    session = Session()
    try:
        yield session
    except Exception, err:
        session.rollback()
        logger.error('====== db_session - GetSession : err start')
        logger.error(err)
        logger.error('====== db_session - GetSession : err end')
    else:
        session.commit()
    finally:
        session.close()


def SelectProject(iUserId=0, bVisible=True):
    """
    @note 获取用户有权限访问的分组列表
    @param iUserId:用户ID
    @param bVisible:是否可见
    @return: 项目ID 项目名称（字典）列表
    """
    lstProject = []
    with GetSession() as db_ses:
        if (0 == iUserId):
            # 查询所有分组
            for it in db_ses.query(tables.Project.id, tables.Project.name).order_by(tables.Project.name).all():
                dictTmp = {"id": it.id, "name": it.name}
                lstProject.append(dictTmp)
            return lstProject

        # 查询当前用户有权限查看的所有分组
        for it in db_ses.query(tables.Project.id, tables.Project.name).distinct(). \
                filter(tables.User.id == iUserId). \
                filter(tables.Server.visible == bVisible). \
                filter(tables.Server.project_id == tables.Project.id). \
                filter(tables.PrivilegeProject.project_id == tables.Project.id). \
                filter(tables.PrivilegeProject.user_id == tables.User.id). \
                filter(tables.PrivilegeProject.read == 1).order_by(tables.Project.name).all():
            dictTmp = {"id": it.id, "name": it.name}
            lstProject.append(dictTmp)

    if (0 == len(lstProject)):
        logger.info("query project by user %s failed" % iUserId)
    return lstProject


def SelectProjectName(iUserId=0, bVisible=True):
    """
    @note 获取用户有权限访问的分组列表
    @param iUserId:用户ID
    @param bVisible:是否可见
    @return: 分组名（字符串）列表
    """
    lstProject = []
    with GetSession() as db_ses:
        if (0 == iUserId):
            # 查询所有分组
            for it in db_ses.query(tables.Project.name).order_by(tables.Project.name).all():
                lstProject.append(it.name)
            return lstProject

        # 查询当前用户有权限查看的所有分组
        for it in db_ses.query(tables.Project.name).distinct(). \
                filter(tables.User.id == iUserId). \
                filter(tables.PrivilegeProject.user_id == tables.User.id). \
                filter(tables.PrivilegeProject.project_id == tables.Project.id). \
                filter(tables.Server.project_id == tables.Project.id). \
                filter(tables.Server.visible == bVisible). \
                filter(tables.PrivilegeProject.read == 1).order_by(tables.Project.name).all():
            lstProject.append(it.name)

    if (0 == len(lstProject)):
        logger.info("query project Name by user %s failed" % iUserId)
    return lstProject


def SelectProjectByID(iProjectId):
    """
    @note 获取指定项目名称
    @param iProjectId:用户ID
    @return: 项目名称（字符串）
    """
    with GetSession() as db_ses:
        rcdTmp = db_ses.query(tables.Project).filter(tables.Project.id == iProjectId).first()
        if (None == rcdTmp):
            return None
        dictTmp = {"id": rcdTmp.id, "name": rcdTmp.name}

    return dictTmp


def SelectProjectByName(strName, iUserId, bVisible=True):
    """
    @note 根据指定分组名称获取用户有权限访问的分组
    @param strName:分组名称
    @param iUserId:用户ID
    @param bVisible:是否可见
    @return: 分组名（字符串）列表
    """
    with GetSession() as db_ses:
        # 查询当前用户有权限查看的所有分组
        rcdProject = db_ses.query(tables.Project). \
            filter(tables.User.id == iUserId). \
            filter(tables.Project.name == strName). \
            filter(tables.Server.visible == bVisible). \
            filter(tables.Server.project_id == tables.Project.id). \
            filter(tables.PrivilegeProject.project_id == tables.Project.id). \
            filter(tables.PrivilegeProject.user_id == tables.User.id). \
            filter(tables.PrivilegeProject.read == 1).order_by(tables.Project.name).first()

        if (None == rcdProject):
            logger.info("query project by name %s failed" % strName)
            return None

        dictProject = {"id": rcdProject.id, "name": rcdProject.name}
    return dictProject


def SelectProjectByIdc(strIdcName, iUserId=0):
    """
    @note 获取指定机房中用户有权限访问的分组列表
    @param iUserId:用户ID
    @param strIdcName:idc名称
    @return: 分组名（字符串）列表
    """
    lstProject = []
    with GetSession() as db_ses:
        if (0 == iUserId):
            # 查询所有分组
            for it in db_ses.query(tables.Project.name).distinct(). \
                    filter(tables.Server.idc == strIdcName). \
                    filter(tables.Server.visible == 1). \
                    filter(tables.Server.project_id == tables.Project.id).order_by(tables.Project.name).all():
                lstProject.append(it.name)
            return lstProject

        # 查询当前用户有权限查看的所有分组
        for it in db_ses.query(tables.Project.name).distinct(). \
                filter(tables.User.id == iUserId). \
                filter(tables.Server.idc == strIdcName). \
                filter(tables.Server.visible == 1). \
                filter(tables.Server.project_id == tables.Project.id). \
                filter(tables.PrivilegeProject.project_id == tables.Project.id). \
                filter(tables.PrivilegeProject.user_id == tables.User.id). \
                filter(tables.PrivilegeProject.read == 1).order_by(tables.Project.name).all():
            lstProject.append(it.name)

    if (0 == len(lstProject)):
        logger.info("query project by idc %s user %s failed" % (strIdcName, iUserId))
    return lstProject


def SelectProjectBySet(strSetName):
    """
    @note 获取指定操作集所属的项目名称
    @param strSetName:操作集名称
    @return: 项目名称（字符串）
    """
    with GetSession() as db_ses:
        # 查询当前用户有权限查看的所有分组
        rcdTmp = db_ses.query(tables.Project).distinct(). \
            filter(tables.Project.id == tables.Set.project_id). \
            filter(tables.Set.name == strSetName).first()

        if (None == rcdTmp):
            logger.info("query project by server set %s failed" % (strSetName))
            return None
        dictTmp = {"id": rcdTmp.id, "name": rcdTmp.name}

    return dictTmp


def SelectIdcName(iUserId=0, bVisible=True):
    """
    @note 获取用户有权限访问的机房列表
    @param iUserId:用户ID
    @param bVisible:是否可见
    @return: IDC名（字符串）列表
    """
    lstIdc = []
    with GetSession() as db_ses:
        if (0 == iUserId):
            # 查询所有分组
            for it in db_ses.query(tables.Project.name).order_by(tables.Project.name).all():
                lstIdc.append(it.name)
            return lstIdc

        # 查询当前用户有权限查看的所有机房
        for it in db_ses.query(tables.Server.idc).distinct(). \
                filter(tables.User.id == iUserId). \
                filter(tables.Server.visible == bVisible). \
                filter(tables.Server.project_id == tables.Project.id). \
                filter(tables.PrivilegeProject.project_id == tables.Project.id). \
                filter(tables.PrivilegeProject.user_id == tables.User.id). \
                filter(tables.PrivilegeProject.read == 1).order_by(tables.Server.idc).all():
            lstIdc.append(it.idc)

    if (0 == len(lstIdc)):
        logger.info("query idc by user %s failed" % iUserId)

    return lstIdc


def SelectServer(iUserId=0, bVisible=True):
    """
    @note 获取用户有权限访问的主机列表
    @param iUserId:用户ID
    @param bVisible:是否可见
    @return: 主机（字典）列表
    """
    lstServer = []
    with GetSession() as db_ses:
        if (0 == iUserId):
            # 数据库中插叙已停机的主机相关信息(已停机主机的visible字段被置为0)
            lstRcd = db_ses.query(tables.Server, tables.Project). \
                filter(tables.Server.visible == bVisible). \
                order_by(tables.Project.name).order_by(tables.Server.domain).all()
        else:
            # 数据库中插叙已停机的主机相关信息(已停机主机的visible字段被置为0)
            lstRcd = db_ses.query(tables.Server, tables.Project). \
                filter(tables.User.id == iUserId). \
                filter(tables.Server.visible == bVisible). \
                filter(tables.Server.project_id == tables.Project.id). \
                filter(tables.PrivilegeProject.project_id == tables.Project.id). \
                filter(tables.PrivilegeProject.user_id == tables.User.id). \
                filter(tables.PrivilegeProject.read == 1). \
                order_by(tables.Project.name).order_by(tables.Server.domain).all()

        if (lstRcd != None):
            for rcdServer in lstRcd:
                # if (rcdServer.Server.comment == '' ):
                #    rcdServer.Server.comment = "添加"
                dictTmp = {"id": rcdServer.Server.id,
                           "domain": rcdServer.Server.domain,
                           "status": rcdServer.Server.stat,
                           "ip_ex": rcdServer.Server.ip_ex,
                           "ip_in": rcdServer.Server.ip_in,
                           "host_ip": rcdServer.Server.host_ip,
                           "project": rcdServer.Project.name,
                           "idc": rcdServer.Server.idc,
                           "usages": rcdServer.Server.usages,
                           "os": rcdServer.Server.os,
                           "cpu": rcdServer.Server.cpu,
                           "memory": rcdServer.Server.memory,
                           "disk": rcdServer.Server.disk,
                           "pool": rcdServer.Server.pool,
                           "comment": rcdServer.Server.comment}
                lstServer.append(dictTmp)

    if (0 == len(lstServer)):
        logger.info("query server by user %s failed" % iUserId)
    return lstServer


def SelectServerById(iServerId, iUserId=0, bVisible=True):
    """
    @note 获取指定ID的主机
    @param iServerId:主机ID
    @param iUserId:用户ID
    @param bVisible:是否可见
    @return: 主机（字典）
    """
    with GetSession() as db_ses:
        if (0 == iUserId):
            # 数据库中插叙已停机的主机相关信息(已停机主机的visible字段被置为0)
            rcdServer = db_ses.query(tables.Server, tables.Project). \
                filter(tables.Server.id == iServerId). \
                filter(tables.Server.visible == bVisible). \
                order_by(tables.Project.name).first()
        else:
            # 数据库中插叙已停机的主机相关信息(已停机主机的visible字段被置为0)
            rcdServer = db_ses.query(tables.Server, tables.Project). \
                filter(tables.User.id == iUserId). \
                filter(tables.Server.id == iServerId). \
                filter(tables.Server.visible == bVisible). \
                filter(tables.Server.project_id == tables.Project.id). \
                filter(tables.PrivilegeProject.project_id == tables.Project.id). \
                filter(tables.PrivilegeProject.user_id == tables.User.id). \
                filter(tables.PrivilegeProject.read == 1).first()

        if (None == rcdServer):
            logger.error("query server %s by user %s failed" % (iServerId, iUserId))
            return None

        dictTmp = {"id": rcdServer.Server.id,
                   "domain": rcdServer.Server.domain,
                   "status": rcdServer.Server.stat,
                   "ip_ex": rcdServer.Server.ip_ex,
                   "ip_in": rcdServer.Server.ip_in,
                   "host_ip": rcdServer.Server.host_ip,
                   "project": rcdServer.Project.name,
                   "idc": rcdServer.Server.idc,
                   "usages": rcdServer.Server.usages,
                   "os": rcdServer.Server.os,
                   "cpu": rcdServer.Server.cpu,
                   "memory": rcdServer.Server.memory,
                   "disk": rcdServer.Server.disk,
                   "pool": rcdServer.Server.pool,
                   "comment": rcdServer.Server.comment}
    return dictTmp


def SelectServerByProject(strProjectName, iUserId=0):
    """
    @note 获取指定分组内的主机列表
    @param iUserId:用户ID
    @param strProjectName:分组名称
    @return: 主机（字典）列表
    """
    with GetSession() as db_ses:
        lstServer = []
        if (0 == iUserId):
            # 数据库中查询指定分组名称的主机
            lstRcd = db_ses.query(tables.Server, tables.Project). \
                filter(tables.Project.name == strProjectName). \
                filter(tables.Server.visible == 1). \
                filter(tables.Server.project_id == tables.Project.id). \
                order_by(tables.Server.pool.desc(), tables.Server.ip_in).all()
        else:
            # 数据库中查询指定分组名称的主机
            lstRcd = db_ses.query(tables.Server, tables.Project). \
                filter(tables.User.id == iUserId). \
                filter(tables.Project.name == strProjectName). \
                filter(tables.Server.visible == 1). \
                filter(tables.Server.project_id == tables.Project.id). \
                filter(tables.PrivilegeProject.project_id == tables.Project.id). \
                filter(tables.PrivilegeProject.user_id == tables.User.id). \
                filter(tables.PrivilegeProject.read == 1). \
                order_by(tables.Server.pool.desc(), tables.Server.ip_in).all()

        if (None == lstRcd):
            logger.info("query server by project %s user %s failed" % (strProjectName, iUserId))
            return None

        if (lstRcd != None):
            for rcdServer in lstRcd:
                # logger.info ("comment:%s" %(rcdServer.Server.comment))
                #if rcdServer.Server.comment is None:
                #    rcdServer.Server.comment = "添加"
                dictTmp = {"id": rcdServer.Server.id,
                           "domain": rcdServer.Server.domain,
                           "status": rcdServer.Server.stat,
                           "ip_ex": rcdServer.Server.ip_ex,
                           "ip_in": rcdServer.Server.ip_in,
                           "host_ip": rcdServer.Server.host_ip,
                           "project": rcdServer.Project.name,
                           "idc": rcdServer.Server.idc,
                           "usages": rcdServer.Server.usages,
                           "os": rcdServer.Server.os,
                           "cpu": rcdServer.Server.cpu,
                           "memory": rcdServer.Server.memory,
                           "disk": rcdServer.Server.disk,
                           "pool": rcdServer.Server.pool,
                           "comment": rcdServer.Server.comment}
                lstServer.append(dictTmp)
    return lstServer


def SelectServerByIdc(strIdcName, iUserId=0):
    """
    @note 获取指定机房内的主机列表
    @param iUserId:用户ID
    @param strIdcName:机房名称
    @return: 主机（字典）列表
    """
    with GetSession() as db_ses:
        lstServer = []
        if (0 == iUserId):
            # 数据库中查询指定分组名称的主机
            lstRcd = db_ses.query(tables.Server, tables.Project). \
                filter(tables.Server.idc == strIdcName). \
                filter(tables.Server.visible == 1). \
                filter(tables.Server.project_id == tables.Project.id). \
                order_by(tables.Project.name).order_by(tables.Server.domain).all()
        else:
            # 数据库中查询指定分组名称的主机
            lstRcd = db_ses.query(tables.Server, tables.Project). \
                filter(tables.User.id == iUserId). \
                filter(tables.Server.idc == strIdcName). \
                filter(tables.Server.visible == 1). \
                filter(tables.Server.project_id == tables.Project.id). \
                filter(tables.PrivilegeProject.project_id == tables.Project.id). \
                filter(tables.PrivilegeProject.user_id == tables.User.id). \
                filter(tables.PrivilegeProject.read == 1). \
                order_by(tables.Project.name).order_by(tables.Server.domain).all()

        if (None == lstRcd):
            logger.info("query server by idc %s user %s failed" % (strIdcName, iUserId))
            return None

        if (lstRcd != None):
            for rcdServer in lstRcd:
                dictTmp = {"id": rcdServer.Server.id,
                           "domain": rcdServer.Server.domain,
                           "status": rcdServer.Server.stat,
                           "ip_ex": rcdServer.Server.ip_ex,
                           "ip_in": rcdServer.Server.ip_in,
                           "host_ip": rcdServer.Server.host_ip,
                           "project": rcdServer.Project.name,
                           "idc": rcdServer.Server.idc,
                           "usages": rcdServer.Server.usages,
                           "os": rcdServer.Server.os,
                           "cpu": rcdServer.Server.cpu,
                           "memory": rcdServer.Server.memory,
                           "disk": rcdServer.Server.disk,
                           "pool": rcdServer.Server.pool,
                           "comment": rcdServer.Server.comment}
                lstServer.append(dictTmp)
    return lstServer


def SelectServerBySet(strSetName):
    """
    @note 获取指定操作集内的主机列表
    @param iUserId:用户ID
    @param strSetName:操作集名称
    @return: 主机（字典）列表
    """
    with GetSession() as db_ses:
        lstServer = []
        # 数据库中查询指定分组名称的主机
        lstRcd = db_ses.query(tables.Server, tables.Project). \
            filter(tables.Server_Set.set_id == tables.Set.id). \
            filter(tables.Server_Set.server_id == tables.Server.id). \
            filter(tables.Project.id == tables.Server.project_id). \
            filter(tables.Set.name == strSetName).all()
        if (None == lstRcd or 0 == len(lstRcd)):
            logger.info("query server by set %s failed" % (strSetName))
            return None

        if (lstRcd != None):
            for rcdServer in lstRcd:
                dictTmp = {"id": rcdServer.Server.id,
                           "domain": rcdServer.Server.domain,
                           "status": rcdServer.Server.stat,
                           "ip_ex": rcdServer.Server.ip_ex,
                           "ip_in": rcdServer.Server.ip_in,
                           "host_ip": rcdServer.Server.host_ip,
                           "project": rcdServer.Project.name,
                           "idc": rcdServer.Server.idc,
                           "usages": rcdServer.Server.usages,
                           "os": rcdServer.Server.os,
                           "cpu": rcdServer.Server.cpu,
                           "memory": rcdServer.Server.memory,
                           "disk": rcdServer.Server.disk,
                           "pool": rcdServer.Server.pool,
                           "comment": rcdServer.Server.comment}
                lstServer.append(dictTmp)
    return lstServer


def SelectCommentByServer(iServerId):
    """
    @note 获取指定主机的历史备注
    @param iServerId:主机ID
    @return: 备注（字典）列表
    """
    with GetSession() as db_ses:
        lstComment = []
        for rcdComment in db_ses.query(tables.CommentHistory).filter(tables.CommentHistory.server_id == iServerId):
            lstComment.append({'server_id': rcdComment.server_id, 'history': rcdComment.comment,
                               'update_time': rcdComment.update_time})

    if (0 == len(lstComment)):
        logger.info("query server %s comment history failed" % (iServerId))
    return lstComment


def UpdateComment(iServerId, iUserId, strComment):
    """
    @note 更新备注
    @param iServerId:主机ID
    @param iUserId:用户ID
    @param strComment:备注信息
    @return:
    """
    with GetSession() as db_ses:
        # 将当前备注信息添加到历史备注
        rcdComment = db_ses.query(tables.Server.comment).filter(tables.Server.id == iServerId).first()
        comment_history = tables.CommentHistory(server_id=iServerId, comment=rcdComment.comment)
        db_ses.add(comment_history)

        #将当前备注信息改为用户输入的值
        db_ses.query(tables.Server).filter(tables.Server.id == iServerId).update({"comment": strComment})
    return


def InsertUser(strUserName, strPassword, iType, strCtime):
    """
    @note 新增用户
    @param strUserName:用户名
    @param strPassword:密码
    @return:
    """
    with GetSession() as db_ses:
        user = tables.User(name=strUserName, password=strPassword, type=iType, create_time=strCtime)
        db_ses.add(user)

        user_id = db_ses.query(tables.User.id).filter(tables.User.name == strUserName).first()
    return user_id


def SelectUser():
    """
    @note 获取所有用户信息
    @param strUserName:用户名
    @param strPassword:密码
    @return:
    """
    lstUser = []
    with GetSession() as db_ses:
        for rcdUser in db_ses.query(tables.User).order_by(tables.User.create_time.desc()):
            dictUser = {"id": rcdUser.id, "name": rcdUser.name, "password": rcdUser.password,
                        "create_time": rcdUser.create_time}
            if (0 == rcdUser.type):
                dictUser["type"] = u"系统管理员"
            elif (1 == rcdUser.type):
                dictUser["type"] = u"运维"
            elif (2 == rcdUser.type):
                dictUser["type"] = u"运营"
            else:
                continue
            lstUser.append(dictUser)
    if (0 == len(lstUser)):
        logger.info("query user failed")
    return lstUser


def DeleteUser(iUserId):
    """
    @note 删除用户
    @param iUserId:用户ID
    @return:
    """
    with GetSession() as db_ses:
        # 从数据库中删除指定ID用户的所有权限
        db_ses.query(tables.PrivilegeProject).filter(tables.PrivilegeProject.user_id == iUserId).delete()
        #从数据库中删除指定ID用户的所有权限
        db_ses.query(tables.PrivilegeSet).filter(tables.PrivilegeSet.user_id == iUserId).delete()
        #从数据库中删除指定ID的用户
        db_ses.query(tables.User).filter(tables.User.id == iUserId).delete()
    return


def SelectUserByName(strUserName):
    """
    @note 获取指定用户名的用户信息
    @param strUserName:用户名
    @return:
    """
    with GetSession() as db_ses:
        rcdUser = db_ses.query(tables.User.id, tables.User.name, tables.User.password, tables.User.type,
                               tables.User.create_time).filter(tables.User.name == strUserName).first()

    if (None == rcdUser):
        logger.error("query user %s failed" % strUserName)
        return None

    dictUser = {"id": rcdUser.id, "name": rcdUser.name, "password": rcdUser.password, "type": rcdUser.type,
                "create_time": rcdUser.create_time}
    return dictUser


def SelectUserById(iUserId):
    """
    @note 获取指定用户ID的用户信息
    @param iUserId:用户ID
    @return:
    """
    with GetSession() as db_ses:
        rcdUser = db_ses.query(tables.User.id, tables.User.name, tables.User.password).filter(
            tables.User.id == iUserId).first()

    if (None == rcdUser):
        logger.error("query user %s failed" % iUserId)
        return None

    dictUser = {"id": rcdUser.id, "name": rcdUser.name, "password": rcdUser.password}
    return dictUser


def UpdateUserPassword(iUserId, strPassword):
    """
    @note 修改用户密码
    @param iUserId:用户ID
    @param strPassword:用户密码
    @return:
    """
    with GetSession() as db_ses:
        db_ses.query(tables.User).filter(tables.User.id == iUserId).update({"password": strPassword})


def SelectProjectPrivilege(iUserId):
    """
    @note 获取指定用户的权限
    @param iUserId:用户ID
    @return: 分组及权限（字典）列表
    """
    lstResult = []
    with GetSession() as db_ses:
        lstRcd = db_ses.query(tables.Project, tables.PrivilegeProject). \
            outerjoin(tables.PrivilegeProject,
                      and_(tables.Project.id == tables.PrivilegeProject.project_id,
                           tables.PrivilegeProject.user_id == iUserId)).order_by(tables.Project.id.desc()).all()
        if (None == lstRcd):
            logger.info("can't find user %s project privilege" % (iUserId))
            return None

        for project, privilege in lstRcd:
            if (None == privilege):
                dictPrivilege = {"project_id": project.id,
                                 "project_name": project.name,
                                 "read": "0",
                                 "write": "0"}
            else:
                dictPrivilege = {"project_id": project.id,
                                 "project_name": project.name,
                                 "read": privilege.read,
                                 "write": privilege.write}
            lstResult.append(dictPrivilege)

    if (0 == len(lstResult)):
        logger.info("query user %s privilege failed" % (iUserId))
    return lstResult


def SelectPorjectPrivilegeByProject(strProjectName, iUserId):
    """
    @note 获取指定用户对指定分组的权限
    @param iServerId：主机ID
    @param strProjectName:分组名称
    @return: 主机权限（字典）
    """
    with GetSession() as db_ses:
        rcdPrivilege = db_ses.query(tables.PrivilegeProject). \
            filter(tables.Project.id == tables.PrivilegeProject.project_id). \
            filter(tables.PrivilegeProject.user_id == iUserId). \
            filter(tables.Project.name == strProjectName).first()
        if (None == rcdPrivilege):
            dictPrivilege = {"read": "0", "write": "0"}
        else:
            dictPrivilege = {"read": rcdPrivilege.read, "write": rcdPrivilege.write}
    return dictPrivilege


def SelectProjectPrivilegeByServer(iServerId, iUserId):
    """
    @note 获取指定用户对指定主机的权限
    @param iServerId：主机ID
    @param iUserId:用户ID
    @return: 主机权限（字典）
    """
    with GetSession() as db_ses:
        rcdPrivilege = db_ses.query(tables.PrivilegeProject). \
            filter(tables.User.id == iUserId). \
            filter(tables.Server.id == iServerId). \
            filter(tables.Server.visible == 1). \
            filter(tables.Server.project_id == tables.PrivilegeProject.project_id). \
            filter(tables.PrivilegeProject.user_id == tables.User.id). \
            filter(tables.PrivilegeProject.read == 1).first()
        if (None == rcdPrivilege):
            dictPrivilege = {"read": "0", "write": "0"}
        else:
            dictPrivilege = {"read": rcdPrivilege.read, "write": rcdPrivilege.write}
    return dictPrivilege


def UpdateProjectPrivilege(iProjectId, iUserId, iRead, iWrite):
    """
    @note 修改指定用户对指定分组的权限
    @param iServerId：主机ID
    @param iProjectId:分组ID
    @param iRead:读权限（1=有，0=无）
    @param iWrite:写权限（1=有，0=无）
    @return:
    """
    with GetSession() as db_ses:
        rcdTmp = db_ses.query(tables.PrivilegeProject). \
            filter(tables.PrivilegeProject.project_id == iProjectId). \
            filter(tables.PrivilegeProject.user_id == iUserId).first()
        if (None == rcdTmp):
            if (1 == iRead or 1 == iWrite):
                prvlgTmp = tables.PrivilegeProject(project_id=iProjectId, user_id=iUserId, read=iRead, write=iWrite)
                db_ses.add(prvlgTmp)
        else:
            if (0 == iRead and 0 == iWrite):
                db_ses.query(tables.PrivilegeProject). \
                    filter(tables.PrivilegeProject.project_id == iProjectId). \
                    filter(tables.PrivilegeProject.user_id == iUserId).delete()
            else:
                db_ses.query(tables.PrivilegeProject). \
                    filter(tables.PrivilegeProject.project_id == iProjectId). \
                    filter(tables.PrivilegeProject.user_id == iUserId).update({"read": iRead, "write": iWrite})
    return


def SelectSetPrivilege(iUserId):
    """
    @note 获取指定用户的权限
    @param iUserId:用户ID
    @return: 分组及权限（字典）列表
    """
    lstResult = []
    with GetSession() as db_ses:
        lstRcd = db_ses.query(tables.Set, tables.PrivilegeSet). \
            outerjoin(tables.PrivilegeSet,
                      and_(tables.PrivilegeSet.set_id == tables.Set.id,
                           tables.PrivilegeSet.user_id == iUserId)).order_by(tables.Set.id.desc()).all()

        if (None == lstRcd or 0 == len(lstRcd)):
            logger.info("can't find user %s server set privilege" % (iUserId))
            return None

        for srv_set, privilege in lstRcd:
            if (None == privilege):
                dictPrivilege = {"set_id": srv_set.id,
                                 "set_name": srv_set.name,
                                 "init": 0,
                                 "merge": 0,
                                 "upgrade": 0,
                                 "reboot": 0}
            else:
                dictPrivilege = {"set_id": srv_set.id,
                                 "set_name": srv_set.name,
                                 "init": privilege.init,
                                 "merge": privilege.merge,
                                 "upgrade": privilege.upgrade,
                                 "reboot": privilege.reboot}
            lstResult.append(dictPrivilege)
    return lstResult


def SelectSetPrivilegeBySet(strSetName, iUserId):
    """
    @note 获取指定用户的权限
    @param iUserId:用户ID
    @return: 分组及权限（字典）列表
    """
    with GetSession() as db_ses:
        rcdTmp = db_ses.query(tables.PrivilegeSet). \
            filter(tables.Set.id == tables.PrivilegeSet.set_id). \
            filter(tables.PrivilegeSet.user_id == iUserId). \
            filter(tables.Set.name == strSetName).first()
        if (None == rcdTmp):
            return None
        else:
            dictPrivilege = {"set_id": rcdTmp.set_id,
                             "user_id": rcdTmp.user_id,
                             "init": rcdTmp.init,
                             "merge": rcdTmp.merge,
                             "upgrade": rcdTmp.upgrade,
                             "reboot": rcdTmp.reboot}
            return dictPrivilege


def UpdateSetPrivilege(iSetId, iUserId, iInit, iMerge, iUpgrade, iReboot):
    """
    @note 修改指定用户对指定分组的权限
    @param iServerId：主机ID
    @param iSetId:操作集ID
    @param iInit:开服（1=有，0=无）
    @param iMerge:合服（1=有，0=无）
    @param iUpgrade:更新（1=有，0=无）
    @param iReboot:维护（1=有，0=无）
    @return:
    """
    with GetSession() as db_ses:
        rcdTmp = db_ses.query(tables.PrivilegeSet). \
            filter(tables.PrivilegeSet.set_id == iSetId). \
            filter(tables.PrivilegeSet.user_id == iUserId).first()
        if (None == rcdTmp):
            if (iInit + iMerge + iUpgrade + iReboot > 0):
                prvlgTmp = tables.PrivilegeSet(set_id=iSetId,
                                               user_id=iUserId,
                                               init=iInit,
                                               merge=iMerge,
                                               upgrade=iUpgrade,
                                               reboot=iReboot)
                db_ses.add(prvlgTmp)
        else:
            if (iInit + iMerge + iUpgrade + iReboot <= 0):
                db_ses.query(tables.PrivilegeSet). \
                    filter(tables.PrivilegeSet.set_id == iSetId). \
                    filter(tables.PrivilegeSet.user_id == iUserId).delete()
            else:
                db_ses.query(tables.PrivilegeSet). \
                    filter(tables.PrivilegeSet.set_id == iSetId). \
                    filter(tables.PrivilegeSet.user_id == iUserId). \
                    update({"init": iInit, "merge": iMerge, "upgrade": iUpgrade, "reboot": iReboot})
    return True


def InsertReturn(strJobId, strMinionId, strFun, strOperationId, iUserId, iProjectId, iSetId, strCurrentTime,
                 strAction=None):
    """
    @note 添加salt job记录
    @param strJobId：salt job ID
    @param strMinionId:对象主机内网IP
    @param strFun:执行的命令/脚本名称
    @param strOperationId:本次操作ID
    @param iUserId:操作员ID
    @return:
    """
    with GetSession() as db_ses:
        insReturn = tables.SaltReturns(job_id=strJobId,
                                       minion_id=strMinionId,
                                       fun=strFun,
                                       success='',
                                       ret='',
                                       full_ret='',
                                       operation_id=strOperationId,
                                       user_id=iUserId,
                                       project_id=iProjectId,
                                       set_id=iSetId,
                                       start_time=strCurrentTime,
                                       action=strAction)
        db_ses.add(insReturn)
    return


def SelectReturnByOpId(strOperationId):
    """
    @note 获取某次操作的结果
    @param strOperationId:本次操作ID
    @return: 操作结果（字典）列表
    """
    lstResult = []
    with GetSession() as db_ses:
        # 以输入的operation_id为索引查找匹配的salt job 结果
        lstReturn = db_ses.query(tables.SaltReturns).filter(tables.SaltReturns.operation_id == strOperationId).all()
        logger.info("%s job found" % len(lstReturn))
        for rcdReturn in lstReturn:
            #如果还没有结果,显示为等待状态
            if ("" == rcdReturn.full_ret or "" == rcdReturn.success or "" == rcdReturn.ret):
                dictResult = {"ip_in": rcdReturn.minion_id,
                              "fun": rcdReturn.fun,
                              "success": "pending",
                              "return": "pending",
                              "retcode": "0",
                              "jid": rcdReturn.job_id,
                              "start_time": rcdReturn.start_time,
                              "alter_time": rcdReturn.alter_time}
                lstResult.append(dictResult)
                continue

            #从full_ret字段中解析retcode
            dictFullRet = json.loads(rcdReturn.full_ret, strict=False)
            #if("retcode" in dictFullRet):
            if (dictFullRet <> 0 and ("retcode" in dictFullRet)):
                strRetCode = dictFullRet["retcode"]
            else:
                strRetCode = "None"

            #将查找到的信息生成结果列表
            dictResult = {"ip_in": rcdReturn.minion_id,
                          "fun": rcdReturn.fun,
                          "success": rcdReturn.success,
                          "return": rcdReturn.ret,
                          "retcode": strRetCode,
                          "jid": rcdReturn.job_id,
                          "start_time": rcdReturn.start_time,
                          "alter_time": rcdReturn.alter_time}

            lstResult.append(dictResult)
        logger.info("%s job return" % len(lstResult))
    return lstResult


def SelectOperation():
    """
    @note 获取全部操作历史记录
    @return: 操作历史ID（字符串）列表
    """
    tb = tables.SaltReturns
    with GetSession() as db_ses:
        # 在数据库中查找所有操作的记录
        lstReturn = db_ses.query(tb.operation_id, tb.project_id, tb.set_id, tb.user_id, tb.start_time,
                                 tb.action).distinct().order_by(tables.SaltReturns.start_time.desc()).all()
        if (None == lstReturn or 0 == len(lstReturn)):
            return None

        #将查找到的信息生成结果列表
        lstOperation = []
        for rcdReturn in lstReturn:
            dictTmp = {"operation_id": rcdReturn.operation_id,
                       "project_id": rcdReturn.project_id,
                       "set_id": rcdReturn.set_id,
                       "start_time": rcdReturn.start_time,
                       "user_id": rcdReturn.user_id,
                       "action": rcdReturn.action}
            lstOperation.append(dictTmp)
    return lstOperation


def InsertSet(strName, iProjectId, userId):
    """
    @note 获取全部操作历史记录
    @return: 操作历史ID（字符串）列表
    """
    with GetSession() as db_ses:
        srv_set = tables.Set(name=strName, project_id=iProjectId, create_userid=userId)
        db_ses.add(srv_set)
        db_ses.commit()

        rcdTmp = db_ses.query(tables.Set).filter(tables.Set.name == strName).first()
        if (None == rcdTmp):
            logger.error(
                "insert set failed. set name = %s, project_id = %s, create_userid = %s" % (strName, iProjectId, userId))
            return 0
        iTmp = rcdTmp.id

    return iTmp


def DeleteSet(strName):
    """
    @note 删除指定的操作集
    @param strName 操作集名称
    """
    with GetSession() as db_ses:
        rcdTmp = db_ses.query(tables.Set).filter(tables.Set.name == strName).first()
        if (None == rcdTmp):
            return False

        db_ses.query(tables.Set).filter(tables.Set.name == strName).delete()
        db_ses.query(tables.Action).filter(tables.Action.set_id == rcdTmp.id).delete()
        db_ses.query(tables.PrivilegeSet).filter(tables.PrivilegeSet.set_id == rcdTmp.id).delete()
    return True


def SelectSet(iUserId=0, bVisible=True):
    """
    @note 获取用户有权限访问的操作集列表
    @param iUserId:用户ID
    @param bVisible:是否可见
    @return: 操作集ID 操作集名称（字典）列表
    """
    lstServerSet = []
    with GetSession() as db_ses:
        if (0 == iUserId):
            # 查询所有分组
            for it in db_ses.query(tables.Set).order_by(tables.Set.name).all():
                dictTmp = {"id": it.id, "name": it.name, "project_id": it.project_id}
                lstServerSet.append(dictTmp)
            return lstServerSet

        # 查询当前用户有权限查看的所有分组
        for it in db_ses.query(tables.Set).distinct(). \
                filter(tables.User.id == iUserId). \
                filter(tables.Server.visible == bVisible). \
                filter(tables.Server_Set.server_id == tables.Server.id). \
                filter(tables.Server_Set.set_id == tables.Set.id). \
                filter(tables.PrivilegeSet.set_id == tables.Set.id). \
                filter(tables.PrivilegeSet.user_id == tables.User.id). \
                filter(or_(tables.PrivilegeSet.init == 1,
                           tables.PrivilegeSet.merge == 1,
                           tables.PrivilegeSet.upgrade == 1,
                           tables.PrivilegeSet.reboot == 1)).order_by(tables.Set.name).all():
            dictTmp = {"id": it.id, "name": it.name, "project_id": it.project_id}
            lstServerSet.append(dictTmp)

    if (0 == len(lstServerSet)):
        logger.info("query set by user %s failed" % iUserId)
    return lstServerSet


def SelectSetById(iSetId):
    """
    @note 获取指定ID的操作
    @param iSetId:用户ID
    @return: 操作集名称（字符串）
    """
    with GetSession() as db_ses:
        rcdTmp = db_ses.query(tables.Set).filter(tables.Set.id == iSetId).first()
        if (None == rcdTmp):
            return None
        dictTmp = {"id": rcdTmp.id, "name": rcdTmp.name, "project_id": rcdTmp.project_id}
    return dictTmp


def SelectSetByName(strName):
    """
    @note 获取全部操作历史记录
    @return: 操作历史ID（字符串）列表
    """
    with GetSession() as db_ses:
        rcdTmp = db_ses.query(tables.Set).filter(tables.Set.name == strName).first()
        if (None == rcdTmp):
            return None
        dictTmp = {"id": rcdTmp.id, "name": rcdTmp.name, "project_id": rcdTmp.project_id}
    return dictTmp


def SelectSetByProject(iProjectId):
    """
    @note 获取全部操作历史记录
    @return: 操作历史ID（字符串）列表
    """
    with GetSession() as db_ses:
        lstRcdTmp = db_ses.query(tables.Set).filter(tables.Set.project_id == iProjectId).order_by(
            tables.Set.create_time.desc()).all()
        if (None == lstRcdTmp or 0 == len(lstRcdTmp)):
            return None

        lstServerSet = []
        for rcdTmp in lstRcdTmp:
            dictTmp = {"id": rcdTmp.id,
                       "name": rcdTmp.name,
                       "project_id": rcdTmp.project_id,
                       "create_userid": rcdTmp.create_userid,
                       "create_time": rcdTmp.create_time
                       }
            lstServerSet.append(dictTmp)
    return lstServerSet


def AddServerToSet(iSetId, lstServer):
    """
    @note 关联指定的服务器和操作集
    @param iSetId:用户ID
    @param lstServer:待添加的服务器列表
    @return: 失败返回0  成功返回已关联的服务器数量
    """
    if (0 == iSetId or None == lstServer or 0 == len(lstServer)):
        logger.error("add server to set failed.set id=%s" % iSetId)
        return 0

    iCount = 0
    with GetSession() as db_ses:
        for itServer in lstServer:
            rcdTmp = tables.Server_Set(server_id=itServer["id"], set_id=iSetId)
            db_ses.add(rcdTmp)
            iCount += 1

    return iCount


def InsertAction(strName, strPath, iSetId):
    """
    @note 获取全部操作历史记录
    @return: 操作历史ID（字符串）列表
    """
    with GetSession() as db_ses:
        rcdTmp = db_ses.query(tables.Action).filter(
            and_(tables.Action.name == strName, tables.Action.set_id == iSetId)).first()
        if (rcdTmp != None):
            logger.error("insert action failed. duplicate name or set id.")
            return

        action = tables.Action(name=strName, path=strPath, set_id=iSetId)
        db_ses.add(action)
    return


def DeleteActionBySetId(iSetId):
    """
    @note 删除指定操作集相关的所有操作
    @return: 无
    """
    with GetSession() as db_ses:
        db_ses.query(tables.Action).filter(tables.Action.set_id == iSetId).delete()
    return


def UpdateActionBySetName(strSetName, strActionName, strActionPath):
    """
    @note 更新指定操作集相关的操作
    @return: 无
    """
    with GetSession() as db_ses:
        db_ses.query(tables.Action). \
            filter(tables.Action.set_id == tables.Set.id). \
            filter(tables.Set.name == strSetName). \
            filter(tables.Action.name == strActionName).update({"path": strActionPath})
    return


def SelectActionByName(strSetName, strActionName):
    """
    @note 获取指定名称的操作
    @param strName 操作名称
    @return: 操作（字典）
    """
    with GetSession() as db_ses:
        rcdTmp = db_ses.query(tables.Action). \
            filter(tables.Action.set_id == tables.Set.id). \
            filter(tables.Action.name == strActionName). \
            filter(tables.Set.name == strSetName).first()
        if (None == rcdTmp):
            return None

        dictTmp = {"id": rcdTmp.id, "name": rcdTmp.name, "path": rcdTmp.path, "set_id": rcdTmp.set_id}
    return dictTmp


def SelectActionBySrvSet(strSetName):
    """
    @note 获取指定路径的操作
    @param strName 操作路径
    @return: 操作（字典）
    """
    with GetSession() as db_ses:
        lstRcd = db_ses.query(tables.Action).filter(tables.Action.set_id == tables.Set.id).filter(
            tables.Set.name == strSetName).all()
        if (None == lstRcd or 0 == len(lstRcd)):
            return None

        lstAction = []
        for rcdTmp in lstRcd:
            dictTmp = {"id": rcdTmp.id, "name": rcdTmp.name, "path": rcdTmp.path, "set_id": rcdTmp.set_id}
            lstAction.append(dictTmp)
    return lstAction


def UpdateSaltReturns(strSuccess, strReturn, strFullRet, strAlterTime, strJobId):
    """
    @note 更新salt的返回
    """
    with GetSession() as db_ses:
        try:
            db_ses.query(tables.SaltReturns).filter(tables.SaltReturns.job_id == strJobId). \
                update({"success": strSuccess,
                        "return": strReturn,
                        "full_ret": strFullRet,
                        "alter_time": strAlterTime})
        except Exception, e:
            logger.error("=== UpdateSaltReturns Error : %s - %s " % (strAlterTime, strJobId))
            logger.error(e)
    return


