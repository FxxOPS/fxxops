# -*- coding: utf-8 -*-
'''
Creat on 2015.10.20

__author__ = 'hellsp'

note: index views
'''

import json
import MySQLdb
from flask import request, redirect, render_template, session, url_for
from Database.SeaOpsSqlAlchemy import db_session
from Database.const import *
from . import WebApp, logger
from Utils import IsSessValid, getFirstPY


@WebApp.route('/')
@WebApp.route('/index')
def index():
    titletxt=('常用操作').decode('utf-8')
    # """
    # @note GET方法:显示分组列表/机房列表
    # """
    # if (False == IsSessValid()):
    #     return redirect(url_for("login"))
    #
    # lstProject = db_session.SelectProjectName(session["user_id"], True)
    # lstCode = []
    # for r in lstProject:
    #     strCode = r.split("-")[0]
    #     strCode = "%s-%s" % (getFirstPY(strCode), strCode)
    #     if (strCode not in lstCode):
    #         lstCode.append(strCode)
    #
    # lstSet = db_session.SelectSet(session["user_id"], True)
    # lstIdc = db_session.SelectIdcName(session["user_id"], True)
    # lstServer = db_session.SelectServer(session["user_id"], True)
    return render_template("index.html",
                           title=titletxt)
                           # code_list=lstCode,
                           # project_list=lstProject,
                           # server_list=lstServer,
                           # set_list=lstSet,
                           # idc_list=lstIdc)
