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

from cfg import *
from util.id_generator import IdGenerator
from toolbox.common.smart_table import SmartTable

class Project(Base):
    '''
    Project information
    Project can be a SR, PB or a Incident which trigger a change
    '''
    __tablename__ = 'z_itsm_project'
    id = Column('id',String(32),primary_key=True)
    category=Column('category',String(10),nullable=False)
    summary = Column('summary',Text,nullable=False)
    status=Column('status',String(10),nullable=False)
    assign_group=Column('assign_group',String(32),nullable=False)
    assignee=Column('assignee',String(32),nullable=False)
    driven_type=Column('type',String(32))
    submit_date=Column('start_time',DateTime,nullable=False)
    mtp_date=Column('mtp_date',DateTime)
    own_attend=Column('own_attend',String(32))
    creation_date = Column('creation_date',DateTime,default =datetime.now)
    create_by = Column('create_by',String(32))
    
class WorkLoad(Base,SmartTable):
    '''
     The detail Task of the project
    '''
    __tablename__ = 'z_itsm_workload'
    id = Column('id',String(32),primary_key=True)
    ref_id = Column('ref_id',String(32),nullable=False)
    assign_group_name=Column('assign_group',String(32),nullable=False)
    assignee=Column('assignee',String(32),nullable=False)
    man_day=Column('man_day',Integer,nullable=False)
    start_time = Column('start_time',DateTime,nullable=False)
    end_time = Column('end_time',DateTime,nullable=False)
    task_detail = Column('task_desc',Text,nullable=False)
    
class MtpWindow(Base):
    '''
    Config the mtp windows
    '''
    __tablename__='conf_mtp_window'
    mtp_date=Column('mtp_date',DateTime,primary_key=True)
    
class IssueCategory(Base):
    '''
    the ticket category useed for ticket analyze  
    '''
    __tablename__='conf_itsm_issue_category'
    module=Column('module',String(32),primary_key=True)
    issue_category=Column('issue_category',String(64),primary_key=True)
    issue=Column('issue',String(64),primary_key=True)
    issue_desc=Column('issue_desc',String(120))
    issue_comment=Column('issue_comment',String(300))
    status=Column('status',String(10))
    
class TicketRootCause(Base):
    '''
    ticket Root Cause Define
    '''
    __tablename__='conf_itsm_root_cause'
    rc_category=Column('rc_category',String(64),primary_key=True)
    root_cause=Column('root_cause',String(64),primary_key=True)
    ud_category=Column('ud_category',String(64))
    status=Column('status',String(10),default='ACTIVE')
    
    
class TicketAnalyze(Base,SmartTable):
    '''
    ticket analyze result
    '''
    __tablename__='z_itsm_ticket_analyze'
    incident_id=Column('incident_id',String(32),primary_key=True)
    rc_category=Column('rc_category',String(64))
    root_cause=Column('root_cause',String(64))
    sub_biz=Column('sub_biz', String(10))
    release=Column('release', String(10))
    issue_category=Column('issue_category',String(64))
    issue=Column('issue',String(64))
    issue_comment=Column('issue_comment',String(300))
    ta_status=Column('ta_status',String(10),default='confirmed')
    problem_category=Column('problem_category',String(64))
    
class TicketUsers(Base):
    '''
    ticket user Information
    '''
    __tablename__='z_itsm_conf_user_info'
    internet_email=Column('internet_email',String(120),primary_key=True)
    itcode=Column('itcode',String(64))
    first_name=Column('first_name',String(64))
    last_name=Column('last_name', String(64))
    email=Column('email', String(120))
    user_type=Column('user_type',String(30))
    org_id=Column('org_id',String(64))
    country=Column('country',String(30))
    state=Column('state',String(30))
    phone=Column('phone',String(64))
    sub_biz=Column('sub_biz',String(64))
    function_group=Column('function_group',String(64))
    

class OperationEvent(Base,SmartTable):
    '''
    the event happen in operation, which will impact the performance of workflow, increase or reduce incident volumn 
    '''
    __tablename__='z_operation_event'
    id=Column('id',String(32),primary_key=True)
    event_name=Column('event_name',String(100),nullable=False)
    event_detail=Column('event_detail',Text,nullable=False)
    start_time = Column('start_time',DateTime,nullable=False)
    end_time = Column('end_time',DateTime,nullable=False)
    module=Column('module',String(32))
    
    