# -*- coding: utf-8 -*-
'''
Created on 2014.05.12

@author: yuan.gao

@note: 文件操作
'''
import os
from . import logger


def IsAllowedExt(strFileName):
    strExt = os.path.splitext(strFileName)[1]
    if (strExt != ".sh"):
        return False
    return True


def MakeDir(strPathName):
    strExt = os.path.splitext(strFileName)[1]
    if (strExt != ".sh"):
        return False
    return True


def ListFile(path=None):
    """
    @note 列出指定的路径中的所有文件
    @param path: 指定的路径
    """
    try:
        if (None == path):
            logger.error("invalid path input")
            return None
        path = path.encode('utf-8')
        if (False == os.path.isdir(path)):
            os.makedirs(path)
            logger.info("create dir : %s" % path)
            return None

        lstRtn = []
        lstFile = os.listdir(path)
        for f in lstFile:
            tmp = os.path.join(path, f)
            if (False == os.path.isfile(tmp)):
                continue
            fExt = os.path.splitext(f)[1]
            if (fExt != ".sh"):
                continue
            lstRtn.append(f)

        if 0 == len(lstRtn):
            logger.error("no script file found in input path")
            return None
    except Exception, err:
        logger.error(err)

    return lstRtn
