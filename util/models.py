# coding=utf-8
'''
Created on 2013-7-24  @author: lidm1
'''

from datetime import datetime
import types

from sqlalchemy import (DateTime,String,Column,Text,Integer,Boolean,text)
from sqlalchemy.orm import (validates,relationship, backref)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import (event,Index)
from pyramid import config
#from history_meta import Versioned, versioned_session

from util.id_generator import IdGenerator
import cfg

DBSession=cfg.DBSession
Base=cfg.Base

class ChangeHeader(Base):
    '''
    Change Header Table
    This table used to store all objects change log when __audit_trail__ = True
    '''
    __tablename__='sys_change'
    id=Column('id',String(15),primary_key=True,default=IdGenerator('CHEADER').nextval)
    objectcls=Column('OBJECTCLS',String(32),nullable=False,doc='object class name')
    objectid=Column('objectid',String(96),nullable=False,doc='object id generate from primary key split by "|"')
    changed_by=Column('changed_by',String(32),nullable=False,doc='who did the change')
    changed_date=Column('change_date',DateTime,nullable=False,default=datetime.now,doc='change time')
    action=Column('action',String(96),nullable=False,doc='the action which change was made')
    change_type=Column('change_type',String(1),nullable=False,doc='change type [I,U,D]')

class ChangeDetail(Base):
    '''
    the change detail information
    the old new value for each field
    '''
    __tablename__='sys_change_detail'
    id=Column('id',String(15),primary_key=True,default=IdGenerator('CLINE').nextval)
    change_id=Column('change_id',String(15),nullable=False,doc='change herder ref to ChangeHeader class')
    table_name=Column('table_name',String(30),nullable=False,doc='changed table name')
    fname=Column('fname',String(30),nullable=False)
    old_value=Column('old_value',String(300))
    new_value=Column('new_value',String(300))
    

class BaseTable(object):
    '''
    ent_status： [ACTIVE,DELETED] usered to logic deleted
    modified_date : last modified date for this record
    modified_by: last modified user id
    create_date : creation data  for this record
    create_by :  who create this record
    '''
    __audit_trail__=False
    @classmethod
    @declared_attr
    def ent_status(cls):
        return Column('sys_ent_status',String(10),default='ACTIVE')
    @classmethod
    @declared_attr
    def modified_date(cls):
        return Column('sys_modified_date',DateTime)
    @classmethod
    @declared_attr
    def modified_by(cls):
        return Column('sys_modified_by',String(32))
    @classmethod
    @declared_attr
    def creation_date(cls):
        return Column('sys_creation_date',DateTime)
    @classmethod
    @declared_attr
    def creation_by(cls):
        return Column('sys_created_by',String(32))
        
class TestBaseTable(BaseTable,Base):
    __tablename__='TEST_BASE_TABLE'
    __audit_trail__=True
    id=Column('id',String(32),primary_key='True')
    
@event.listens_for(TestBaseTable, 'before_insert')    
def before_insert(mapper, connection, target):
    target.creation_by='lidm1'
    target.creation_date=datetime.now()
    if target.__audit_trail__:
        print(target)
        
@event.listens_for(TestBaseTable, 'before_update')    
def before_update(mapper, connection, target):
    target.modified_by='lidm1'
    target.modified_date=datetime.now()
    if target.__audit_trail__:
        print(target)