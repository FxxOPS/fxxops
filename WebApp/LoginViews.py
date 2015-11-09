# -*- coding: utf-8 -*-
__author__ = 'Abbott'
import time, hashlib
from flask import request, flash, redirect, render_template, session, url_for
from . import WebApp
from forms import LoginForm, PasswordForm
from Database.SeaOpsSqlAlchemy import db_session, PrivilegeSession, CommonSession
from Utils import IsSessValid
from util import PrivilegeUtil



@WebApp.route('/login', methods = ['GET', 'POST'])
def login():
    """
    @note GET方法:显示用户登录页面
    @note POST方法:提交用户名/密码进行登录验证
    """

    #生成登录表单对象
    form = LoginForm(request.form)
    #如果是POST方法,验证表单提交的数据
    loginErr = '用户名或者密码错误'
    if (request.method == "POST" and form.validate()):
        #根据用户名在数据库中查找用户信息
        dictUser = db_session.SelectUserByName(form.strUser.data)
        if (None == dictUser):
            flash(loginErr.decode('utf8'))
            return redirect(url_for('login'))

        #判断数据库中保存的用户密码和页面提交的密码是否相同
        strCtime = dictUser["create_time"].strftime("%Y%m%d%H%M%S")
        inputPass = hashlib.md5(hashlib.md5("%s-%s" % (form.strPassword.data, strCtime)).hexdigest()).hexdigest().upper()
        if(dictUser["password"] != inputPass):
            flash(loginErr.decode('utf8'))
            return redirect(url_for('login'))

        # menupriv_list = PrivilegeSession.SelectMenuPrivilege(dictUser["id"])
        menu_priv_list = PrivilegeSession.SelectMenuProjectPrivilege(dictUser["id"])

        lev1_list, lev2_list = PrivilegeUtil.BuiltPageMenu(menu_priv_list)

        prj_dic = CommonSession.SelectProject('PrjNameDic')
        lstProject = db_session.SelectProject(dictUser["id"], True)
        lstSet = db_session.SelectSet(dictUser["id"], True)

        #在session中保存用户ID和用户名
        session['user_id'] = dictUser["id"]
        session['user_name'] = dictUser["name"]
        session["user_type"] = dictUser["type"]
        session["last_time"] = time.time()
        session["project_list"] = lstProject
        session["project_dic"] = prj_dic
        session["set_list"] = lstSet
        # session["menu_priv"] = menupriv_list
        session["menu_priv_list"] = menu_priv_list
        session["lev1_list"] = lev1_list
        session["lev2_list"] = lev2_list
        if 'referUrl' in session:
            return redirect(session["referUrl"])
        else:
            return redirect(url_for('index'))

    return render_template('login.html', title='Login', form=form)



@WebApp.route('/logout')
def logout():
    """
    @note GET方法:用户退出,清理session中的用户名/用户ID,重定向到登录页面
    """
    # remove the user_id from the session if it's there
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop("user_type", None)
    session.pop('last_time', None)
    session.pop("server_list", None)
    session.pop('project_list', None)
    session.pop("set_list", None)
    session.pop("referUrl", None)
    session.pop("menu_priv", None)
    session.pop("menu_priv_list", None)
    session.pop("lev1_list", None)
    session.pop("lev2_list", None)

    return redirect(url_for('login'))
