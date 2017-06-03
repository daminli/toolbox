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
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from flask import g

from util.id_generator import IdGenerator

db=g.db

class DataSource(db.Model):
    '''
    the data base connection
    '''
    __tablename__ = 'sys_data_source'
    name = Column('name',String(30),primary_key=True)
    user_name = Column('user_name',String(30))
    _password = Column('password',String(30))
    db_connect = Column('db_connect',String(300))
    ds_type = Column('ds_type',String(32)) #sqlalchemy , cx_oracle 
    ds_group = Column('ds_group',String(32))
    pool_min=Column('pool_min',Integer)
    pool_max=Column('pool_max',Integer)
    pool_step=Column('pool_step',Integer)
    creation_date = Column('sys_creation_date',DateTime,default =datetime.now)
    last_modified_date = Column('sys_last_modified_date',DateTime,default =datetime.now)
    last_modified_by = Column('sys_last_modified_by',String(30))
    create_by = Column('sys_create_by',String(30))
    
    @hybrid_property
    def password(self):
        return base64.decodestring(self._password)

    @password.setter
    def password(self,password):
        self._password = base64.encodestring(password)
        
    def create_pool(self):
        self.engine=create_engine('oracle://'+self.user_name+':'+self.password+'@'+self.db_connect,pool_size=10, max_overflow=20)
        self.null_pool_engine = create_engine('oracle://'+self.user_name+':'+self.password+'@'+self.db_connect,poolclass=NullPool)
        #=======================================================================
        # if self.ds_type=='sqlalchemy' or self.ds_type==None:
        #     self.engine=create_engine('oracle://'+self.user_name+':'+self.password+'@'+self.db_connect)
        # if self.ds_type=='cx_oracle':
        #     #dsn_tns = cx_Oracle.makedsn('localhost', 1521, 'XE')
        #     self.engine = cx_Oracle.SessionPool(user=self.user_name,password=self.password,dsn=self.db_connect,min=1,max=5,increment=1)
        #=======================================================================  
        
class DataSourceEngine:
    '''
    the class to maintain the datasource
    '''
    _engine_list = {}
        
    def __init__(self,ds_name):
        if ds_name not in DataSourceEngine._engine_list:
            ds=db.query(DataSource).filter(DataSource.name==ds_name).first()
            if ds:
                ds.create_pool()
                DataSourceEngine._engine_list[ds_name]=ds
        self.datasource=DataSourceEngine._engine_list[ds_name]
        self.engine=self.datasource.engine
        self.null_pool_engine=self.datasource.null_pool_engine
        self.name=ds_name