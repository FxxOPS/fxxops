# -*- coding: utf-8 -*-
__author__ = 'Abbott'

from .. import WebApp
import datetime

@WebApp.template_filter('Subdomain')
def Subdomain(Subdomain):
    sub_list = []
    if Subdomain:
        subdomain = Subdomain.split(';')
        for s in subdomain:
            # print s.split(','), "---"
            sub_list.append(s.split(','))
        # print subdomain,"--"
        # print Subdomain
    return sub_list

@WebApp.template_filter('Expiration')
def Expiration(Expiration):
    if Expiration:
        ex_dates = datetime.datetime.strptime(str(Expiration), "%Y-%m-%d")
        now_time = datetime.datetime.now().strftime("%Y-%m-%d")
        now_dates = datetime.datetime.strptime(now_time, "%Y-%m-%d")

        datas = (ex_dates - now_dates).days
        if int(datas) <= 90:
            return "True"
        else:
            return "False"
