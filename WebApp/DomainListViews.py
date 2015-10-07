# -*- coding: utf-8 -*-
__author__ = 'Abbott'


import json
from . import WebApp
from flask import request, redirect, render_template, session, url_for
from Database.SeaOpsSqlAlchemy import db_session
import mysqlconf
from Utils import IsSessValid,getFirstPY
from domain.utils import auto_dig

mysql_conf = mysqlconf.mysql_connect()

@WebApp.route('/domain/')
def domain_info():
    if(False == IsSessValid()):
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
    # print domain_return_list
    return render_template("domain/domain_info.html", title='Domain', domain_return_list=domain_return_list)


@WebApp.route('/domain/add/', methods=['GET', 'POST'])
def domain_add():
    if request.method == 'POST':
        subdomain_dic = {"www": request.form['www_ip'], 'v': request.form['v_ip'], 's': request.form['s_ip'], 'p1': request.form['p1_ip']}
        project_name = db_session.SelectProjectId(request.form['project_id'])
        # print subdomain_dic
        for domain in request.form['domain_name'].split('\r\n'):
            # print domain,"+++"
            pre_id = db_session.InsertDomain(domain, request.form['project_id'], project_name[0], request.form['fuction'], request.form['comments'])
            # print pre_id[0]
            db_session.InsertSubdomain(pre_id[0], subdomain_dic)
            auto_dig(domain, pre_id[0])
        return redirect("/domain")
    return render_template("domain/add_update.html")


@WebApp.route('/domain/comments/<iDomainId>', methods=['GET', 'POST'])
def domain_comments(iDomainId):
    domain_return_list = []
    domain_field = []
    domain_id_select_sql = 'select f.*, GROUP_CONCAT(z.domain_name,":  ",z.ip_source,"|", z.cdn_hightanti SEPARATOR "<br>") as subdomain  from domain_info f left join domain_info z on z.pre_domain_id = f.domain_id where f.pre_domain_id = 0 and f.domain_id = %d  group by f.domain_id;' % int(iDomainId)
    domain_result = mysql_conf.sql_exec(domain_id_select_sql)
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

    if request.method == 'POST':
        print request.form['comments'], "+++"
        db_session.UpdateDomainComments(iDomainId, request.form['comments'])
        return redirect("/domain")
    return render_template("domain/domain_comments.html", title='Comment', domain_return_list=domain_return_list)