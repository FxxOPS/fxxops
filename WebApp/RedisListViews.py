# -*- coding: utf-8 -*-
__author__ = 'Abbott'

from . import WebApp
from . import logger
from flask import request, redirect, render_template, session, url_for, send_from_directory
from Database.SeaOpsSqlAlchemy import db_session
from Database.SeaOpsMySQLdb import mysql_connect
from Utils import IsSessValid, getFirstPY
from util.RedisUtil import run_redis
from config import *
from util.MySQLUtil import MysqlReturnValue

import decimal
import datetime
import os

@WebApp.route('/redis/')
def redis_info():
    if (False == IsSessValid()):
        return redirect(url_for("login"))

    redis_list = db_session.SelectRedisInfo()

    return render_template("redis/redis_info.html", title='Redis', redis_list=redis_list)

@WebApp.route('/redis/add/<ProjectName>/', methods=['GET', 'POST'])
def redis_add(ProjectName):
    if (False == IsSessValid()):
        return redirect(url_for("login"))

    if ProjectName == 'video':
        if request.method == 'POST':
            command_list = request.values.getlist('command')
            redisdownloadpath, redisfilename = run_redis(command_list)
            db_session.InsertRedisInfo(ProjectName, ';'.join(command_list), session["user_id"], redisdownloadpath, redisfilename)
            return redirect("/redis/")
        else:
            return render_template("redis/redis_add.html", redis_project=ProjectName)
    elif ProjectName == 'discuze':
        if request.method == 'POST':
            command_list = request.values.getlist('command')
            redisdownloadpath, redisfilename = run_redis(command_list)
            db_session.InsertRedisInfo(ProjectName, ';'.join(command_list), session["user_id"], redisdownloadpath, redisfilename)
            return redirect("/redis/")
        else:
            return render_template("redis/redis_add.html", redis_project=ProjectName)


@WebApp.route("/redis/download/<filename>")
def downloader(filename):
    downloadpath = os.path.join(WebApp.root_path, REDIS_DOWNLOAD_PATH)
    return send_from_directory(downloadpath, filename, as_attachment=True)