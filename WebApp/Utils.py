# -*- coding: utf-8 -*-
'''
Created on 2014年6月4日

@author: root
'''
import sys,time,json,os
from flask import request, redirect, render_template, session, url_for
from Database.SeaOpsSqlAlchemy import db_session
from . import WebApp,logger

def IsSessValid():
    if("last_time" not in session):
        return False

    fTime = session["last_time"]
    if(time.time() - fTime >= 3600.0):
        session.pop("user_name", None)
        session.pop("user_id", None)
        session.pop("last_time", None)
        if ("q?term" not in request.url and "search" not in request.url ):
            session["referUrl"] = request.url
        return False

    session["last_time"] = time.time()
    return True

def IsAdmin():
    if("user_type" not in session):
        return False

    if(session["user_type"] != 0):
        return False

    return True

def UpdateProjectList(iProjectId, iRead):
    if(0 == iProjectId):
        return

    bIsFound = False
    iPos = 0
    lstProject = session["project_list"]
    for index, dictProject in enumerate(lstProject):
        if(dictProject["id"] == iProjectId):
            bIsFound = True
            iPos = index
            break

    if(0 == iRead):
        if(True == bIsFound):
            del lstProject[iPos]
    elif(1 == iRead):
        if(False == bIsFound):
            dictProject = db_session.SelectProjectByID(iProjectId)
            if(None == dictProject):
                return
            dictTmp = {"id":iProjectId, "name":dictProject["name"]}
            lstProject.append(dictTmp)
    else:
        return

    return

def UpdateServerSetList(iSetId, iInit, iMerge, iUpgrad, iReboot):
    if(0 == iSetId):
        return

    bIsFound = False
    iPos = 0
    lstSet = session["set_list"]
    for index, dictSet in enumerate(lstSet):
        if(dictSet["id"] == iSetId):
            bIsFound = True
            iPos = index
            break

    if(0 == iInit and 0 == iMerge and 0 == iUpgrad and 0 == iReboot):
        if(True == bIsFound):
            del lstSet[iPos]
    else:
        if(False == bIsFound):
            dictSet = db_session.SelectSetById(iSetId)
            if(None == dictSet):
                return
            dictTmp = {"id":iSetId, "name":dictSet["name"]}
            lstSet.append(dictTmp)
    return

@WebApp.route('/error/<errMsg>', methods = ['GET'])
def ErrorMsg(errMsg):

    """
    @note GET方法:显示错误信息
    """
    if(False == IsSessValid()):
        return redirect(url_for("login"))

    try:
        reload(sys)
        sys.setdefaultencoding('utf-8')
        res = errMsg.encode('utf-8')
        if 'Referer' in request.headers:
            ref = request.headers['Referer']
        else:
            ref = "javascript:history.go(-1);"
        return render_template("error.html",title = 'Error',refurl=ref ,err_msg = res)
        #return "%s" % json.dumps(res)
    except Exception, err:
        logger.error(err)

#####
##  拼音
#####

def getFirstPY(word, encoding='utf-8'):
    if isinstance(word, unicode):
        try:
            word = word[0].encode('gbk')
        except:
            return '?'
    elif isinstance(word, str):
        try:
            word = word.decode(encoding)[0].encode('gbk')
        except:
            return '?'

    if len(word) == 1:
        return word
    else:
        asc = ord(word[0])*256 + ord(word[1]) - 65536
        if asc >= -20319 and asc <= -20284:
            return 'A'
        if asc >= -20283 and asc <= -19776:
            return 'B'
        if asc >= -19775 and asc <= -19219:
            return 'C'
        if asc >= -19218 and asc <= -18711:
            return 'D'
        if asc >= -18710 and asc <= -18527:
            return 'E'
        if asc >= -18526 and asc <= -18240:
            return 'F'
        if asc >= -18239 and asc <= -17923:
            return 'G'
        if asc >= -17922 and asc <= -17418:
            return 'H'
        if asc >= -17417 and asc <= -16475:
            return 'J'
        if asc >= -16474 and asc <= -16213:
            return 'K'
        if asc >= -16212 and asc <= -15641:
            return 'L'
        if asc >= -15640 and asc <= -15166:
            return 'M'
        if asc >= -15165 and asc <= -14923:
            return 'N'
        if asc >= -14922 and asc <= -14915:
            return 'O'
        if asc >= -14914 and asc <= -14631:
            return 'P'
        if asc >= -14630 and asc <= -14150:
            return 'Q'
        if asc >= -14149 and asc <= -14091:
            return 'R'
        if asc >= -14090 and asc <= -13119:
            return 'S'
        if asc >= -13118 and asc <= -12839:
            return 'T'
        if asc >= -12838 and asc <= -12557:
            return 'W'
        if asc >= -12556 and asc <= -11848:
            return 'X'
        if asc >= -11847 and asc <= -11056:
            return 'Y'
        if asc >= -11055 and asc <= -10247:
            return 'Z'
        return 'Other'