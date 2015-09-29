# -*- coding: utf-8 -*-
'''
Created on 2014年5月30日

@author: yuan.gao

@note: 操作视图(远程执行命令或脚本)
'''
import time, random
from flask import request, redirect, render_template, session, url_for
from salt import client
from Database.SeaOpsSqlAlchemy import db_session
from FileSystem import SeaOpsFile
from NetWork import SaltMaster
from . import WebApp, logger, config, Utils


@WebApp.route('/project/<project_name>/operate', methods=['POST', 'GET'])
def operate_server_list(project_name):
    """
    @note GET方法:显示"project_name"参数指定的组中被选中的主机
    @note POST方法:在选定的主机上执行命令或脚本
    @param project_name: 组名
    """

    # 如果session中没有当前用户id的记录,转到登录页面
    if (False == Utils.IsSessValid()):
        return redirect(url_for("login"))

    #如果没有session中没有选定的主机列表,或主机列表为空,返回分组页面
    if ("server_list" not in session):
        logger.error("no operate server list found.")
        return redirect("/error/%s" % "no operate server list found.")

    lstOperate = session["server_list"]
    if (None == lstOperate or 0 == len(lstOperate)):
        logger.error("lstOperate operate server list empty.")
        return redirect("/error/%s" % "lstOperate operate server list empty.")

    dictProject = db_session.SelectProjectByName(project_name, session["user_id"], True)
    if (None == dictProject):
        return redirect("/error/%s" % "dictProject operate server list empty.")

    #查找当前用户对指定组的权限,如果没有操作权限,返回分组页面
    dictPrivilege = db_session.SelectPorjectPrivilegeByProject(project_name, session["user_id"])
    if (None == dictPrivilege or 0 == dictPrivilege["write"]):
        logger.error("operation denied.user:%s project:%s." % (session["user_name"], project_name))
        return redirect("/error/%s" % "operation denied.")

    lstServer = []
    dictTmp = db_session.SelectProjectByName(project_name, session["user_id"])
    #dirProject = ("%s-%s" % (dictTmp["id"] , project_name))
    dirProject = "%s" % dictTmp["id"]

    lstFile = SeaOpsFile.ListFile(config.SCRIPT_PATH + dirProject)

    #遍历选定的主机列表
    for server_id in lstOperate:
        #根据主机id查找主机相关信息,包括域名\IP等等
        dictServer = db_session.SelectServerById(server_id, session["user_id"], True)
        if dictServer is None:
            logger.error("dictServer is None!!")
        lstServer.append(dictServer)


    #如果是处理GET方法,生成响应页面
    if (request.method == "GET"):
        return render_template("operate.html",
                               title="Operate Server List",
                               name=project_name,
                               pdir=config.SCRIPT_PATH + dirProject,
                               server_list=lstServer,
                               file_list=lstFile)

    #获取当前系统时间
    strOperationId = time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(random.randint(10, 99))
    strCurTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    #判断用户提交的表单中选择制定脚本或执行命令
    if (request.form["src"] == "script" and request.form["script"] <> ""):
        #如果用户选择执行脚本,指定获取脚本文件的路径
        strSrcPath = "salt://%s/%s" % (dirProject, request.form["script"])
        strDstPath = "/tmp/%s" % request.form["script"]
        strCmd = strDstPath
    else:
        if ("command" in request.form):
            strCmd = request.form["command"]
        if ('=OK=' not in strCmd):
            strCmd = strCmd + " && echo =OK="

    #如果用户没有输入命令或脚本文件名,返回分组页面
    if strCmd.strip() == "":
        return redirect("/error/%s" % "no command or script file name.")

    logger.info("%s server in list" % len(lstServer))
    local = client.LocalClient()
    for server in lstServer:
        #如果用户选择执行脚本,首先使用salt.cp.get_file将脚本文件传送到远端主机
        if (request.form["src"] == "script"):
            res = local.cmd(server["ip_in"], "cp.get_file", [strSrcPath, strDstPath])
            if (0 == len(res)):
                logger.error("server %s get script file failed." % server["ip_in"])
                continue
            #在远端修改脚本文件权限
            res = local.cmd(server["ip_in"], "cmd.run", ["chmod a+x %s" % strDstPath])
            if (0 == len(res)):
                logger.error("server %s chmod script file failed." % server["ip_in"])
                continue

        #调用salt.cmd_async以异步方式在远端执行命令/脚本,如果没有正常生成salt job跳过当前主机
        logger.info("async cmd run: %s on server: %s" % (strCmd, server["ip_in"]))
        strJobId = local.cmd_async(server["ip_in"], "cmd.run", [strCmd])
        if (0 == strJobId):
            logger.error("async cmd run error. server:%s" % server["ip_in"])
            continue

        #将当前salt job相关的信息插入数据库,包括job id\主机salt id\执行的命令\操作标识(operation_id)
        db_session.InsertReturn(strJobId,
                                server["ip_in"],
                                strCmd,
                                strOperationId,
                                session["user_id"],
                                dictProject["id"],
                                0,
                                strCurTime)

    time.sleep(1)
    return redirect("/operation/result/%s/%s/%s" % (strOperationId, session["user_name"], dictProject["name"]))


@WebApp.route('/operation/result/<operation_id>/<op_user>/<p_name>', methods=['GET'])
def show_operation_result(operation_id, op_user, p_name):
    """
    @note GET方法:显示"operation_id"指定的操作的执行结果
    @param operation_id: 操作ID,某一次操作的唯一标识
    """
    # 如果session中没有当前用户id的记录,转到登录页面
    if (False == Utils.IsSessValid()):
        return redirect(url_for("login"))

    lstResult = db_session.SelectReturnByOpId(operation_id)
    return render_template("operation_result.html",
                           title="Operate Result List",
                           operation_id=operation_id,
                           op_user=op_user,
                           p_name=p_name,
                           result_list=lstResult)


@WebApp.route('/operation/history/', methods=['GET'])
def show_operation_history_list():
    """
    @note GET方法:显示平台上所执行过的所有操作列表
    """
    # 如果session中没有当前用户id的记录,转到登录页面
    if (False == Utils.IsSessValid()):
        return redirect(url_for("login"))

    lstOperation = db_session.SelectOperation()
    try:
        for itOperation in lstOperation:
            dictUser = db_session.SelectUserById(itOperation["user_id"])
            itOperation["user_id"] = dictUser["name"]

            dictProject = db_session.SelectProjectByID(itOperation["project_id"])
            itOperation["project_id"] = dictProject["name"]

            if (0 == itOperation["set_id"]):
                itOperation["set_id"] = ""
            else:
                dictSet = db_session.SelectSetById(itOperation["set_id"])
                if dictSet is None:
                    itOperation["set_id"] = ""
                else:
                    itOperation["set_id"] = dictSet["name"]


    except Exception, e:
        logger.error(e)
        return None
    return render_template("operation_history_list.html", title="Operation Histroy List", operation_list=lstOperation)


@WebApp.route("/project/<project_name>/set/create", methods=["POST", "GET"])
def create_srv_set(project_name):
    """
    @note GET方法:显示创建操作集页面
          POST方法:创建操作集
    @param project_name: 项目名称

    必须现创建目录和脚本,如项目名称为test,config.ini中ShellScriptPath=/data/salt/ (必须加最后的"/")
    则:
    先建立目录: /data/salt/test
    开服脚本: /data/salt/test/kaifu.sh
    合服脚本: /data/salt/test/hefu.sh
    更新脚本: /data/salt/test/gengxin.sh
    维护脚本: /data/salt/test/weihu.sh
    """
    # 如果session中没有当前用户id的记录,转到登录页面
    if (False == Utils.IsSessValid()):
        return redirect(url_for("login"))

    #如果没有session中没有选定的主机列表,或主机列表为空,返回分组页面
    if ("server_list" not in session):
        logger.error("no server list for create a server set found.")
        return redirect("/error/%s" % "no server list for create a server set found.")

    lstServerId = session["server_list"]
    if (None == lstServerId or 0 == len(lstServerId)):
        logger.error("server list for create a server set is empty.")
        return redirect("/error/%s" % "server list for create a server set is empty.")

    #查找当前用户对指定组的权限,如果没有操作权限,返回分组页面
    dictPrivilege = db_session.SelectPorjectPrivilegeByProject(project_name, session["user_id"])
    if (None == dictPrivilege or 0 == dictPrivilege["write"]):
        logger.error("create server set denied.user:%s, project_name:%s" % (session["user_name"], project_name))
        return redirect("/error/%s" % "create server set denied.")

    lstServer = []
    for server_id in lstServerId:
        #根据主机id查找主机相关信息,包括域名\IP等等
        dictServer = db_session.SelectServerById(server_id, session["user_id"], True)
        lstServer.append(dictServer)

    dictTmp = db_session.SelectProjectByName(project_name, session["user_id"])
    #dirProject = ("%s-%s" % (dictTmp["id"] , project_name))
    dirProject = "%s" % dictTmp["id"]

    lstFile = SeaOpsFile.ListFile(config.SCRIPT_PATH + dirProject)
    if (None == lstFile):
        logger.info("no script file in project %s folder." % project_name)

    if (request.method == "GET"):
        return render_template("srv_set.html", title="Create", pname=project_name, pdir=config.SCRIPT_PATH + dirProject,
                               file_list=lstFile, server_list=lstServer)

    if ("name" not in request.form or request.form["name"].strip() == ""):
        return redirect("/error/%s" % "no ops set name.")

    dictProject = db_session.SelectProjectByName(project_name, session["user_id"])
    if (None == dictProject):
        return redirect("/error/%s" % "have no Project, create server set denied.")

    dictServerSet = db_session.SelectSetByName(request.form["name"])
    if (dictServerSet != None):
        return redirect("/error/%s" % "set name is existed.")

    iSetId = db_session.InsertSet(request.form["name"], dictProject["id"], session["user_id"])
    if (0 == iSetId):
        return redirect("/error/%s" % "insert set fail.")

    iRet = db_session.AddServerToSet(iSetId, lstServer)
    if (iRet <= 0):
        return redirect("/error/%s" % "add server to set fail.")

    db_session.InsertAction(u"开服", request.form["init"], iSetId)
    db_session.InsertAction(u"合服", request.form["merge"], iSetId)
    db_session.InsertAction(u"更新", request.form["upgrade"], iSetId)
    db_session.InsertAction(u"维护", request.form["reboot"], iSetId)

    # add privilege
    dictSet = db_session.SelectSetByName(request.form["name"])
    iInit = 1 if request.form["init"] else 0
    iMerge = 1 if request.form["merge"] else 0
    iUpgrade = 1 if request.form["upgrade"] else 0
    iReboot = 1 if request.form["reboot"] else 0

    iPriv = db_session.UpdateSetPrivilege(dictSet["id"], session['user_id'], iInit, iMerge, iUpgrade, iReboot)
    logger.info(iPriv)
    #if (iPriv <> 1):
    #    return redirect("/error/%s" % "add set privilege fail.")

    return redirect("/project/%s/srv_set" % project_name)


@WebApp.route("/project/<project_name>/srv_set", methods=["GET"])
def show_srv_set_list(project_name):
    """
    @note GET方法:显示项目操作集
    @param project_name: 项目名称
    """
    # 如果session中没有当前用户id的记录,转到登录页面
    if (False == Utils.IsSessValid()):
        return redirect(url_for("login"))

    #查找当前用户对指定组的权限,如果没有操作权限,返回分组页面
    dictPrivilege = db_session.SelectPorjectPrivilegeByProject(project_name, session["user_id"])
    if (None == dictPrivilege or 0 == dictPrivilege["write"]):
        logger.error("create server set denied.user:%s, project_name:%s" % (session["user_name"], project_name))
        return redirect("/error/%s" % "create server set denied.")

    dictProject = db_session.SelectProjectByName(project_name, session["user_id"])
    if (None == dictProject):
        return redirect("/error/%s" % "have no Project.")

    lstServerSet = db_session.SelectSetByProject(dictProject["id"])
    return render_template("srv_set_list.html", title="Server Set List", project_name=project_name,
                           server_set_list=lstServerSet)


@WebApp.route("/project/<project_name>/srv_set/<srv_set_name>", methods=["POST", "GET"])
def show_srv_set(project_name, srv_set_name):
    """
    @note GET方法:显示项目操作集
    @param project_name: 项目名称
    """
    # 如果session中没有当前用户id的记录,转到登录页面
    if (False == Utils.IsSessValid()):
        return redirect(url_for("login"))

    #查找当前用户对指定组的权限,如果没有操作权限,返回分组页面
    dictPrivilege = db_session.SelectPorjectPrivilegeByProject(project_name, session["user_id"])
    if (None == dictPrivilege or 0 == dictPrivilege["write"]):
        logger.error("create server set denied.user:%s, project_name:%s" % (session["user_name"], project_name))
        return redirect("/error/%s" % "create server set denied.")

    if ("GET" == request.method):
        lstAction = db_session.SelectActionBySrvSet(srv_set_name)
        if (None == lstAction):
            return redirect("/error/%s" % "have no Action.")

        dictAction = {}
        for actTmp in lstAction:
            if (u"开服" == actTmp["name"]):
                dictAction["init"] = actTmp["path"]
            elif (u"合服" == actTmp["name"]):
                dictAction["merge"] = actTmp["path"]
            elif (u"更新" == actTmp["name"]):
                dictAction["upgrade"] = actTmp["path"]
            elif (u"维护" == actTmp["name"]):
                dictAction["reboot"] = actTmp["path"]
            else:
                break

        set_id = actTmp["set_id"]
        lstServerSet = db_session.SelectServerBySet(srv_set_name)
        if (None == lstServerSet):
            return redirect("/error/%s" % "have no ServerSet.")

        dictTmp = db_session.SelectProjectByName(project_name, session["user_id"])
        #dirProject = ("%s-%s" % (dictTmp["id"] , project_name))
        dirProject = "%s" % dictTmp["id"]
        lstFile = SeaOpsFile.ListFile(config.SCRIPT_PATH + dirProject)

        return render_template("srv_set.html",
                               title="Server Set",
                               pname=project_name,
                               name=srv_set_name,
                               pdir=config.SCRIPT_PATH + dirProject,
                               setid=set_id,
                               actions=dictAction,
                               file_list=lstFile,
                               server_list=lstServerSet)
    else:
        for k, v in request.form.iteritems():
            if (k == "init"):
                strActionName = "开服"
                iInit = 0 if len(v) == 0 else 1
            elif (k == "merge"):
                strActionName = "合服"
                iMerge = 0 if len(v) == 0 else 1
            elif (k == "upgrade"):
                strActionName = "更新"
                iUpgrade = 0 if len(v) == 0 else 1
            elif (k == "reboot"):
                strActionName = "维护"
                iReboot = 0 if len(v) == 0 else 1
            else:
                continue
            db_session.UpdateActionBySetName(srv_set_name, strActionName, v)
        db_session.UpdateSetPrivilege(request.form['set_id'], session['user_id'], iInit, iMerge, iUpgrade, iReboot)
        return redirect("/project/%s/srv_set" % project_name)


@WebApp.route("/set/<srv_set_name>/execute", methods=["GET", "POST"])
def execute_srv_set(srv_set_name):
    """
    @note GET方法:执行操作集
    @param set_name: 操作集名称
    """
    # 如果session中没有当前用户id的记录,转到登录页面
    if (False == Utils.IsSessValid()):
        return redirect(url_for("login"))

    #查找当前用户对指定组的权限,如果没有操作权限,返回分组页面
    dictPrivilege = db_session.SelectSetPrivilegeBySet(srv_set_name, session["user_id"])
    if (None == dictPrivilege or (0 == dictPrivilege["init"] and
                                          0 == dictPrivilege["merge"] and
                                          0 == dictPrivilege["upgrade"] and
                                          0 == dictPrivilege["reboot"])):
        return redirect("/error/%s" % "you have not privileges.")

    lstServer = db_session.SelectServerBySet(srv_set_name)
    if (None == lstServer or 0 == len(lstServer)):
        return redirect("/error/%s" % "this set have no server list.")
    lstAction = db_session.SelectActionBySrvSet(srv_set_name)

    dictProject = db_session.SelectProjectBySet(srv_set_name)
    dictAction = {}
    for actTmp in lstAction:
        if (u"开服" == actTmp["name"]):
            dictAction["initPath"] = actTmp["path"]
        elif (u"合服" == actTmp["name"]):
            dictAction["mergePath"] = actTmp["path"]
        elif (u"更新" == actTmp["name"]):
            dictAction["upgradePath"] = actTmp["path"]
        elif (u"维护" == actTmp["name"]):
            dictAction["rebootPath"] = actTmp["path"]
        else:
            break
    if (None == lstAction):
        return redirect("/error/%s" % "have no Action.")

    if (1 == dictPrivilege["init"]):
        dictAction["init"] = 1
    if (1 == dictPrivilege["merge"]):
        dictAction["merge"] = 1
    if (1 == dictPrivilege["upgrade"]):
        dictAction["upgrade"] = 1
    if (1 == dictPrivilege["reboot"]):
        dictAction["reboot"] = 1

    if (request.method == "GET"):
        return render_template("srv_set_execute.html",
                               title="Execute",
                               pname=dictProject["name"],
                               pdir="%s%s" % (config.SCRIPT_PATH, dictProject["id"]),
                               name=srv_set_name,
                               actions=dictAction,
                               server_list=lstServer)
    else:
        if ("type" not in request.form):
            return redirect("/error/%s" % "have no ops type .")

        if (request.form["type"] == "init"):
            strActionName = "开服"
        elif (request.form["type"] == "merge"):
            strActionName = "合服"
        elif (request.form["type"] == "upgrade"):
            strActionName = "更新"
        elif (request.form["type"] == "reboot"):
            strActionName = "维护"
        else:
            logger.error("invalid script selection.")
            return redirect("/error/%s" % "invalid script selection.")

        dictAction = db_session.SelectActionByName(srv_set_name, strActionName)
        if (None == dictAction):
            return redirect("/error/%s" % "have no select action.")

        #strScript = "%s-%s/%s" % (dictProject["id"],dictProject["name"], dictAction["path"])
        strScript = "%s/%s" % (dictProject["id"], dictAction["path"])
        strSname = dictAction["path"]
        strOperationId = SaltMaster.ExecuteScript(session["user_id"],
                                                  dictProject["id"],
                                                  dictPrivilege["set_id"],
                                                  strScript,
                                                  strSname,
                                                  lstServer,
                                                  strActionName)
        if (None == strOperationId):
            return redirect("/error/%s" % "have no operation id.")

    return redirect("/operation/result/%s/%s/%s" % (strOperationId, session["user_name"], dictProject["name"]))


@WebApp.route("/set/<srv_set_name>/delete", methods=["GET"])
def delete_srv_set(srv_set_name):
    """
    @note GET方法:删除项目操作集
    @param set_name: 操作集名称
    """
    # 如果session中没有当前用户id的记录,转到登录页面
    if (False == Utils.IsSessValid()):
        return redirect(url_for("login"))

    #查找当前用户对指定操作集的权限
    dictPrivilege = db_session.SelectSetPrivilegeBySet(srv_set_name, session["user_id"])
    if (None == dictPrivilege or (0 == dictPrivilege["init"] and
                                          0 == dictPrivilege["merge"] and
                                          0 == dictPrivilege["upgrade"] and
                                          0 == dictPrivilege["reboot"])):
        return redirect("/error/%s" % "you have not privileges.")

    lstSet = db_session.SelectSetByName(srv_set_name)
    if (None == lstSet or 0 == len(lstSet)):
        return redirect("/error/%s" % "have no set.")

    res = db_session.DeleteSet(srv_set_name)
    if res == False:
        return redirect("/error/%s" % "DeleteSet fail !!")

    return redirect("/error/%s" % "DeleteSet Success !!")