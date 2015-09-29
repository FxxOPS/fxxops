# -*- coding: utf-8 -*-
'''
Created on 2014年5月26日

@author: root
'''
import time, random
from salt import client
from Database.SeaOpsSqlAlchemy import db_session
from . import logger


def ExecuteScript(iUserId, iProjectId, iSetId, strScript, strSname, lstServer, strAction=None):
    if (0 == iUserId or "" == strScript.strip() or None == lstServer or 0 == len(lstServer)):
        return None

    # 获取当前系统时间
    strOperationId = time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(random.randint(10, 99))
    strCurTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    #如果用户选择执行脚本,指定获取脚本文件的路径
    strSrcPath = "salt://%s" % strScript
    #strDstPath = "/tmp/%s" % strScript
    strDstPath = "/tmp/opsRun-%s/%s" % (iSetId, strSname)

    lstStr = strDstPath.rsplit("/", 1)

    iExecCnt = 0
    local = client.LocalClient()
    for server in lstServer:
        res = local.cmd(server["ip_in"], "cmd.run", ["mkdir %s" % lstStr[0]])

        res = local.cmd(server["ip_in"], "cp.get_file", [strSrcPath, strDstPath])
        if (0 == len(res) or (server["ip_in"] not in res) or False == res[server["ip_in"]] or "" == res[
            server["ip_in"]]):
            logger.error("server %s get script file failed." % server["ip_in"])
            continue

        #在远端修改脚本文件权限
        res = local.cmd(server["ip_in"], "cmd.run", ["chmod a+x %s" % strDstPath])
        if (0 == len(res)):
            logger.error("server %s chmod script file failed." % server["ip_in"])
            continue

        #调用salt.cmd_async以异步方式在远端执行命令/脚本,如果没有正常生成salt job跳过当前主机
        strJobId = local.cmd_async(server["ip_in"], "cmd.run", [strDstPath], ret="seaops")
        if (0 == strJobId):
            logger.error("async cmd run error. server:%s" % server["ip_in"])
            continue

        #将当前salt job相关的信息插入数据库,包括job id\主机salt id\执行的命令\操作标识(operation_id)
        db_session.InsertReturn(strJobId,
                                server["ip_in"],
                                strDstPath,
                                strOperationId,
                                iUserId,
                                iProjectId,
                                iSetId,
                                strCurTime,
                                strAction)
        iExecCnt += 1

    if (0 == iExecCnt):
        return None

    return strOperationId


def ExecuteCmd(iUserId, strCmd, lstServer):
    # 获取当前系统时间
    strOperationId = time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(random.randint(10, 99))
    strCurTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    #如果用户没有输入命令或脚本文件名,返回分组页面
    if strCmd.strip() == "":
        return

    local = client.LocalClient()
    for server in lstServer:
        #调用salt.cmd_async以异步方式在远端执行命令/脚本,如果没有正常生成salt job跳过当前主机
        strJobId = local.cmd_async(server["ip_in"], "cmd.run", [strCmd], ret="seaops")
        if (0 == strJobId):
            logger.error("async cmd run error. server:%s" % server["ip_in"])
            continue

        #将当前salt job相关的信息插入数据库,包括job id\主机salt id\执行的命令\操作标识(operation_id)
        db_session.InsertReturn(strJobId, server["ip_in"], strCmd, strOperationId, iUserId, strCurTime)
    return
