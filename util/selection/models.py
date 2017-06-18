# coding=utf-8
'''
Created on 2013-5-8

@author: lidm1
'''
import base64
from datetime import datetime

from flask import g
from sqlalchemy import (DateTime,String,Column,Text,Integer,Boolean)
from sqlalchemy.orm import validates,relationship, backref
from sqlalchemy import text
from sqlalchemy.ext.hybrid import hybrid_property

from util.id_generator import IdGenerator
from util.datasource.models import  DataSourceEngine

db=g.db

class CodeType(db.Model):
    '''
    the code type for selection
    '''
    __tablename__ = 'sys_code_type'
    type_id = Column('type_id',String(30),primary_key=True)
    type_name = Column('type_name',String(30))
    parent_type_id = Column('parent_type_id',String(30))
    
class CodeValue(db.Model):
    '''
    the code value for selection
    '''
    __tablename__ = 'sys_code_value'
    id = Column('id',String(30),primary_key=True,default=IdGenerator('CODE_ID').nextval)
    type_id = Column('type_id',String(30))
    value_id = Column('value_id',String(30))
    value_name = Column('value_name',String(30))
    parent_id = Column('parent_id',String(30))
    
class Selection(db.Model):
    '''
    the code value for selection
    '''
    __tablename__ = 'sys_selection'
    name = Column('name',String(30),primary_key=True)
    type = Column('type',String(30))
    config = Column('config',Text)
    datasource=Column('datasource',String(32))
     
    def get_selectlist(self):
        params={}
        if self.type=='code_type':
            sql_text='select value_name "text", value_id "value" from sys_code_type a join sys_code_value b on a.type_id = b.TYPE_ID where a.TYPE_NAME =:type_name  order by text'
            params=dict(type_name=self.config)
        if self.type=='sql':
            sql_text=self.config
        if self.type == 'model':
            pass
        if self.datasource:
            data_source = DataSourceEngine(self.datasource)
            conn = data_source.engine.connect()
            try:
                resultProxy=conn.execute(text(sql_text),params)
                result = resultProxy.fetchall()
                resultProxy.close()
            finally:
                conn.close()
        else:
            resultProxy=db.session.execute(text(sql_text),params)
            result = resultProxy.fetchall()
            resultProxy.close()
            print(text(sql_text))
        return result
        
    
    