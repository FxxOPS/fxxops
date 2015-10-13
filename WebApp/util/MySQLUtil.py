# -*- coding: utf-8 -*-
__author__ = 'Abbott'

import decimal
from Database.SeaOpsMySQLdb import mysql_connect

mysql_conf = mysql_connect()

def MysqlReturnValue(sql):
    return_list = []
    field = []
    select_sql = '%s' % (sql)
    result = mysql_conf.sql_exec(select_sql, 'remote')

    for f in result['field']:
        field.append(f[0])

    for v in result['value']:
        result_dic = {}
        for n in range(len(field)):
            if v[n] is None:
                result_dic[field[n]] = ""
            elif type(v[n]) == float:
                result_dic[field[n]] = '%.6f' % decimal.Decimal(v[n])
            else:
                result_dic[field[n]] = v[n]
        return_list.append(result_dic)
    return return_list
