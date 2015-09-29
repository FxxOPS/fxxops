# -*- coding: utf-8 -*-
__author__ = 'Abbott'

import json
from . import WebApp
from flask import request, redirect, render_template, session, url_for
from Database.SeaOpsSqlAlchemy import db_session
import mysqlconf
from Utils import IsSessValid, getFirstPY

mysql_conf = mysqlconf.mysql_connect()


@WebApp.route('/domain/')
def domain_info():
    if (False == IsSessValid()):
        return redirect(url_for("login"))

    domain_return_list = []
    domain_field = []

    domain_select_sql = 'select f.*, GROUP_CONCAT(z.domain_name,":  ",z.ip_source,"|", z.cdn_hightanti SEPARATOR "<br>") as subdomain  from domain_info f left join domain_info z on z.pre_domain_id = f.domain_id where f.pre_domain_id = 0  group by f.domain_id;'
    domain_result = mysql_conf.sql_exec(domain_select_sql)
    for f in domain_result['field']:
        domain_field.append(f[0])

    for v in domain_result['value']:
        domain_dic = {}
        for n in range(len(domain_field)):
            if v[n] is None:
                domain_dic[domain_field[n]] = ""
            else:
                domain_dic[domain_field[n]] = v[n]
        domain_return_list.append(domain_dic)

    return render_template("domain/domain_info.html", title='Domain', domain_return_list=domain_return_list)