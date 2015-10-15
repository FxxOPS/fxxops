# -*- coding: utf-8 -*-
__author__ = 'Abbott'

import commands
import re
import datetime
import time
import sys

sys.path.append("/ops/fxxops/Database")
from SeaOpsMySQLdb import mysql_connect


starttime = time.clock()
domain_list = []

subdomain_head_list = ['www', 'v', 's', 'p1']


cdn_rule_dic = {'.cdng[a-z].net.': 'CDNetwork'}
highanti_rule_dic = {'5.254.87.': 'Voxility', 'incapdns': 'incapslua'}

dns_check = ['ultradns', 'dnsmadeeasy', 'cloudflare']


check_sql = 'select domain_name from domain_info where pre_domain_id = %d;'
counts_sql = 'select count(1) from domain_info where pre_domain_id = %d;'
update_sub_sql = "update domain_info set cdn_hightanti = '%s', dml_time = '%s', dml_flag = 2 where domain_name = '%s' and pre_domain_id = %d;"
insert_sub_sql = "insert into domain_info(domain_name, cdn_hightanti, pre_domain_id, init_time, dml_time, ip_source) value ('%s', '%s', %d, '%s', '%s', 'NULL')"
delete_sub_sql = "delete from domain_info where domain_name = '%s' and pre_domain_id = %d;"


mysql_conf = mysql_connect()
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

        dns_result = commands.getstatusoutput(''' dig %s +trace | grep "%s" |awk '{print $NF}' ''' % (str(domain['domain_name']), str(domain['domain_name'])))
        if int(dns_result[0]) == 0:
            for dns in dns_check:
                if re.search(dns, dns_result[1]):
                    mysql_conf.sql_exec("update domain_info set domain_DNS = '%s', dml_time = '%s' where domain_name = '%s' " % (dns, now_time, str(domain['domain_name'])))
                else:
                    pass
        time_result = commands.getstatusoutput(''' whois %s|grep Expir | awk '{print $NF}' ''' % (str(domain['domain_name'])))
        if int(time_result[0]) == 0:
            times = str(time_result[1]).split('T')[0]
            print domain['domain_name'], times, "+++"
            mysql_conf.sql_exec("update domain_info set expiration = '%s', dml_time = '%s' where domain_name = '%s' " % (times, now_time, str(domain['domain_name'])))

        for head in subdomain_head_list:
            subdomain = '%s.%s' % (head, domain['domain_name'])
            dig_sub_result = commands.getstatusoutput('dig %s +short |head -1' % subdomain)
            delete_list = []


            cdn_result_list = []
            for k, v in cdn_rule_dic.items():
                cdn_result_dic = {head: "Unknow"}
                if re.search(k, dig_sub_result[1]):
                    cdn_result_dic[head] = v
                    cdn_result_list.append(cdn_result_dic)
            if cdn_result_list:
                check_result = mysql_conf.sql_exec(check_sql % (domain['domain_id']))

                check_value = []
                for v in check_result['value']:
                    check_value.append(v[0])

                if head in check_value:
            #         # print head,"update, fff"
                    mysql_conf.sql_exec(update_sub_sql % (cdn_result_list[0][head], now_time, head, domain['domain_id']))
                else:
                    mysql_conf.sql_exec(insert_sub_sql % (head, cdn_result_list[0][head], domain['domain_id'], now_time, now_time))
            else:
                delete_list.append("Unknow")

            highanti_result_list = []
            for k, v in highanti_rule_dic.items():
                highanti_result_dic = {head: "Unknow"}
                if re.search(k, dig_sub_result[1]):
                    highanti_result_dic[head] = v
                    highanti_result_list.append(highanti_result_dic)
            if highanti_result_list:
                # delete_list.append("Unknow")
                check_result = mysql_conf.sql_exec(check_sql % (domain['domain_id']))

                check_value = []
                for v in check_result['value']:
                    check_value.append(v[0])

                if head in check_value:
                    # print head,"update, fff"
                    mysql_conf.sql_exec(update_sub_sql % (highanti_result_list[0][head], now_time, head, domain['domain_id']))
                else:
                    mysql_conf.sql_exec(insert_sub_sql % (head, highanti_result_list[0][head], domain['domain_id'], now_time, now_time))
            else:
                delete_list.append("Unknow")

            if len(delete_list) == 2 and list(set(delete_list))[0] == "Unknow":
                mysql_conf.sql_exec(delete_sub_sql % (head, domain['domain_id']))

        count_result = mysql_conf.sql_exec(counts_sql % int(domain['domain_id']))
        if int(count_result['value'][0][0]) == 0:
            mysql_conf.sql_exec("update domain_info set status = '2', dml_time = '%s' where domain_name = '%s' " % (now_time, str(domain['domain_name'])))
        else:
            mysql_conf.sql_exec("update domain_info set status = '1', dml_time = '%s' where domain_name = '%s' " % (now_time, str(domain['domain_name'])))
if __name__ == '__main__':

    domains_list=get_domain()
    auto_dig(domains_list)
    endtime = time.clock()
    print (endtime-starttime)
