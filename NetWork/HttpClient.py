# -*- coding: utf-8 -*-
'''
Created on 2014年5月26日

@author: yuan.gao

@note: 通过http接口获取主机信息,保存在本地数据库中
'''

from httplib import HTTPConnection
from Database import SeaOpsMySQLdb
from .import logger
import time

def GetServerList():
    """
    @note 通过http接口获取主机信息字符串,并整理为字典列表结构
    """
    try:
        httpClient = HTTPConnection('server.yw.rrgdev.com', 80)
        httpClient.request('GET', '/seasia.py')
        response = httpClient.getresponse()
        if(404 == response.status):
            return None

        s = response.read()
        s = s.lstrip("{")
        s = s.rstrip("\n")
        s = s.rstrip("}")
        s = s.strip("\n")

        lstStr = s.split("\n")
        lstServer = []
        for strTmp in lstStr:
            if(0 == len(strTmp)):
                logger.error("invalid server information string")
                continue;

            strTmp = strTmp.rstrip(",")
            dictTmp = eval(strTmp)
            if(len(dictTmp) < 14):
                logger.error("invalid para num in server information string")
                continue
            lstServer.append(dictTmp)
    except Exception, e:
        logger.error(e)
        return None
    else:
        return lstServer


def ProcServerInfo():
    """
    @note 将http接口获取到的主机信息插入到本地数据库
    """
    uiRet = 0

    #调用GetServerList函数获取主机信息列表
    lstServer = GetServerList()
    if(None == lstServer):
        return 1

    lstServerSqlPara = []
    with SeaOpsMySQLdb.GetCursor() as cur:
        #遍历主机列表
        for dictTmp in lstServer:
            #在数据库中查询当前主机所在的分组是否已经存在,如果已经存在,获取分组ID
            #否则插入分组数据,并获取分组ID
            uiProjectNum = cur.execute(SeaOpsMySQLdb.SQL_SELECT_PROJECT_BY_NAME % dictTmp["group"])
            if(0 == uiProjectNum):
                uiRet = cur.execute(SeaOpsMySQLdb.SQL_INSERT_PROJECT % dictTmp["group"])
                if(0 == uiRet):
                    logger.error("insert project %s failed" % dictTmp["group"])
                    continue
                cur.execute("COMMIT")

                uiRet = cur.execute(SeaOpsMySQLdb.SQL_SELECT_PROJECT_BY_NAME % dictTmp["group"])
                if(0 == uiRet):
                    logger.error("insert project %s failed" % dictTmp["group"])
                    continue
                result = cur.fetchone()
                dictTmp["group"] = result[0]
            else:
                result = cur.fetchone()
                dictTmp["group"] = result[0]

            tplPara = (dictTmp["Id"],
                       dictTmp["domain"],
                       dictTmp["status"],
                       dictTmp["ip_ex"],
                       dictTmp["ip_in"],
                       dictTmp["host_ip"],
                       dictTmp["group"],
                       dictTmp["idc"],
                       dictTmp["usages"],
                       dictTmp["os"],
                       dictTmp["cpu"],
                       dictTmp["memory"],
                       dictTmp["disk"],
                       dictTmp["pool"])
            lstServerSqlPara.append(tplPara)

        #插入主机信息到数据库
        cur.executemany(SeaOpsMySQLdb.SQL_INSERT_SERVER, lstServerSqlPara)
        cur.execute("COMMIT")

        count = cur.execute(SeaOpsMySQLdb.SQL_SELECT_SERVER_ORDER_BY_PROJECT)

        print "-- update not exists server info: ",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        results = cur.fetchall()
        #比较HTTP接口获取到的主机列表和本地数据库中保存的主机列表,如果在本地库中存在,接口获取到的列表中不存在,
        #认为该主机已停机,将其visible字段置为0
        for r in results:
            bIsFound = False
            for tplPara in lstServerSqlPara:
                if(r[0] is None or tplPara[0] == long(r[0])):
                    bIsFound = True
                    break

            if(False == bIsFound):
                count = cur.execute(SeaOpsMySQLdb.SQL_UPDATE_SERVER_VISIBLE_BY_ID % r[0])
                cur.execute("COMMIT")
                print "         update to invisible id : ",r[0]
    return uiRet

