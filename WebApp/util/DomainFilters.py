# -*- coding: utf-8 -*-
__author__ = 'Abbott'

from .. import WebApp
import datetime

@WebApp.template_filter('Subdomain')
def Subdomain(Subdomain):
    """
    @note 格式化显示子域名
    :param Subdomain:
    :return:
    """
    sub_list = []
    if Subdomain:
        subdomain = Subdomain.split(';')
        for s in subdomain:
            sub_list.append(s.split(','))
    return sub_list

@WebApp.template_filter('Expiration')
def Expiration(Expiration):
    """
    @note 过滤超时时间信息（90天）
    :param Expiration:
    :return:
    """
    if Expiration:
        ex_dates = datetime.datetime.strptime(str(Expiration), "%Y-%m-%d")
        now_time = datetime.datetime.now().strftime("%Y-%m-%d")
        now_dates = datetime.datetime.strptime(now_time, "%Y-%m-%d")

        datas = (ex_dates - now_dates).days
        if int(datas) <= 90:
            return "True"
        else:
            return "False"
