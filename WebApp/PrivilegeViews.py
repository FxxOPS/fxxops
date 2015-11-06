# -*- coding: utf-8 -*-
'''
Created on 2014年5月28日

@author: yuan.gao

@note: 权限管理视图(包括用户列表/用户添加/用户删除/用户赋权)
'''
import time, hashlib
from WebApp import WebApp
from flask import request, redirect, render_template, url_for, flash, session
from Database.SeaOpsSqlAlchemy import db_session, PrivilegeSession, CommonSession
from . import Utils, const
import json
from util.PrivilegeUtil import IsShowPage
from const import *

@WebApp.route('/privilege/', methods=['GET'])
def list_user():
    """
    @note GET方法:显示所用用户列表
    """
    if (False == Utils.IsSessValid()):
        return redirect(url_for("login"))

    bIsAdmin = Utils.IsAdmin()
    if False == bIsAdmin and IsShowPage(session["user_id"], MENU_DIC['UserPrivilege']) == FALSE:
        return redirect("/")

    # 查询全部用户
    lstUser = db_session.SelectUser()
    return render_template("privilege_list_user.html", title="User Management", user_list=lstUser)


@WebApp.route('/privilege/add_user', methods=['GET', 'POST'])
def add_user():
    """
    @note GET方法:显示用户添加页面(用户名/密码)
    @note POST方法:提交用户信息(用户名/密码)
    """
    if (False == Utils.IsSessValid()):
        return redirect(url_for("login"))

    bIsAdmin = Utils.IsAdmin()
    if False == bIsAdmin and IsShowPage(session["user_id"], MENU_DIC['UserPrivilege']) == FALSE:
        return redirect(url_for("/"))

    if (request.method == 'POST'):
        if (request.form["name"] == "" or request.form["name"] == "admin"):
            errMsg = '请输入用户名和密码!!'
            flash(errMsg.decode('utf8'))
            return redirect("/privilege/add_user")

        if (request.form["password"] == "" or len(request.form["password"]) < 5 ):
            errMsg = '密码至少6位!!'
            flash(errMsg.decode('utf8'))
            return redirect("/privilege/add_user")

        # 如果提交的用户名已经存在,不能重复添加
        user = db_session.SelectUserByName(request.form["name"])
        if (user != None):
            errMsg = '用户名已经存在'
            flash(errMsg.decode('utf8'))
            return redirect("/privilege/add_user")

        if ("opadmin" == request.form["type"]):
            iType = const.PRI_OP_ADMIN
        elif ("opsadmin" == request.form["type"]):
            iType = const.PRI_OPS_ADMIN
        elif ("sysadmin" == request.form["type"]):
            iType = const.PRI_SYS_ADMIN
        else:
            return redirect("/privilege/add_user")

        #向数据库中添加用户名/密码()
        strCurTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        password = hashlib.md5(
            hashlib.md5("%s-%s" % (request.form["password"], strCurTime)).hexdigest()).hexdigest().upper()

        user_id = db_session.InsertUser(request.form["name"], password, iType, strCurTime)
        PrivilegeSession.InsertNewUserPrivilege(user_id[0])
        return redirect("/privilege")

    return render_template("privilege_add_user.html", title="Add User")


@WebApp.route('/privilege/del_user', methods=['POST'])
def del_user():
    """
    @note GET方法:显示用户列表
    @note POST方法:提交待删除用户ID
    """
    if (False == Utils.IsSessValid()):
        return redirect(url_for("login"))

    bIsAdmin = Utils.IsAdmin()
    if False == bIsAdmin and IsShowPage(session["user_id"], MENU_DIC['UserPrivilege']) == FALSE:
        return redirect(url_for("/"))

    for tmp in request.form:
        db_session.DeleteUser(tmp)
    return redirect("/privilege")


@WebApp.route('/privilege/<user_id>', methods=['GET', 'POST'])
def empower_user(user_id):
    """
    @note GET方法:显示"user_id"指定的用户的权限列表
    @note POST方法:提交权限表单
    """
    if (False == Utils.IsSessValid()):
        return redirect(url_for("login"))

    # 查询当前用户是否有Admin权限,如果没有,不能进行用户管理
    bIsAdmin = Utils.IsAdmin()
    if False == bIsAdmin and IsShowPage(session["user_id"], MENU_DIC['UserPrivilege']) == FALSE:
        return redirect("/")

    #以用户ID为索引查找指定的用户,如果找不到用户,返回根页面
    dictUser = db_session.SelectUserById(user_id)
    if (None == dictUser):
        return redirect("/error/%s" % "no user exist.")

    #从数据库中查找指定用户的权限
    lstProjectPrivilege = db_session.SelectProjectPrivilege(user_id)
    lstSetPrivilege = db_session.SelectSetPrivilege(user_id)


    if (request.method == 'GET'):
        menu_list = PrivilegeSession.SelectMenuProjectPrivilege(user_id)
        return render_template("privilege_empower_user.html",
                               title="User Privilege",
                               user_id=user_id,
                               user_name=dictUser["name"],
                               project_list=lstProjectPrivilege,
                               set_list=lstSetPrivilege,
                               menu_list=menu_list)
    else:
        datas = json.loads(request.form['data'])
        strMenuId = datas['id']

        PrivilegeSession.UpdateUserPrivilege(user_id, strMenuId, datas['detail'])

        # return redirect("/privilege/%s" % user_id)
        return '%s' % json.dumps("ok")