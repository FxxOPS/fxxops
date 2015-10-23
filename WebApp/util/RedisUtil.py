# -*- coding: utf-8 -*-
__author__ = 'Abbott'
import redis
import sys
import uuid
import os
from .. import WebApp
from ..config import *

# REDIS_DOWNLOAD_PATH = 'FileOperate/Redis/Download'


def run_redis(command_list):
    filename = "redis-%s.%s" % (uuid.uuid4(), 'txt')
    print filename
    print WebApp.root_path
    print os.path.join(WebApp.root_path, REDIS_DOWNLOAD_PATH)
    path = os.path.join(WebApp.root_path, REDIS_DOWNLOAD_PATH, filename)
    pool = redis.ConnectionPool(host='10.1.110.24', port=6379)
    r = redis.Redis(connection_pool=pool)
    for command in command_list:

        if command.split()[0] == 'hgetall':
            redis_result = r.hgetall(command.split()[1])
            redis_file(command, redis_result, path, filename)

    return REDIS_DOWNLOAD_PATH, filename


def redis_file(command, result, path, filename):
    # print sql_list,"?????"
    # filename = "redis-%s.%s" % (uuid.uuid4(), 'txt')
    # path = os.path.join(REDIS_PATH, filename)
    f = open(path, 'ab+')

    # print type(sql['result'])
    # print str(sql['result']), "xxxxx"
    if command.split()[0] == 'hgetall':
        f.write("%s\n\n" % command)
        for k, v in result.items():
            f.write("%s:%s\n" % (k, v))
        f.write("\n\n\n")
    f.close()
