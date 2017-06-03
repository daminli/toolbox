# coding=utf-8
'''
Created on 2014-2-22

@author: lidm1
'''
from datetime import datetime
import types
from xml.etree import ElementTree

from sqlalchemy import (DateTime,String,Column,Text,Integer,Boolean,Index)
from sqlalchemy.orm import (validates,relationship, backref)
from sqlalchemy import (text)
from pyramid import config
from ..common.smart_table import SmartTable


from util.id_generator import IdGenerator
import cfg
from tasks import Task

Base=cfg.Base

class Action(Base,SmartTable):
    '''
    action type:  
      different action type with different config param
    procedure:
     procedure_name : XXX
    
    TS Workflow:
     run_id : 
     config_id : 
     workflow_name :
     attach params:
     <ROOT>
        <PROCEDURE_NAME Value=""/>
     </ROOT>
     
     function: 
       function name : module.function_name
     
     abpp post:
    '''
    __tablename__ = 'px_action'
    ui_name = Column('ui_name',String(64),primary_key=True)
    action_name = Column('action_name',String(64),primary_key=True)
    action_type=Column('action_type',String(32)) # procedure, ts workflow, function, abpp post
    is_sync=Column('is_sync',Boolean,default=True)
    action_detail=Column('action_detail',Text)
    
    def execute(self,params):
        task=Task(self)
        return task.execute(params)
        
    
class UI(Base,SmartTable):
    __tablename__='px_ui'
    name = Column('name',String(64),primary_key=True)
    ui_desc=Column('ui_desc',String(124),nullable=False)
    url=Column('url',String(124),nullable=False)
    
class Navigation(Base,SmartTable):
    __tablename__='px_navagation'
    id=Column('id',String(32),primary_key=True,default = IdGenerator('NVL_ID').nextval)
    parent_id=Column('parent_id',String(32),nullable=False) #0 means root
    type=Column('type',String(32),nullable=False) #folder or item
    display_name=Column('display_name',String(64),nullable=False)
  
class TaskQueue(Base):
    __tablename__='z_ui_task_queue'
    instance_id = Column('id',String(32),primary_key=True)
    event_name = Column('event_name',String(100))
    run_by = Column('ui_user_id',String(62))
        
class TaskLog(Base):
    __tablename__='px_task_log'
    id = Column('id',String(32),primary_key=True,default = IdGenerator('TASK_ID').nextval)
    task_name = Column('task_name',String(64),nullable=False) #ui_name.action_name
    task_type=Column('task_type',String(64),nullable=False)
    start_time=Column('start_time',DateTime)
    end_time=Column('start_time',DateTime)
    status=Column('status',String(32)) # wait running completed failed cancel
    run_by=Column('run_by',String(64))
    raw_input = Column('raw_data',Text) # original input from extjs
    input_data=Column('input_data',Text) # input data to procedure or workflow
    output_data=Column('output_data',Text)
    
class TaskLogProc(Base):
    __tablename__='px_task_log_proc'
    id=Column('id',String(32),primary_key=True)
    task_id = Column('task_id',String(32))
    
    
class TaskInstance(Base):
    __tablename__='px_task_instance'
    id = Column('id',String(32),primary_key=True)
    task_detail=Column('task_detail',Text)
    sys_timestamp=Column('sys_timestamp',DateTime,default =datetime.now)
    