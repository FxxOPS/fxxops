# -*- coding: utf-8 -*-
'''
Created on 2014年5月26日

@author: root
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, text
from Database.const import DB_ADDRESS, DB_PORT, DB_USER, DB_PWD, DB_CHAR_SET, DB_DEF

strEngine = "mysql+mysqldb://%s:%s@%s:%s/%s?charset=%s" % (DB_USER, DB_PWD, DB_ADDRESS, DB_PORT, DB_DEF, DB_CHAR_SET)
engine = create_engine(strEngine, echo = False)
Base = declarative_base(bind = engine)

class User(Base):
    __tablename__ = "user"
    id = Column("id", Integer, primary_key = True, nullable = False, unique = True)
    name = Column("name", String(16))
    password = Column("password", String(16))
    type = Column("type", Integer, nullable = False)
    create_time = Column("create_time", TIMESTAMP)

    def __repr__(self):
        return "<User(id='%s', name='%s, password=%s, type=%s, create_time=%s')>" % (self.id, self.name, self.password, self.type, self.create_time)

class Project(Base):
    __tablename__ = "project"
    id = Column("id", Integer, primary_key = True, nullable = False, unique = True)
    name = Column("name", String(128))
    gm_url= Column("gm_url",String(256))
    type=Column("type",String(64))

    def __repr__(self):
        return "<Project(id='%s', name='%s')>" % (self.id, self.name)

class PrivilegeProject(Base):
    __tablename__ = "prvlg_prj"
    id = Column("id", Integer, primary_key = True, nullable = False, unique = True, autoincrement = True)
    project_id = Column("project_id", Integer, nullable = False, unique = True)
    user_id = Column("user_id", Integer, nullable = False, unique = True)
    read = Column("read", Integer, nullable = False, unique = True)
    write = Column("write", Integer, nullable = False, unique = True)

    def __repr__(self):
        return "<PrivilegeProject(id='%s', project_id='%s', user_id='%s', read='%s', write='%s')>" % (self.id, self.project_id, self.user_id, self.read, self.write)

class PrivilegeSet(Base):
    __tablename__ = "prvlg_set"
    id = Column("id", Integer, primary_key = True, nullable = False, unique = True, autoincrement = True)
    set_id = Column("set_id", Integer, nullable = False, unique = True)
    user_id = Column("user_id", Integer, nullable = False, unique = True)
    init = Column("init", Integer, nullable = False, unique = True)
    merge = Column("merge", Integer, nullable = False, unique = True)
    upgrade = Column("upgrade", Integer, nullable = False, unique = True)
    reboot = Column("reboot", Integer, nullable = False, unique = True)

    def __repr__(self):
        return "<PrivilegeSet(id='%s', project_id='%s', user_id='%s', read='%s', write='%s')>" % (self.id, self.project_id, self.user_id, self.init, self.merge, self.upgrade, self.reboot)

class CommentHistory(Base):
    __tablename__ = "comment_history"

    id = Column("id", Integer, primary_key = True, nullable = False, unique = True, autoincrement = True)
    server_id = Column("server_id", String(128), nullable = False)
    comment = Column("comment", String(256), nullable = False, default = "INIT")
    update_time = Column("update_time", TIMESTAMP, server_default = text("CURRENT_TIMESTAMP"))
    def __repr__(self):
        return "<CommentHistory(id='%s', server_id = %s, comment='%s, update_time='%s')>" % (self.id, self.server_id, self.comment, self.update_time)

class SaltReturns(Base):
    __tablename__ = "salt_returns"

    job_id = Column("job_id", String(255), primary_key = True, nullable = False, unique = True)
    minion_id = Column("minion_id", String(255), nullable = False)
    fun = Column("fun", String(50), nullable = False)
    success = Column("success", String(10))
    ret = Column("return", Text)
    full_ret = Column("full_ret", Text)
    operation_id = Column("operation_id", String(32), nullable = False)
    user_id = Column("user_id", Integer, nullable = False)
    project_id = Column("project_id", Integer, nullable = False)
    set_id = Column("set_id", Integer, nullable = False)
    start_time = Column("start_time", String(64), nullable = False)
    alter_time = Column("alter_time", TIMESTAMP, server_default = text("CURRENT_TIMESTAMP"))
    action = Column("action", String(256))
    def __repr__(self):
        return "<SaltReturns(job_id='%s',\
                             minion_id='%s',\
                             fun='%s',\
                             success='%s',\
                             ret='%s',\
                             full_ret='%s',\
                             operation_id='%s',\
                             user_id = '%s',\
                             project_id = '%s',\
                             set_id = '%s',\
                             alter_time='%s',\)>" % \
                             (self.job_id,
                              self.minion_id,
                              self.fun,
                              self.success,
                              self.ret,
                              self.full_ret,
                              self.operation_id,
                              self.user_id,
                              self.project_id,
                              self.set_id,
                              self.alter_time)

class Server(Base):
    __tablename__ = "server"

    id = Column("id", String(128), primary_key = True, nullable = False, unique = True)
    domain = Column("domain", String(64), default = "NULL")
    stat = Column("stat", String(16), default = "NULL")
    ip_ex = Column("ip_ex", String(16), default = "NULL")
    ip_in = Column("ip_in", String(16), unique = True, default = "NULL")
    host_ip = Column("host_ip", String(16), default = "NULL")
    project_id = Column("project_id", Integer, default = "NULL")
    idc = Column("idc", String(64), default = "NULL")
    usages = Column("usages", String(128), default = "NULL")
    os = Column("os", String(32), default = "NULL")
    cpu = Column("cpu", String(32), default = "NULL")
    memory = Column("memory", String(32), default = "NULL")
    disk = Column("disk", String(32), default = "NULL")
    pool = Column("pool", String(32), default = "NULL")
    comment = Column("comment", String(255), default = "NULL")
    update_time = Column("update_time", TIMESTAMP, server_default = text("CURRENT_TIMESTAMP"))
    visible = Column("visible", Integer, default = "NULL")

    def __repr__(self):
        return "<Server(id='%s',\
                       domain='%s',\
                       stat='%s',\
                       ip_ex='%s',\
                       ip_in='%s',\
                       host_ip='%s',\
                       project_id='%s',\
                       idc='%s',\
                       usages='%s',\
                       os='%s',\
                       cpu='%s',\
                       memory='%s',\
                       disk='%s',\
                       pool='%s',\
                       comment='%s',\
                       update_time='%s',\
                       visible='%s')>" % (self.id,
                                          self.domain,
                                          self.stat,
                                          self.ip_ex,
                                          self.ip_in,
                                          self.host_ip,
                                          self.project_id,
                                          self.idc,
                                          self.usages,
                                          self.os,
                                          self.cpu,
                                          self.memory,
                                          self.disk,
                                          self.pool,
                                          self.comment,
                                          self.update_time,
                                          self.visible)

class Server_Set(Base):
    __tablename__ = "server_set"

    id = Column("id", Integer, primary_key = True, nullable = False, unique = True, autoincrement = True)
    server_id = Column("server_id", Integer, nullable = False)
    set_id = Column("set_id", Integer, nullable = False)
    def __repr__(self):
        return "<Server_Set(id='%s', server_id = %s, set_id='%s')>" % (self.id, self.server_id, self.set_id)

class Set(Base):
    __tablename__ = "set"

    id = Column("id", Integer, primary_key = True, nullable = False, unique = True, autoincrement = True)
    name = Column("name", String(32), nullable = False, unique = True)
    project_id = Column("project_id", Integer, nullable = False)
    create_userid =  Column("create_userid", Integer, nullable = False)
    create_time =  Column("create_time", TIMESTAMP, server_default = text("CURRENT_TIMESTAMP"))
    def __repr__(self):
        return "<Set(id='%s', name = %s, project_id='%s')>" % (self.id, self.name, self.project_id)

class Action(Base):
    __tablename__ = "action"

    id = Column("id", Integer, primary_key = True, nullable = False, unique = True, autoincrement = True)
    name = Column("name", String(32), nullable = False)
    path = Column("path", String(32))
    set_id = Column("set_id", Integer, nullable = False)
    def __repr__(self):
        return "<Set(id='%s', name = %s, path='%s, set_id='%s')>" % (self.id, self.name, self.path, self.set_id)


class Domain(Base):
    __tablename__ = "domain_info"

    domain_id = Column("id", Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    domain_name = Column("domain", String(64), unique=True,  nullable=False)
    project_id = Column("project_id", Integer, default="NULL")
    ip_source = Column("ip_source", String(16), default="NULL")
    status = Column("status", String(64), default="NULL")
    cdn_hightanti = Column("cdn_hightanti", String(64), default="NULL")
    pre_domain_id = Column("pre_domain_id", Integer, nullable=False, default=0)
    function = Column("function", String(255), default="NULL")
    comments = Column("comments", String(255), default="NULL")
    is_public = Column("is_public", Integer, default=0)
    register = Column("register", String(64), default="NULL")
    register_date = Column("register_date", TIMESTAMP, server_default="NULL")
    expiration = Column("expiration", TIMESTAMP, server_default="NULL")
    init_time = Column("init_time", TIMESTAMP, server_default="NULL")
    update_time = Column("update_time", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    dml_flag = Column("dml_flag", Integer, default="NULL")
    def __repr__(self):
        return "<Domain(domain_id='%s',\
                       domain_name ='%s',\
                       project_id='%s',\
                       ip_source='%s',\
                       status='%s',\
                       cdn_hightanti='%s',\
                       pre_domain_id='%s',\
                       fuction='%s',\
                       comments='%s',\
                       is_public='%s',\
                       register='%s',\
                       register_date='%s',\
                       expiration='%s',\
                       init_time='%s',\
                       update_time='%s',\
                       dml_flag='%s')>" % (self.domain_id,
                                          self.domain_name,
                                          self.project_id,
                                          self.ip_source,
                                          self.status,
                                          self.cdn_hightanti,
                                          self.pre_domain_id,
                                          self.fuction,
                                          self.comments,
                                          self.is_public,
                                          self.register,
                                          self.register_date,
                                          self.expiration,
                                          self.init_time,
                                          self.update_time,
                                          self.dml_flag)
