# -*- coding: utf-8 -*-
__author__ = 'Abbott'

from DbSession import GetSession
from . import tables, logger
from WebApp.config import *

def InsertDomain(strDomainName, strProjectId, strProjectName, strFunctions, strComments):
    """
    @note 主域名信息数据插入Domain表里，并返回domain id
    :param strDomainName:
    :param strProjectId:
    :param strProjectName:
    :param strFunctions:
    :param strComments:
    :return:返回domain id
    """
    with GetSession() as db_ses:
        domain = tables.Domain(domain_name=strDomainName, project_id=strProjectId, project_name=strProjectName,
                               functions=strFunctions, comments=strComments)
        db_ses.add(domain)
        domain_id = db_ses.query(tables.Domain.domain_id).filter(tables.Domain.domain_name == strDomainName).first()
    return domain_id


def InsertSubdomain(pre_id, DicSubdomain):
    """
    @note 子域名信息数据插入Domain表里
    :param pre_id:
    :param DicSubdomain:
    :return:
    """
    with GetSession() as db_ses:
        for k, v in DicSubdomain.items():
            print k, v
            if v:
                subdomain = tables.Domain(domain_name=k, ip_source=v, pre_domain_id=pre_id)
                db_ses.add(subdomain)


def UpdateDomainComments(strDomainId, strComments):
    """
    @note 更新域名Comments
    :param strDomainId:
    :param strComments:
    :return:
    """
    with GetSession() as db_ses:
        db_ses.query(tables.Domain).filter(tables.Domain.domain_id == strDomainId).update({"comments": strComments})


def SelectProjectId(strProjectId):
    """
    @note 查询项目ID
    :param strProjectId:
    :return:项目名字
    """
    with GetSession() as db_ses:
        project_name = db_ses.query(tables.Project.name).filter(tables.Project.id == strProjectId).first()

    return project_name


def SelectDomainId(strDomainName):
    """
    @note 查询域名ID
    :param strDomainName:
    :return:域名ID
    """
    with GetSession() as db_ses:
        domain_id = db_ses.query(tables.Domain.domain_id).filter(tables.Domain.domain_name == strDomainName).first()
    return domain_id


def UpdateDomain(strDomainID, strDomainDic):
    """
    @note 更新域名信息
    :param strDomainID:
    :param strDomainDic:
    :return:
    """
    with GetSession() as db_ses:
        subdomains = db_ses.query(tables.Domain.domain_name).filter(tables.Domain.pre_domain_id == strDomainID).all()
        db_ses.query(tables.Domain).filter(tables.Domain.domain_id == strDomainID).update(
            {"comments": strDomainDic['comments'], "functions": strDomainDic['function']})

        for sub in subdomains:
            db_ses.query(tables.Domain).filter(tables.Domain.pre_domain_id == strDomainID,
                                               tables.Domain.domain_name == sub[0]).update(
                {"ip_source": strDomainDic[sub[0]]})
    return