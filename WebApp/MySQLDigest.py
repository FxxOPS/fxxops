# -*- coding: utf-8 -*-
__author__ = 'Abbott'

from . import WebApp
from . import logger
from flask import request, redirect, render_template, session, url_for
from Database.SeaOpsMySQLdb import mysql_connect
from Utils import IsSessValid, getFirstPY
from util.MySQLUtil import MysqlReturnValue
import datetime
import json

mysql_conf = mysql_connect()


@WebApp.route('/digest/')
def digest():
    """
    @note MySQL Digest总的展示页面
    :return:
    """
    if (False == IsSessValid()):
        return redirect(url_for("login"))

    return render_template("digest/digest.html", title='Digest')


@WebApp.route('/digest/<DigestName>/', methods=['GET', 'POST'])
def digest_info(DigestName):
    """
    @note MySQL Digest具体数据库信息返货前台
    :param DigestName:
    :return:
    """
    if (False == IsSessValid()):
        return redirect(url_for("login"))

    HistoryName = "analyze_sql_history_%s" % DigestName
    ReviewName = "analyze_sql_review_%s" % DigestName
    if request.args.get('filter_id') is None or int(request.args.get('filter_id')) == 9:
        digest_select_sql = 'select z.ts_cnt, z.Query_time_sum, z.Query_time_max, z.Query_time_pct_95, z.sample, z.checksum,f.*  from (select * from `%s` order by ts_max desc ) as  z left join `%s` f on z.checksum = f.checksum  group by z.checksum;' % (HistoryName, ReviewName)
        result_list = MysqlReturnValue(digest_select_sql)
    else:
        review_id = request.args.get('filter_id')
        filter_sql = 'select z.ts_cnt, z.Query_time_sum, z.Query_time_max, z.Query_time_pct_95, z.sample, z.checksum,f.*  from (select * from `%s` order by ts_max desc ) as  z left join `%s` f on z.checksum = f.checksum where f.review_switch = %d group by z.checksum;' % (HistoryName, ReviewName, int(review_id))
        result_list = MysqlReturnValue(filter_sql)


    return render_template("digest/digest_info.html", title='DigestInfo', table_name=DigestName, result_list=result_list)


@WebApp.route('/digest/<DigestName>/<SumCheck>')
def digest_pop(DigestName,SumCheck):
    """
    @note 针对某一checksum展示其所有信息
    :param DigestName:
    :param SumCheck:
    :return:
    """
    if (False == IsSessValid()):
        return redirect(url_for("login"))

    HistoryName = "analyze_sql_history_%s" % DigestName
    ReviewName = "analyze_sql_review_%s" % DigestName

    history_select_sql = 'select  z.*,f.fingerprint, f.comments from (select * from `%s` order by ts_max desc ) as  z left join `%s` f on z.checksum = f.checksum where z.checksum = %d group by z.checksum' % (HistoryName, ReviewName, int(SumCheck))
    history_return_list = MysqlReturnValue(history_select_sql)
    return render_template("digest/digestpop.html", title='Digest', history_return_list=history_return_list, table_name=DigestName)

@WebApp.route('/digest/comments/<SumCheck>', methods=['GET', 'POST'])
def digest_comments(SumCheck):
    """
    @note 前台MySQL Digest某一sumcheck提交的comment存入数据库
    :param SumCheck:
    :return:
    """
    if request.method == 'POST':
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ReviewName = "analyze_sql_review_%s" % request.form['tablename']
        update_sql = "update `%s` set comments = '%s',reviewed_on = '%s', review_switch = 1 where checksum = %d" % (ReviewName, request.form['comments'], now_time, int(SumCheck))
        comments_result = mysql_conf.sql_exec(update_sql, 'remote')
    return redirect("/digest/%s/%s" % (request.form['tablename'], SumCheck))


@WebApp.route('/digest/comments/rewiew', methods=['GET', 'POST'])
def digest_rewiew():
    """
    @note 批量处理MySQL Digest rewiew数据
    :return:
    """

    # 得到所有checksum，并去除最后一个多余的逗号
    rewies_list = request.form['checksum'].replace('<br>', ',')[:-1]
    comments = request.form['comment']
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ReviewName = "analyze_sql_review_%s" % request.form['tableName']

    update_sql = "update `%s` set comments = '%s',reviewed_on = '%s', review_switch = 1 where checksum in (%s)" % (ReviewName, comments, now_time, rewies_list)
    comments_result = mysql_conf.sql_exec(update_sql, 'remote')
    return_value = comments_result['result']
    return "%s" % json.dumps(return_value)


