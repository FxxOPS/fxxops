# -*- coding: utf-8 -*-

import salt.utils.event
import json,time
from Database.SeaOpsSqlAlchemy import db_session
from . import logger
from threading import Thread

def EventLog2db():
    event = salt.utils.event.MasterEvent('/var/run/salt/master')
    for eachevent in event.iter_events(full=True):
        ret = eachevent['data']
        if ("ret" in eachevent['tag']) and ret.has_key('fun') and ret['return'] <> '' and ret['fun'] == "cmd.run":
            logger.info('update Salt return: %s - %s'% (ret["jid"],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            db_session.UpdateSaltReturns(str(ret["success"]), ret["return"], json.dumps(ret), ret["_stamp"], ret["jid"])

'''
A thread keep getting remote server salt's result
'''


class eventThread(Thread):
    def __init__(self):
        Thread.__init__(self)
       # self.name= name
        #self.sTime = sTkjkime
    def run(self):
        logger.info('Start Event2DB Thread: %s'% time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
        EventLog2db()

def EventThreadRun():
    thread = eventThread()
    thread.setDaemon(True)
    thread.start()

if __name__ == "__main__":
    EventLog2db()

