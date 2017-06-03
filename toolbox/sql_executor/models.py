# coding=utf-8
'''
Created on 2013-5-8

@author: lidm1
'''
import base64
from datetime import datetime

from sqlalchemy import (DateTime,String,Column,Text,Integer,Boolean)
from sqlalchemy.orm import validates,relationship, backref
from sqlalchemy import text
from sqlalchemy.ext.hybrid import hybrid_property
from flask import g

from util.id_generator import IdGenerator

db=g.db

class ExecHistory(db.Model):
    '''
    request a new run
    '''
    __tablename__ = 'exec_history'
    id = Column('id',String(32),primary_key=True,default = IdGenerator('EXEC_HISTORY').nextval)
    summary = Column('summary',Text)
    creation_date = Column('creation_date',DateTime,default=datetime.now)
    create_by = Column('create_by',String(32))
    
class ExecRunLog(db.Model):
    '''
     log when each time user click execute button
    '''
    __tablename__ = 'exec_run_log'
    id = Column('id',String(32),primary_key=True,default = IdGenerator('EXEC_RUN').nextval)
    exec_id = Column('exec_id',String(32))
    data_source = Column('data_source',String(30))
    start_time = Column('start_time',DateTime)
    end_time = Column('end_time',DateTime)
    script = Column('script',Text)
    result = Column('result',Text)
    run_by = Column('create_by',String(32))
    status = Column('status',String(32))
    
class ExecRunDetail(db.Model):
    '''
    log for each sql in script
    '''
    __tablename__ = 'exec_run_detail'
    id = Column('id',String(32),primary_key=True,default = IdGenerator('EXEC_SQL').nextval)
    run_id = Column('run_id',String(32))
    sql_text = Column('sql_text',Text)
    start_time = Column('start_time',DateTime)
    end_time = Column('end_time',DateTime)
    result = Column('result',Text)
    status = Column('status',String(10))
    run_by = Column('run_by',String(32))
