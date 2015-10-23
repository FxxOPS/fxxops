# -*- coding: utf-8 -*-
'''
Created on 2014年5月26日

@author: yuan.gao

@note: 查询视图(包括主机列表/分组列表/机房列表/指定索引查询等)
'''
import json
import MySQLdb
from flask import request, redirect, render_template, session, url_for
from Database.SeaOpsSqlAlchemy import db_session
from Database.const import *
from . import WebApp, logger
from Utils import IsSessValid, getFirstPY


@WebApp.route('/q', methods=['GET'])
def show_q_result():
    """
    @note GET方法:为指定索引查询的输入框提供自动完成功能
    """
    if (False == IsSessValid()):
        return redirect(url_for("login"))

    req = request.args
    if req is None:
        return
    else:
        SQL_SELECT_Q = """select distinct t.* from (
                        select domain from server where visible = 1 and domain like '%%%s%%' limit 10
                        union all
                        select ip_ex from server where visible = 1 and ip_ex like '%%%s%%' limit 10
                        union all
                        select ip_in from server where visible = 1 and ip_in like '%%%s%%' limit 10
                        union all
                        select host_ip from server where visible = 1 and host_ip like '%%%s%%' limit 10
                        union all
                        select comment from server where visible = 1 and comment like '%%%s%%' limit 10
                        union all
                        select name from project where name like '%%%s%%' limit 10
                        ) t """

        try:
            conn = MySQLdb.connect(host=DB_ADDRESS, user=DB_USER, passwd=DB_PWD, port=DB_PORT, charset=DB_CHAR_SET)
            conn.select_db(DB_DEF)
            cur = conn.cursor()

            term = req.get('term')
            cur.execute(SQL_SELECT_Q % (term, term, term, term, term, term))
            result = cur.fetchall()

            lstResult = []
            for r in result:
                lstResult.append('%s' % r)

        except Exception, e:
            print e
        finally:
            cur.close()
            conn.close()

    return "%s" % json.dumps(lstResult)


@WebApp.route('/search', methods=['POST'])
def show_server_list_search():
    """
    @note POST方法:根据输入的索引查找主机
    """
    if (False == IsSessValid()):
        return redirect(url_for("login"))

    SQL_SELECT_SERVER_BY_USER = """ select distinct t.* from (
                                        (SELECT
                                          server.id,
                                          server.domain,
                                          server.stat,
                                          server.ip_ex,
                                          server.ip_in,
                                          project.name,
                                          server.idc,
                                          server.usages,
                                          server.os,
                                          server.cpu,
                                          server.memory,
                                          server.disk,
                                          server.pool,
                                          server.comment,
                                          server.host_ip,
                                          server.visible
                                          FROM server, prvlg_prj, project, user WHERE
                                          user.id = '%s' AND
                                          project.id = server.project_id AND
                                          prvlg_prj.project_id = project.id AND
                                          prvlg_prj.user_id = user.id AND
                                          prvlg_prj.read = '1' AND
                                          project.name like '%%%s%%'
                                          ORDER BY project.name,server.domain)
                                            union all
                                          (SELECT
                                          server.id,
                                          server.domain,
                                          server.stat,
                                          server.ip_ex,
                                          server.ip_in,
                                          project.name,
                                          server.idc,
                                          server.usages,
                                          server.os,
                                          server.cpu,
                                          server.memory,
                                          server.disk,
                                          server.pool,
                                          server.comment,
                                          server.host_ip,
                                          server.visible
                                          FROM server, prvlg_prj, project, user WHERE
                                          user.id = '%s' AND
                                          server.project_id = project.id AND
                                          prvlg_prj.project_id = project.id AND
                                          prvlg_prj.user_id = user.id AND
                                          prvlg_prj.read = '1' AND
                                          server.domain like '%%%s%%'
                                          ORDER BY project.name,server.domain)
                                            union all
                                          (SELECT
                                          server.id,
                                          server.domain,
                                          server.stat,
                                          server.ip_ex,
                                          server.ip_in,
                                          project.name,
                                          server.idc,
                                          server.usages,
                                          server.os,
                                          server.cpu,
                                          server.memory,
                                          server.disk,
                                          server.pool,
                                          server.comment,
                                          server.host_ip,
                                          server.visible
                                          FROM server, prvlg_prj, project, user WHERE
                                          user.id = '%s' AND
                                          server.project_id = project.id AND
                                          prvlg_prj.project_id = project.id AND
                                          prvlg_prj.user_id = user.id AND
                                          prvlg_prj.read = '1' AND
                                          server.ip_in like '%%%s%%'
                                          ORDER BY project.name,server.domain)
                                            union all
                                          (SELECT
                                          server.id,
                                          server.domain,
                                          server.stat,
                                          server.ip_ex,
                                          server.ip_in,
                                          project.name,
                                          server.idc,
                                          server.usages,
                                          server.os,
                                          server.cpu,
                                          server.memory,
                                          server.disk,
                                          server.pool,
                                          server.comment,
                                          server.host_ip,
                                          server.visible
                                          FROM server, prvlg_prj, project, user WHERE
                                          user.id = '%s' AND
                                          server.project_id = project.id AND
                                          prvlg_prj.project_id = project.id AND
                                          prvlg_prj.user_id = user.id AND
                                          prvlg_prj.read = '1' AND
                                          server.ip_ex like '%%%s%%'
                                          ORDER BY project.name,server.domain)
                                            union all
                                          (SELECT
                                          server.id,
                                          server.domain,
                                          server.stat,
                                          server.ip_ex,
                                          server.ip_in,
                                          project.name,
                                          server.idc,
                                          server.usages,
                                          server.os,
                                          server.cpu,
                                          server.memory,
                                          server.disk,
                                          server.pool,
                                          server.comment,
                                          server.host_ip,
                                          server.visible
                                          FROM server, prvlg_prj, project, user WHERE
                                          user.id = '%s' AND
                                          server.project_id = project.id AND
                                          prvlg_prj.project_id = project.id AND
                                          prvlg_prj.user_id = user.id AND
                                          prvlg_prj.read = '1' AND
                                          server.host_ip like '%%%s%%'
                                          ORDER BY project.name,server.domain)
                                            union all
                                          (SELECT
                                          server.id,
                                          server.domain,
                                          server.stat,
                                          server.ip_ex,
                                          server.ip_in,
                                          project.name,
                                          server.idc,
                                          server.usages,
                                          server.os,
                                          server.cpu,
                                          server.memory,
                                          server.disk,
                                          server.pool,
                                          server.comment,
                                          server.host_ip,
                                          server.visible
                                          FROM server, prvlg_prj, project, user WHERE
                                          user.id = '%s' AND
                                          server.project_id = project.id AND
                                          prvlg_prj.project_id = project.id AND
                                          prvlg_prj.user_id = user.id AND
                                          prvlg_prj.read = '1' AND
                                          server.comment like '%%%s%%'
                                          ORDER BY project.name,server.domain)
                                        )t """

    try:
        conn = MySQLdb.connect(host=DB_ADDRESS, user=DB_USER, passwd=DB_PWD, port=DB_PORT, charset=DB_CHAR_SET)
        conn.select_db(DB_DEF)
        cur = conn.cursor()

        lstProject = []
        lstServer = []

        uid = session["user_id"]
        req = request.form["value"]
        strSql = SQL_SELECT_SERVER_BY_USER % (uid, req, uid, req, uid, req, uid, req, uid, req, uid, req)

        cur.execute(strSql)
        results = cur.fetchall()
        for r in results:
            if (r[5] not in lstProject):
                lstProject.append(r[5])
            lstServer.append(
                {'id': r[0], 'domain': r[1], 'status': r[2], 'ip_ex': r[3], 'ip_in': r[4], 'project': r[5], 'idc': r[6],
                 'usages': r[7], 'os': r[8], 'cpu': r[9], 'memory': r[10], 'disk': r[11], 'pool': r[12],
                 'comment': r[13], 'host_ip': r[14], 'visible': r[15]})
    except Exception, e:
        print e
    finally:
        cur.close()
        conn.close()
    return render_template("result.html", title="search Result", project_list=lstProject, server_list=lstServer,
                           req_text=req)


@WebApp.route('/closed', methods=['GET'])
def show_server_list_closed():
    """
    @note GET方法:显示所有已停机的主机信息
    """
    if (False == IsSessValid()):
        return redirect(url_for("login"))

    lstServer = db_session.SelectServer(session["user_id"], False)
    return render_template("result.html", title="Closed", server_list=lstServer)


@WebApp.route('/project/<strProjectName>', methods=['POST', 'GET'])
def show_server_list_project(strProjectName):
    """
    @note GET方法:显示指定组名的所有主机
    @note POST方法:提交一个选定的主机列表,用于执行命令/脚本
    @param strProjectName: 分组名称
    """
    if (False == IsSessValid()):
        return redirect(url_for("login"))

    if (request.method == "GET"):
        lstServer = db_session.SelectServerByProject(strProjectName, session["user_id"])
        return render_template("result.html", title="Project Server List", type="project", name=strProjectName,
                               server_list=lstServer)
    else:
        lstServerId = []
        for k, v in request.form.iteritems():
            if (k != "op_sel"):
                lstServerId.append(k)

        session.pop("server_list", None)
        session["server_list"] = lstServerId
        if ("0" == request.form["op_sel"]):
            return redirect("/project/%s/operate" % strProjectName)
        else:
            return redirect("/project/%s/set/create" % strProjectName)


@WebApp.route('/idc/<strIdcName>')
def show_server_list_idc(strIdcName):
    """
    @note GET方法:显示指定机房的所有主机
    """
    if (False == IsSessValid()):
        return redirect(url_for("login"))

    lstProject = db_session.SelectProjectByIdc(strIdcName, session["user_id"])
    lstServer = db_session.SelectServerByIdc(strIdcName, session["user_id"])
    return render_template("result.html", title="IDC Server List", type="idc", name=strIdcName, project_list=lstProject,
                           server_list=lstServer)


@WebApp.route('/server/<iServerId>', methods=['GET', 'POST'])
def show_server_info(iServerId):
    """
    @note GET方法:显示指定ID的主机
    @note POST方法:修改指定主机的备注信息
    @param iServerId: 主机ID
    """
    if (False == IsSessValid()):
        return redirect(url_for("login"))

    # 查询当前用户有权限查看的主机信息
    dictServer = db_session.SelectServerById(iServerId, session["user_id"], True)
    if (request.method == 'GET'):
        #查询指定主机的历史备注
        lstComment = db_session.SelectCommentByServer(iServerId)
        return render_template("server_info.html", title='Server Information', comment_list=lstComment,
                               server=dictServer)
    else:
        #查找用户对指定的分组是否有操作权限
        dictPrivilege = db_session.SelectProjectPrivilegeByServer(iServerId, session["user_id"])
        if (None == dictPrivilege or 0 == dictPrivilege["write"]):
            return redirect("/error/%s" % " you have no privilege, update denied.")

        db_session.UpdateComment(iServerId, session["user_id"], request.form["comment"])
        return redirect("/project/%s" % dictServer["project"])

        # @WebApp.route('/pmodify/<iServerId>', methods = ['GET', 'POST'])
        # def