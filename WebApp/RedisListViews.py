# -*- coding: utf-8 -*-
__author__ = 'Abbott'

from . import WebApp
from . import logger
from flask import request, redirect, render_template, session, url_for, send_from_directory
from Database.SeaOpsSqlAlchemy import RedisSession, CommonSession
from Utils import IsSessValid, getFirstPY
from util.RedisUtil import run_redis
from util.PrivilegeUtil import IsShowPage

from const import *
import os

@WebApp.route('/redis/')
def redis_info():
    """
    @note redis执行信息返回前台
    :return:
    """
    if (False == IsSessValid()):
        return redirect(url_for("login"))

    if IsShowPage(session["user_id"], MENU_DIC['Redis']) == FALSE:
        return redirect("/")

    function_privilege = IsShowPage(session["user_id"], MENU_DIC['Redis'], 'priv')

    redis_list = RedisSession.SelectRedisInfo(session["user_id"])

    return render_template("redis/redis_info.html", title='Redis', redis_list=redis_list, function_privilege=function_privilege)

@WebApp.route('/redis/add/<ProjectName>/', methods=['GET', 'POST'])
def redis_add(ProjectName):
    """
    @note redis添加信息提交到后台并插入数据库
    @note Post方法: 页面信息提交到后台
    :param ProjectName:
    :return:
    """
    if (False == IsSessValid()):
        return redirect(url_for("login"))

    if IsShowPage(session["user_id"], MENU_DIC['Redis']) == FALSE:
        return redirect("/")

    project_keys_list = CommonSession.SelectProject('PrjKeysList')
    print project_keys_list, "++"

    if ProjectName in project_keys_list:
        if request.method == 'POST':
            command_list = request.values.getlist('command')
            redisdownloadpath, redisfilename = run_redis(command_list)
            RedisSession.InsertRedisInfo(ProjectName, ';'.join(command_list), session["user_id"], redisdownloadpath, redisfilename)
            return redirect("/redis/")
        else:
            return render_template("redis/redis_add.html", redis_project=ProjectName)


@WebApp.route("/redis/download/<filename>")
def downloader(filename):
    """
    @note redis结果文件下载路径
    :param filename:
    :return:
    """
    if (False == IsSessValid()):
        return redirect(url_for("login"))

    if IsShowPage(session["user_id"], MENU_DIC['Redis']) == FALSE:
        return redirect("/")

    downloadpath = os.path.join(WebApp.root_path, REDIS_DOWNLOAD_PATH)
    return send_from_directory(downloadpath, filename, as_attachment=True)