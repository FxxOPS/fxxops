# -*- coding: utf-8 -*-
__author__ = 'Abbott'


import json
from . import WebApp
from flask import request, redirect, render_template, session, url_for
from Database.SeaOpsSqlAlchemy import db_session
import mysqlconf

mysql_conf = mysqlconf.mysql_connect()

@WebApp.route('/domain/')
def domain_info():
    domain_return_list = []
    domain_field = []

    domain_select_sql = 'select f.*, GROUP_CONCAT(z.domain_name,"-->", z.cdn_hightanti SEPARATOR "<br>") as subdomain, p.name as project_name from domain_info f, domain_info z, project p where z.pre_domain_id = f.domain_id and f.project_id = p.id group by f.domain_id;'
    domain_result = mysql_conf.sql_exec(domain_select_sql)
    for f in domain_result['field']:
        domain_field.append(f[0])

    for v in domain_result['value']:
        domain_dic = {}
        for n in range(len(domain_field)):
            domain_dic[domain_field[n]] = v[n]
        domain_return_list.append(domain_dic)

    return render_template("domain.html", title='Domain', domain_return_list=domain_return_list)