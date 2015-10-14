# -*- coding: utf-8 -*-
'''
Created on 2014年5月28日

@author: yuan.gao6
'''

from contextlib import contextmanager
import MySQLdb
from const import *
from . import logger

SQL_INSERT_SERVER = """INSERT INTO server(id,domain,stat,ip_ex,ip_in,host_ip,project_id,idc,usages,os,cpu,memory,disk,pool,visible)
                                      VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1)
                                      ON DUPLICATE KEY UPDATE
                                      id=VALUES(id),
                                      domain=VALUES(domain),
                                      stat=VALUES(stat),
                                      ip_in=VALUES(ip_in),
                                      ip_ex=VALUES(ip_ex),
                                      host_ip=VALUES(host_ip),
                                      project_id=VALUES(project_id),
                                      idc=VALUES(idc),
                                      usages=VALUES(usages),
                                      os=VALUES(os),
                                      cpu=VALUES(cpu),
                                      memory=VALUES(memory),
                                      disk=VALUES(disk),
                                      pool=VALUES(pool),
                                      visible=1"""
SQL_SELECT_SERVER_ORDER_BY_PROJECT = """SELECT * FROM server ORDER BY project_id where visible=1"""
SQL_UPDATE_SERVER_VISIBLE_BY_ID = """UPDATE server SET visible=0 WHERE id='%s'"""

SQL_SELECT_PROJECT_BY_NAME = """SELECT * FROM project WHERE name = '%s'"""
SQL_INSERT_PROJECT = """INSERT INTO project(name) values('%s')"""

SQL_UPDATE_SALT_RETURNS_BY_JID = """UPDATE `salt_returns` SET `success`='%s', `return`='%s', `full_ret`='%s', `alter_time`='%s' WHERE `job_id` = '%s'"""

'''
Return a mysql cursor
'''
# @contextmanager
# def GetCursor():
#     try:
#         conn = MySQLdb.connect(host = DB_ADDRESS, user = DB_USER, passwd = DB_PWD, db = DB_DEF, port = DB_PORT, charset = DB_CHAR_SET)
#         cursor = conn.cursor()
#         yield cursor
#     except MySQLdb.DatabaseError as err:
#         cursor.execute("ROLLBACK")
#         logger.error(err)
#     else:
#         cursor.execute("COMMIT")
#     finally:
#         cursor.close()
#         conn.close()


class mysql_connect:

        def sql_exec(self, amont_sql, where='local',):
                result_dic = {}
                try:
                        if where == 'local':
                            conn = MySQLdb.connect(host=DB_ADDRESS, user=DB_USER, passwd=DB_PWD, port=DB_PORT, db=DB_DEF, charset=DB_CHAR_SET)
                        else:
                            conn = MySQLdb.connect(host=DIGEST_HOST, user=DIGEST_USER, passwd=DIGEST_PWD, port=DIGEST_PORT, db=DIGEST_DB, charset=DIGEST_CHAR_SET)
                        cur = conn.cursor()
                        cur.execute(amont_sql)
                        conn.commit()
                        value = cur.fetchall()
                        field = cur.description
                        cur.close()
                        conn.close()
                        result_dic = {'result': 'True', 'value': value, 'field': field}
                        return result_dic
                except MySQLdb.Error, e:
                        err_msg = "Mysql Error Msg: %s" % e
                        result_dic = {'result': 'False', 'err_msg': err_msg}
                        return result_dic
