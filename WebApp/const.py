# -*- coding: utf-8 -*-
'''
Created on 2014年6月10日

@author: root
'''

from Database.SeaOpsSqlAlchemy import db_session, PrivilegeSession

PRI_SYS_ADMIN = 0
PRI_OPS_ADMIN = 1
PRI_OP_ADMIN = 2


### Privielegs dic
TRUE = '1'
FALSE = '2'

PRIV_TRUE = '1'
PRIV_FALSE = '0'


### Pre ID
PAGE_LEV1_PRE_ID = 0


### Menu Dic
MENU_DIC = PrivilegeSession.SelectMenu('DIC')


### Redis download path
REDIS_DOWNLOAD_PATH = 'FileOperate/Redis/Download'

### Redis dict
REDIS_STATUS_PRE_ID = '1'