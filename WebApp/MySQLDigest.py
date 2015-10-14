# -*- coding: utf-8 -*-
__author__ = 'Abbott'

from . import WebApp
from . import logger
from flask import request, redirect, render_template, session, url_for
from Database.SeaOpsSqlAlchemy import db_session
from Database.SeaOpsMySQLdb import mysql_connect
from Utils import IsSessValid, getFirstPY
from util.MySQLUtil import MysqlReturnValue

import decimal
import datetime

mysql_conf = mysql_connect()


@WebApp.route('/digest/')
def digest():
    if (False == IsSessValid()):
        return redirect(url_for("login"))

    return render_template("digest/digest.html", title='Digest')


@WebApp.route('/digest/<DigestName>/', methods=['GET', 'POST'])
def digest_info(DigestName):
    if (False == IsSessValid()):
        return redirect(url_for("login"))

    HistoryName = "analyze_sql_history_%s" % DigestName
    ReviewName = "analyze_sql_review_%s" % DigestName
    if request.args.get('filter_id') is None or int(request.args.get('filter_id')) == 9:
        # digest_select_sql = 'select sum(binary z.ts_cnt) as ts_cnt, sum(binary z.Query_time_sum) as Query_time_sum, sum(binary z.Query_time_max) as Query_time_max,sum(binary z.Query_time_pct_95) as Query_time_pct_95, z.sample, z.checksum,f.*  from `%s` as  z left join `%s` f on z.checksum = f.checksum  group by z.checksum order by z.checksum;' % (HistoryName, ReviewName)
        digest_select_sql = 'select z.ts_cnt, z.Query_time_sum, z.Query_time_max, z.Query_time_pct_95, z.sample, z.checksum,f.*  from `%s` as  z left join `%s` f on z.checksum = f.checksum  group by z.checksum order by z.checksum;' % (HistoryName, ReviewName)
        result_list = MysqlReturnValue(digest_select_sql)
    else:
        review_id = request.args.get('filter_id')
        # filter_sql = 'select sum(binary z.ts_cnt) as ts_cnt, sum(binary z.Query_time_sum) as Query_time_sum, sum(binary z.Query_time_max) as Query_time_max,sum(binary z.Query_time_pct_95) as Query_time_pct_95, z.sample, z.checksum,f.*  from `%s` as  z left join `%s` f on z.checksum = f.checksum where review_switch = %d group by z.checksum order by z.checksum;' % (HistoryName, ReviewName, int(review_id))
        filter_sql = 'select z.ts_cnt, z.Query_time_sum, z.Query_time_max, z.Query_time_pct_95, z.sample, z.checksum,f.*  from (select * from `%s` order by ts_max desc ) as  z left join `%s` f on z.checksum = f.checksum where f.review_switch = %d group by z.checksum order by z.checksum;' % (HistoryName, ReviewName, int(review_id))
        result_list = MysqlReturnValue(filter_sql)



    return render_template("digest/digest_info.html", title='DigestInfo', table_name=DigestName, result_list=result_list)


@WebApp.route('/digest/<DigestName>/<SumCheck>')
def digest_pop(DigestName,SumCheck):
    if (False == IsSessValid()):
        return redirect(url_for("login"))

    HistoryName = "analyze_sql_history_%s" % DigestName
    ReviewName = "analyze_sql_review_%s" % DigestName

    # history_select_sql = " select sum(z.ts_cnt) as ts_cnt, sum(binary z.Query_time_sum) as Query_time_sum, sum(binary z.Query_time_min) as Query_time_min, sum(binary z.Query_time_max) as Query_time_max,sum(binary z.Query_time_pct_95) as Query_time_pct_95, sum(binary z.Query_time_stddev) as Query_time_stddev, sum(binary z.Query_time_median) as Query_time_median, sum(binary z.Lock_time_sum) as Lock_time_sum, sum(binary z.Lock_time_min) as Lock_time_min, sum(binary z.Lock_time_max) as Lock_time_max, sum(binary z.Lock_time_pct_95) as Lock_time_pct_95, sum(binary z.Lock_time_stddev) as Lock_time_stddev, sum(binary z.Lock_time_median) as Lock_time_median, sum(binary z.Rows_sent_sum) as Rows_sent_sum, sum(binary z.Rows_sent_min) as Rows_sent_min, sum(binary z.Rows_sent_max) as Rows_sent_max, sum(binary z.Rows_sent_pct_95) as Rows_sent_pct_95,sum(binary z.Rows_sent_stddev) as Rows_sent_stddev, sum(binary z.Rows_sent_median) as Rows_sent_median, sum(binary z.Rows_examined_sum) as Rows_examined_sum, sum(binary z.Rows_examined_min) as Rows_examined_min, sum(binary z.Rows_examined_max) as Rows_examined_max, sum(binary z.Rows_examined_pct_95) as Rows_examined_pct_95, sum(binary z.Rows_examined_stddev) as Rows_examined_stddev, sum(binary z.Rows_examined_median) as Rows_examined_median, z.sample, f.fingerprint from `%s` z left join `%s` f on z.checksum = f.checksum where z.checksum = %d and z.ts_max in (select max(ts_max) from `%s` where checksum = %d)" % (HistoryName, ReviewName, int(SumCheck), HistoryName, int(SumCheck))
    history_select_sql = 'select  z.*,f.fingerprint, f.comments from (select * from `%s` order by ts_max desc ) as  z left join `%s` f on z.checksum = f.checksum where z.checksum = %d group by z.checksum' % (HistoryName, ReviewName, int(SumCheck))
    history_return_list = MysqlReturnValue(history_select_sql)
    return render_template("digest/digestpop.html", title='Digest', history_return_list=history_return_list, table_name=DigestName)

@WebApp.route('/digest/comments/<SumCheck>', methods=['GET', 'POST'])
def digest_comments(SumCheck):
    if request.method == 'POST':
        print request.form['tablename']
        print request.form['comments'], "+++"
        print SumCheck
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ReviewName = "analyze_sql_review_%s" % request.form['tablename']
        update_sql = "update `%s` set comments = '%s',reviewed_on = '%s', review_switch = 1 where checksum = %d" % (ReviewName, request.form['comments'], now_time, int(SumCheck))
        comments_result = mysql_conf.sql_exec(update_sql)
    return redirect("/digest/%s/%s" % (request.form['tablename'], SumCheck))


