# -*- coding: utf-8 -*-
__author__ = 'Abbott'
import redis
import sys
import uuid
import os
from .. import WebApp
from ..const import *

# REDIS_DOWNLOAD_PATH = 'FileOperate/Redis/Download'


def run_redis(command_list):
    """
    @note redis命令的执行和调用redis_file方法结果输送到文件里
    :param command_list:
    :return:
    """
    filename = "redis-%s.%s" % (uuid.uuid4(), 'txt')
    path = os.path.join(WebApp.root_path, REDIS_DOWNLOAD_PATH, filename)
    pool = redis.ConnectionPool(host='10.1.110.24', port=6379)
    r = redis.Redis(connection_pool=pool)
    for command in command_list:

        if command.split()[0] == 'hgetall':
            redis_result = r.hgetall(command.split()[1])
            redis_file(command, redis_result, path, filename)

    return REDIS_DOWNLOAD_PATH, filename


def redis_file(command, result, path, filename):
    """
    @note redis命令执行完的结果输送到文件里
    :param command:
    :param result:
    :param path:
    :param filename:
    :return:
    """
    f = open(path, 'ab+')
    if command.split()[0] == 'hgetall':
        f.write("%s\n\n" % command)
        for k, v in result.items():
            f.write("%s:%s\n" % (k, v))
        f.write("\n\n\n")
    f.close()
