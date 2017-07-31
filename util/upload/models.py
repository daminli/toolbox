# coding=utf-8
from sqlalchemy_utils.asserts import assert_non_nullable
from datashape.typesets import boolean
'''
Created on 2013-5-8

@author: lidm1
'''
import base64
from datetime import datetime

from flask import g
from flask_login import current_user
from sqlalchemy import (DateTime,String,Column,Text,Integer,Boolean)
from sqlalchemy.orm import validates,relationship, backref
from sqlalchemy import text
from sqlalchemy.ext.hybrid import hybrid_property

from util.id_generator import IdGenerator
from util.datasource.models import  DataSourceEngine

db=g.db

class UploadTemplate(db.Model):
    __doc__='table for upload template'
    __tablename__ = 'sys_upload_template'
    template_id = Column('template_id',String(64),primary_key=True)
    api_name = Column('api_name',String(64),nullable=False)
    api_before = Column('api_before',String(64))
    api_after = Column('api_after',String(64))
    data_type = Column('data_type',String(30),info='[xlsx,json,xml]',nullable=False,default='xlsx')
    start_line = Column('start_line',Integer,nullable=False,default=1)
    has_title = Column('has_title',Boolean,nullable=False,default=True)
    api_mode = Column('api_mode',String(10),info='[row,batch]',nullable=False,default='row')
    creation_date = Column('creation_date',DateTime,default=datetime.now)
    create_by = Column('create_by',String(32))
    
class UploadProps(db.Model):
    __doc__='table for upload template props'
    __tablename__ = 'sys_upload_props'
    template_id = Column('template_id',String(64),primary_key=True)
    title_name = Column('title_name',String(64),primary_key=True)
    seq_id = Column('seq_id',Integer,nullable=False)
    prop_name = Column('prop_name',String(30),nullable=False)
    is_required = Column('is_required',Boolean,nullable=False,default=False)
    title_type = Column('type_name',String(10),info='[rule,text]')
    title_prop_name = Column('title_prop_name',String(30))
    
class UploadLog(db.Model):
    __doc__='table for upload template props'
    __tablename__ = 'sys_upload_log'
    upload_id = Column('upload_id',String(64),primary_key=True)
    template_id = Column('template_id',String(64),primary_key=True)
    tot_rows = Column('tot_rows',Integer)
    suc_rows = Column('suc_rows',Integer)
    error_rows = Column('error_rows',Integer)
    data_details=Column('data_details',Text)
    upload_date = Column('upload_date',DateTime,default=datetime.now)
    upload_by = Column('upload_by',String(32))
    
def init_upload_tempate(template_list):
    upld_templates=[]
    id_list=[]
    upld_props=[]
    for template in template_list:
        id_list.append(template.get('template_id'))
        upld_template=UploadTemplate();
        upld_template.template_id=template.get('template_id')
        upld_template.api_name=template.get('api_name')
        upld_template.api_before=template.get('api_before',None)
        upld_template.api_after=template.get('api_after',None)
        upld_template.data_type=template.get('data_type','xslx')
        upld_template.start_line=template.get('start_line',1)
        upld_template.has_title=template.get('has_title',True)
        upld_template.api_mode=template.get('api_mode','row')
        upld_template.creation_date = datetime.now()
        upld_template.create_by = current_user.login_name
        i=0
        for prop in template.get('upload_props'):
            upld_prop=UploadProps()
            upld_prop.template_id=template.get('template_id')
            i=i+1
            upld_prop.seq_id=i
            upld_prop.title_name=prop.get('title_name')
            upld_prop.prop_name=prop.get('prop_name')
            upld_prop.is_required=prop.get('is_required',False)
            upld_prop.title_type=prop.get('title_type','text')
            upld_prop.title_prop_name=prop.get('title_prop_name',None)
            upld_prop.creation_date = datetime.now()
            upld_prop.create_by = current_user.login_name
            upld_props.append(upld_prop)
        upld_templates.append(upld_template)
    UploadTemplate.query.filter(UploadTemplate.template_id.in_(id_list)).delete(synchronize_session=False)
    UploadProps.query.filter(UploadProps.template_id.in_(id_list)).delete(synchronize_session=False)
    db.session.add_all(upld_templates)
    db.session.add_all(upld_props)
    db.session.flush()
    db.session.commit()
    return template_list