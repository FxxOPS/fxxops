# -*- coding: utf-8 -*-
__author__ = 'Abbott'

import commands
import re
import datetime
import time

from Script import mysqlconf


domain_list = []

subdomain_head_list = ['www', 'v', 's', 'p1']


cdn_rule_dic = {'.cdng[a-z].net.': 'CDNetwork'}
highanti_rule_dic = {'5.254.87.': 'Voxility'}


check_sql = 'select domain_name from domain_info where pre_domain_id = %d;'
update_sub_sql = "update domain_info set cdn_hightanti = '%s', dml_time = '%s', dml_flag = 2 where domain_name = '%s' and pre_domain_id = %d;"
insert_sub_sql = "insert into domain_info(domain_name, project_name, cdn_hightanti, pre_domain_id, init_time, dml_time) value ('%s', 'V项目', '%s', %d, '%s', '%s')"
delete_sub_sql = "delete from domain_info where domain_name = '%s' and pre_domain_id = %d;"


mysql_conf = mysqlconf.mysql_connect()
now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def auto_dig(domain, pre_id):
    
    dig_result = commands.getstatusoutput('dig %s +short |head -1' % domain)
    if int(dig_result[0]) == 0:
        if dig_result[1] == '':
            mysql_conf.sql_exec("update domain_info set status = '已解析', dml_time = '%s' where domain_name = '%s' " % (now_time, str(domain)))
        else:
            mysql_conf.sql_exec("update domain_info set status = '未解析', dml_time = '%s' where domain_name = '%s' " % (now_time, str(domain)))

    for head in subdomain_head_list:
        subdomain = '%s.%s' % (head, domain)
        dig_sub_result = commands.getstatusoutput('dig %s +short |head -1' % subdomain)
        cdn_result_list = []
        for k, v in cdn_rule_dic.items():
            if re.search(k, dig_sub_result[1]):
                cdn_result_list.append(v)
            else:
                cdn_result_list.append("Unknow")

        delete_list = []
        if len(list(set(cdn_result_list))) == 1 and list(set(cdn_result_list))[0] == "Unknow":
            delete_list.append("Unknow")
            pass
        else:
            print cdn_result_list, "+++"
            if 'Unknow' in cdn_result_list:
                reslut = list(set(cdn_result_list)).remove('Unknow')[0]
            else:
                reslut = list(set(cdn_result_list))[0]

            check_result = mysql_conf.sql_exec(check_sql % (pre_id))

            check_value = []
            for v in check_result['value']:
                check_value.append(v[0])

            if head in check_value:
                print head,"update, fff"
                mysql_conf.sql_exec(update_sub_sql % (reslut, now_time, head, pre_id))
            else:
                mysql_conf.sql_exec(insert_sub_sql % (head, reslut, pre_id, now_time, now_time))


        highanti_result_list = []
        for k, v in highanti_rule_dic.items():
            if re.search(k, dig_sub_result[1]):
                highanti_result_list.append(v)
            else:
                highanti_result_list.append("Unknow")
        if len(list(set(highanti_result_list))) == 1 and list(set(highanti_result_list))[0] == "Unknow":
            delete_list.append("Unknow")
            pass
        else:
            print highanti_result_list, '---'
            if 'Unknow' in highanti_result_list:
                reslut = list(set(highanti_result_list)).remove('Unknow')[0]
            else:
                reslut = list(set(highanti_result_list))[0]

            check_result = mysql_conf.sql_exec(check_sql % (pre_id))

            check_value = []
            for v in check_result['value']:
                check_value.append(v[0])

            if head in check_value:
                print head,"update, fff"
                mysql_conf.sql_exec(update_sub_sql % (reslut, now_time, head, pre_id))
            else:
                mysql_conf.sql_exec(insert_sub_sql % (head, reslut, pre_id, now_time, now_time))
        if len(delete_list) == 2 and list(set(delete_list))[0] == "Unknow":
            mysql_conf.sql_exec(delete_sub_sql % (head, pre_id))