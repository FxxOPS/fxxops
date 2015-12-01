# -*- coding: utf-8 -*-
"""
Created on 2014.04.23

@author: yuan.gao

@note: Web应用模块初始化
"""

"""
1.生成web应用实例，制定静态文件路径
2.指定secret_key
"""
from ConfigParser import ConfigParser
from . import config
from NetWork.EventLog2db import EventThreadRun

config = ConfigParser()
lstFile = config.read("config.ini")
if ("config.ini" in lstFile):
    config.SCRIPT_PATH = config.get("FILE", "ShellScriptPath")
    config.LOG_PATH = config.get("LOGGER", "Path")

import logging

logger = logging.getLogger("ServerListLogger")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(config.LOG_PATH)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s-%(funcName)s] %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

from flask import Flask

WebApp = Flask(__name__, static_folder="../resources")
WebApp.secret_key = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"

logger.info("service start")

# 启动Event to Salt Returner 的线程
#EventThreadRun()

"""
导入页面模块
"""
from . import LoginViews
from . import PrivilegeViews
from . import OperationViews
from . import ServerListViews
from . import DomainListViews
from .util import DomainFilters
from . import MySQLDigest
from . import RedisListViews
from . import config
from . import IndexViews
from . import OpDomainListViews
from . import const
