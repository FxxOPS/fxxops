# -*- coding: utf-8 -*-
__author__ = 'Abbott'

import commands
import re
import mysqlconf
import datetime
import time

starttime = time.clock()
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


def get_domain():
    domain_list = []
    domain_field = []
    sql = 'select domain_id, domain_name from domain_info where pre_domain_id = 0 order by domain_id;'
    domains = mysql_conf.sql_exec(sql)

    for f in domains['field']:
        domain_field.append(f[0])

    for domain in domains['value']:
        domain_dic = {}
        for n in range(len(domain_field)):
            domain_dic[domain_field[n]] = domain[n]
        domain_list.append(domain_dic)
    print domain_list
    return domain_list


def auto_dig(domains_list):
    for domain in domains_list:
        dig_result = commands.getstatusoutput('dig %s +short |head -1' % domain['domain_name'])
        if int(dig_result[0]) == 0:
            if dig_result[1] == '':
                mysql_conf.sql_exec(
                    "update domain_info set status = '已解析', dml_time = '%s' where domain_name = '%s' " % (
                    now_time, str(domain['domain_name'])))
            else:
                mysql_conf.sql_exec(
                    "update domain_info set status = '未解析', dml_time = '%s' where domain_name = '%s' " % (
                    now_time, str(domain['domain_name'])))

        for head in subdomain_head_list:
            subdomain = '%s.%s' % (head, domain['domain_name'])
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

                check_result = mysql_conf.sql_exec(check_sql % (domain['domain_id']))

                check_value = []
                for v in check_result['value']:
                    check_value.append(v[0])

                if head in check_value:
                    print head, "update, fff"
                    mysql_conf.sql_exec(update_sub_sql % (reslut, now_time, head, domain['domain_id']))
                else:
                    mysql_conf.sql_exec(insert_sub_sql % (head, reslut, domain['domain_id'], now_time, now_time))

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

                check_result = mysql_conf.sql_exec(check_sql % (domain['domain_id']))

                check_value = []
                for v in check_result['value']:
                    check_value.append(v[0])

                if head in check_value:
                    print head, "update, fff"
                    mysql_conf.sql_exec(update_sub_sql % (reslut, now_time, head, domain['domain_id']))
                else:
                    mysql_conf.sql_exec(insert_sub_sql % (head, reslut, domain['domain_id'], now_time, now_time))
            if len(delete_list) == 2 and list(set(delete_list))[0] == "Unknow":
                mysql_conf.sql_exec(delete_sub_sql % (head, domain['domain_id']))


if __name__ == '__main__':
    domains_list = get_domain()
    auto_dig(domains_list)
    endtime = time.clock()
    print (endtime - starttime)
