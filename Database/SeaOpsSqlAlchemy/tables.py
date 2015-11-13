# -*- coding: utf-8 -*-
__author__ = 'Abbott'

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, text
from Database.const import DB_ADDRESS, DB_PORT, DB_USER, DB_PWD, DB_CHAR_SET, DB_DEF, DB_POOL_RECYCLE, DB_POOL_SIZE

strEngine = "mysql+mysqldb://%s:%s@%s:%s/%s?charset=%s" % (DB_USER, DB_PWD, DB_ADDRESS, DB_PORT, DB_DEF, DB_CHAR_SET)
engine = create_engine(strEngine, echo=False, pool_size=DB_POOL_SIZE, pool_recycle=DB_POOL_RECYCLE)
Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ = "user"
    id = Column("id", Integer, primary_key=True, nullable=False, unique=True)
    name = Column("name", String(16))
    password = Column("password", String(16))
    type = Column("type", Integer, nullable=False)
    create_time = Column("create_time", TIMESTAMP)

    def __repr__(self):
        return "<User(id='%s', name='%s, password=%s, type=%s, create_time=%s')>" % (
            self.id, self.name, self.password, self.type, self.create_time)


class Project(Base):
    __tablename__ = "project"
    id = Column("id", Integer, primary_key=True, nullable=False, unique=True)
    name = Column("name", String(128))
    project_keys = Column("project_keys", String(128))
    gm_url = Column("gm_url", String(256))
    type = Column("type", String(64))

    def __repr__(self):
        return "<Project(id='%s', name='%s')>" % (self.id, self.name)


class PrivilegeProject(Base):
    __tablename__ = "prvlg_prj"
    id = Column("id", Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    project_id = Column("project_id", Integer, nullable=False, unique=True)
    user_id = Column("user_id", Integer, nullable=False, unique=True)
    read = Column("read", Integer, nullable=False, unique=True)
    write = Column("write", Integer, nullable=False, unique=True)

    def __repr__(self):
        return "<PrivilegeProject(id='%s', project_id='%s', user_id='%s', read='%s', write='%s')>" % (
            self.id, self.project_id, self.user_id, self.read, self.write)


class PrivilegeSet(Base):
    __tablename__ = "prvlg_set"
    id = Column("id", Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    set_id = Column("set_id", Integer, nullable=False, unique=True)
    user_id = Column("user_id", Integer, nullable=False, unique=True)
    init = Column("init", Integer, nullable=False, unique=True)
    merge = Column("merge", Integer, nullable=False, unique=True)
    upgrade = Column("upgrade", Integer, nullable=False, unique=True)
    reboot = Column("reboot", Integer, nullable=False, unique=True)

    def __repr__(self):
        return "<PrivilegeSet(id='%s', project_id='%s', user_id='%s', read='%s', write='%s')>" % (
            self.id, self.project_id, self.user_id, self.init, self.merge, self.upgrade, self.reboot)


class CommentHistory(Base):
    __tablename__ = "comment_history"

    id = Column("id", Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    domain_id = Column("domain_id", String(128), nullable=False)
    comment = Column("comment", String(256), nullable=False, default="INIT")
    op_comments = Column("op_comments", String(256), nullable=False, default="INIT")
    apply_user_id = Column("apply_user_id", Integer, default="NULL")
    update_time = Column("update_time", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    def __repr__(self):
        return "<CommentHistory(id='%s', server_id = %s, comment='%s, op_comments='%s', update_time='%s')>" % (
            self.id, self.domain_id, self.comment, self.op_comments, self.update_time)


class SaltReturns(Base):
    __tablename__ = "salt_returns"

    job_id = Column("job_id", String(255), primary_key=True, nullable=False, unique=True)
    minion_id = Column("minion_id", String(255), nullable=False)
    fun = Column("fun", String(50), nullable=False)
    success = Column("success", String(10))
    ret = Column("return", Text)
    full_ret = Column("full_ret", Text)
    operation_id = Column("operation_id", String(32), nullable=False)
    user_id = Column("user_id", Integer, nullable=False)
    project_id = Column("project_id", Integer, nullable=False)
    set_id = Column("set_id", Integer, nullable=False)
    start_time = Column("start_time", String(64), nullable=False)
    alter_time = Column("alter_time", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
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

    id = Column("id", String(128), primary_key=True, nullable=False, unique=True)
    domain = Column("domain", String(64), default="NULL")
    stat = Column("stat", String(16), default="NULL")
    ip_ex = Column("ip_ex", String(16), default="NULL")
    ip_in = Column("ip_in", String(16), unique=True, default="NULL")
    host_ip = Column("host_ip", String(16), default="NULL")
    project_id = Column("project_id", Integer, default="NULL")
    idc = Column("idc", String(64), default="NULL")
    usages = Column("usages", String(128), default="NULL")
    os = Column("os", String(32), default="NULL")
    cpu = Column("cpu", String(32), default="NULL")
    memory = Column("memory", String(32), default="NULL")
    disk = Column("disk", String(32), default="NULL")
    pool = Column("pool", String(32), default="NULL")
    comment = Column("comment", String(255), default="NULL")
    update_time = Column("update_time", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    visible = Column("visible", Integer, default="NULL")

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

    id = Column("id", Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    server_id = Column("server_id", Integer, nullable=False)
    set_id = Column("set_id", Integer, nullable=False)

    def __repr__(self):
        return "<Server_Set(id='%s', server_id = %s, set_id='%s')>" % (self.id, self.server_id, self.set_id)


class Set(Base):
    __tablename__ = "set"

    id = Column("id", Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = Column("name", String(32), nullable=False, unique=True)
    project_id = Column("project_id", Integer, nullable=False)
    create_userid = Column("create_userid", Integer, nullable=False)
    create_time = Column("create_time", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    def __repr__(self):
        return "<Set(id='%s', name = %s, project_id='%s')>" % (self.id, self.name, self.project_id)


class Action(Base):
    __tablename__ = "action"

    id = Column("id", Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = Column("name", String(32), nullable=False)
    path = Column("path", String(32))
    set_id = Column("set_id", Integer, nullable=False)

    def __repr__(self):
        return "<Set(id='%s', name = %s, path='%s, set_id='%s')>" % (self.id, self.name, self.path, self.set_id)


class Domain(Base):
    __tablename__ = "domain_info"

    domain_id = Column("domain_id", Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    domain_name = Column("domain_name", String(64), unique=True, nullable=False)
    project_id = Column("project_id", Integer)
    project_name = Column("project_name", String(64), default="NULL")
    ip_source = Column("ip_source", String(16), default="NULL")
    status = Column("status", String(64), default="NULL")
    cdn_hightanti = Column("cdn_hightanti", String(64), default="NULL")
    pre_domain_id = Column("pre_domain_id", Integer, nullable=False, default=0)
    functions = Column("functions", String(255), default="NULL")
    comments = Column("comments", String(255), default="NULL")
    op_comments = Column("op_comments", String(255), default="NULL")
    is_public = Column("is_public", Integer, default=0)
    register = Column("register", String(64), default="NULL")
    register_date = Column("register_date", TIMESTAMP, server_default="NULL")
    domain_DNS = Column("domain_DNS", String(64), default="NULL")
    expiration = Column("expiration", TIMESTAMP, server_default="NULL")
    init_time = Column("init_time", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    dml_time = Column("dml_time", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    dml_flag = Column("dml_flag", Integer, default=1)

    def __repr__(self):
        return "<Domain(domain_id='%s',\
                       domain_name ='%s',\
                       project_id ='%s',\
                       project_name='%s',\
                       ip_source='%s',\
                       status='%s',\
                       cdn_hightanti='%s',\
                       pre_domain_id='%s',\
                       functions='%s',\
                       comments='%s',\
                       op_comments='%s',\
                       is_public='%s',\
                       register='%s',\
                       register_date='%s',\
                       domain_DNS='%s',\
                       expiration='%s',\
                       init_time='%s',\
                       dml_time='%s',\
                       dml_flag='%s')>" % (self.domain_id,
                                           self.domain_name,
                                           self.project_id,
                                           self.project_name,
                                           self.ip_source,
                                           self.status,
                                           self.cdn_hightanti,
                                           self.pre_domain_id,
                                           self.functions,
                                           self.comments,
                                           self.op_comments,
                                           self.is_public,
                                           self.register,
                                           self.register_date,
                                           self.domain_DNS,
                                           self.expiration,
                                           self.init_time,
                                           self.dml_time,
                                           self.dml_flag)


class Redis(Base):
    __tablename__ = "redis_info"

    redis_id = Column("redis_id", Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    project_id = Column("project_id", Integer)
    project_name = Column("project_name", String(64), default="NULL")
    command = Column("command", String(256), default="NULL")
    status = Column("status", Integer, default="NULL")
    redis_file_path = Column("redis_file_path", String(256), default="NULL")
    redis_filename = Column("redis_filename", String(256), default="NULL")
    apply_user_id = Column("apply_user_id", Integer, default="NULL")
    init_time = Column("init_time", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    dml_time = Column("dml_time", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    dml_flag = Column("dml_flag", Integer, default=1)

    def __repr__(self):
        return "<Redis(redis_id='%s',\
                       command ='%s',\
                       project_id = '%s',\
                       project_name = '%s',\
                       status='%s',\
                       redis_file_path='%s',\
                       redis_filename='%s',\
                       apply_user_id='%s',\
                       init_time='%s',\
                       dml_time='%s',\
                       dml_flag='%s')>" % (self.redis_id,
                                           self.command,
                                           self.project_id,
                                           self.project_name,
                                           self.status,
                                           self.redis_file_path,
                                           self.redis_filename,
                                           self.apply_user_id,
                                           self.init_time,
                                           self.dml_time,
                                           self.dml_flag)


class Datadict(Base):
    __tablename__ = "system_datadict"

    id = Column("id", Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    pre_id = Column("pre_id", Integer, nullable=False)
    name = Column("name", String(64), nullable=False)
    init_time = Column("init_time", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    dml_time = Column("dml_time", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    dml_flag = Column("dml_flag", Integer, default=1)
    value = Column("value", String(64), default="NULL")


    def __repr__(self):
        return "<Datadict(id='%s',\
                       pre_id = '%s',\
                       name = '%s',\
                       init_time='%s',\
                       dml_time='%s',\
                       dml_flag='%s',\
                       value='%s')>" % (self.id,
                                        self.pre_id,
                                        self.name,
                                        self.init_time,
                                        self.dml_time,
                                        self.dml_flag,
                                        self.value)


class Menu(Base):
    __tablename__ = "ops_menu"

    mid = Column("mid", Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    preid = Column("preid", Integer, nullable=False, default=0)
    name = Column("name", String(32), nullable=False)
    keys = Column("keys", String(32), nullable=False)
    url = Column("url", String(128), nullable=False)
    is_func = Column("is_func", Integer, nullable=False, default=1)
    level = Column("level", Integer, nullable=False, default=1)
    status = Column("status", Integer, nullable=False, default=1)
    dml_time = Column("dml_time", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    dml_flag = Column("dml_flag", Integer, default=1)


    def __repr__(self):
        return "<Datadict(mid='%s',\
                       preid = '%s',\
                       name = '%s',\
                       keys = '%s',\
                       url = '%s',\
                       is_func = '%s',\
                       level = '%s',\
                       status = '%s',\
                       dml_time='%s',\
                       dml_flag='%s')>" % (self.mid,
                                           self.preid,
                                           self.name,
                                           self.keys,
                                           self.url,
                                           self.is_func,
                                           self.level,
                                           self.status,
                                           self.dml_time,
                                           self.dml_flag)


class MenuPrivilege(Base):
    __tablename__ = "ops_priv_data"

    uid = Column("uid", Integer, nullable=False, primary_key=True, unique=True)
    mid = Column("mid", Integer, nullable=False, primary_key=True, unique=True)
    pid = Column("pid", Integer, nullable=False, primary_key=True, unique=True)
    r_priv = Column("r_priv", Integer, nullable=False, default=0)
    w_priv = Column("w_priv", Integer, nullable=False, default=0)
    dml_time = Column("dml_time", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    dml_flag = Column("dml_flag", Integer, default=1)


    def __repr__(self):
        return "<Datadict(uid='%s',\
                       mid = '%s',\
                       pid = '%s',\
                       r_priv = '%s',\
                       w_priv = '%s',\
                       dml_time='%s',\
                       dml_flag='%s')>" % (self.uid,
                                           self.mid,
                                           self.pid,
                                           self.r_priv,
                                           self.w_priv,
                                           self.dml_time,
                                           self.dml_flag)

