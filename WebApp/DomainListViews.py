# -*- coding: utf-8 -*-
__author__ = 'Abbott'

from . import WebApp
from . import logger
from flask import request, redirect, render_template, session, url_for
from Database.SeaOpsSqlAlchemy import DomainSession
from Database.SeaOpsMySQLdb import mysql_connect
from Utils import IsSessValid,getFirstPY


mysql_conf = mysql_connect()



@WebApp.route('/domain/')
def domain_info():
    """
    @note domain信息返回页面
    :return:
    """
    if(False == IsSessValid()):
        return redirect(url_for("login"))

    domain_return_list = []
    domain_field = []

    domain_select_sql = 'select f.*, GROUP_CONCAT(z.domain_name,"," ,z.ip_source, "," ,z.cdn_hightanti SEPARATOR ";") as subdomain  from domain_info f left join domain_info z on z.pre_domain_id = f.domain_id where f.pre_domain_id = 0  group by f.domain_id;'

    domain_result = mysql_conf.sql_exec(domain_select_sql)
    for f in domain_result['field']:
        domain_field.append(f[0])

    for v in domain_result['value']:
        domain_dic = {}
        for n in range(len(domain_field)):
            if v[n] is None:
                domain_dic[domain_field[n]] = ""
                logger.info(domain_dic)
            else:
                domain_dic[domain_field[n]] = v[n]
        domain_return_list.append(domain_dic)
    return render_template("domain/domain_info.html", title='Domain', domain_return_list=domain_return_list)


@WebApp.route('/domain/add/', methods=['GET', 'POST'])
def domain_add():
    """
    @note domain添加信息
    @note Post方法: 页面提交信息到后台
    :return:
    """
    if request.method == 'POST':
        subdomain_dic = {"www": request.form['www_ip'], 'v': request.form['v_ip'], 's': request.form['s_ip'], 'p1': request.form['p1_ip']}
        project_name = DomainSession.SelectProjectId(request.form['project_id'])
        for domain in request.form['domain_name'].split('\r\n'):
            pre_id = DomainSession.InsertDomain(domain, request.form['project_id'], project_name[0], request.form['fuction'], request.form['comments'])
            DomainSession.InsertSubdomain(pre_id[0], subdomain_dic)
        return redirect("/domain")

    return render_template("domain/add_update.html")


@WebApp.route('/domain/comments/<iDomainId>', methods=['GET', 'POST'])
def domain_comments(iDomainId):
    """
    @note domain comment页面信息展示
    @note Post方法: domain comment提交信息到后台
    :param iDomainId:
    :return:
    """
    domain_return_list = []
    domain_field = []
    domain_id_select_sql = 'select f.*, GROUP_CONCAT(z.domain_name,"," ,z.ip_source, "," ,z.cdn_hightanti SEPARATOR ";") as subdomain  from domain_info f left join domain_info z on z.pre_domain_id = f.domain_id where f.pre_domain_id = 0 and f.domain_id = %d  group by f.domain_id;' % int(iDomainId)
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
        DomainSession.UpdateDomainComments(iDomainId, request.form['comments'])
        return redirect("/domain")
    return render_template("domain/domain_comments.html", title='Comment', domain_return_list=domain_return_list)


@WebApp.route('/domain/update/', methods=['GET', 'POST'])
def domain_update():
    """
    @note domain 更新信息页面
    :return:
    """
    # 获取要更新的domain到前台
    if request.form['page'] == 'DomainMain':
        domains = request.form['checks']
        domain_list = domains.split('|')
        return render_template("domain/update.html", domain_list=domain_list)
    else:
        # 获取前台要更新的domain信息并更新数据库
        DomainDic = {
            'comments': request.form['comments'],
            'function': request.form['function'],
            'www': request.form['www_ip'],
            'v': request.form['v_ip'],
            'p1': request.form['p1_ip'],
            's': request.form['s_ip']
        }
        domain_list = request.values.getlist('domains')
        for domain in domain_list:
            domain_id = DomainSession.SelectDomainId(domain)
            DomainSession.UpdateDomain(domain_id[0], DomainDic)
        return redirect("/domain/")


