'''
Created on 2017Äê6ÔÂ19ÈÕ

@author: lidm1
'''
from datetime import datetime
from sqlalchemy import (Date,DateTime,String,Column,Text,Integer,Boolean)
from sqlalchemy.orm import validates,relationship, backref
from sqlalchemy import text
from sqlalchemy.ext.hybrid import hybrid_property
from flask import g,current_app
from flask_login import current_user

from util.id_generator import IdGenerator
from networkx.algorithms.bipartite.projection import project
from dill.dill import check
from util import common


db=g.db
app=current_app

class Projects(db.Model):
    __tablename__ = 'mgmt_projects'
    project_name = Column('project_name',String(100),primary_key=True,comment='Project Name')
    summary = Column('summary',Text,comment='Summary')
    it_focal = Column('it_focal',String(30),nullable=False,comment='Planning Focal')
    it_leader = Column('it_leader',String(30),nullable=False,comment='IT Leader')
    int_md = Column('int_md',Integer,nullable=False,comment='Total internal MD')
    ext_cost = Column('ext_cost',Integer,nullable=False,comment='Total external Cost$')
    start_month = Column('start_date',Date,nullable=False,comment='Project start month')
    end_month = Column('end_date',Date,nullable=False,comment='Project end month')
    creation_date = Column('creation_date',DateTime,default=datetime.now,comment='Create Date')
    create_by = Column('create_by',String(32),default=current_user.login_name,comment='Create By')

class CurvePlan(db.Model):
    __tablename__='mgmt_projects_curve'
    project_name = Column('project_name',String(100),primary_key=True,comment='Project Name')
    resource_name = Column('resource_name',String(30),primary_key=True,comment='Resource Name')
    module_name = Column('module_name',String(100),comment='Module Name')
    checker = Column('checker',String(30),nullable=False,comment='Checker',doc='internal resource manager is checker; external resource module focal is checker')
    month_date = Column('month_code',Date,primary_key=True,comment='Month Date')
    man_day = Column('man_day',Integer,nullable=False,default=0,comment='Man Days')
    creation_date = Column('creation_date',DateTime,default=datetime.now,comment='Create Date')
    create_by = Column('create_by',String(32),default=current_user.login_name,comment='Create By')
    
class ActualRMS(db.Model):
    __tablename__='mgmt_rms_data'
    creation_date = Column('creation_date',DateTime,default=datetime.now,comment='Create Date')
    create_by = Column('create_by',String(32),default=current_user.login_name,comment='Create By')

class Resources(db.Model):
    __tablename__='mgmt_resources'
    resource_name = Column('resource_name',String(30),primary_key=True,comment='Resource Name')
    team_name = Column('team_name',String(100),nullable=False,comment='Team/Company Name')
    module_name = Column('module_name',String(100),comment='Module Name')
    resource_type = Column('resource_type',String(30),nullable=False,default='internal',comment='internal/external')
    resource_rate = Column('resource_rate',Integer,nullbale=False,comment='Rate(£¤)')
    creation_date = Column('creation_date',DateTime,default=datetime.now,comment='Create Date')
    create_by = Column('create_by',String(32),default=current_user.login_name,comment='Create By')
    
class ActualTimeSheet(db.model):
    __tablename__='mgmt_actural_timesheet'
    resource_name =  Column('resource_name',String(30),primary_key=True,comment='Resource Name')
    project_name =  Column('project_name',String(100),primary_key=True,comment='Project Name')
    work_type = Column('work_type',String(30),comment='By Week/Day')
    work_date = Column('work_date',Date,primary_key=True,comment='Work Date')
    checker = Column('checker',String(30))
    work_hour = Column('work_hour',Integer,nullable=False,comment='Work Hour',default=0)
    creation_date = Column('creation_date',DateTime,default=datetime.now)
    create_by = Column('create_by',String(32),default=current_user.login_name)
    
class WorkCalendar(db.Model):
    __tablename__='mgmt_work_calendar'
    day_date = Column('day_date',Date,primary_key=True,comment='Date')
    is_work = Column('is_work',Boolean,nullable=False,comment='Is Working Day')
    week_date = Column('week_date',Date,comment='Week Date')
    month_date = Column('month_date',Date,comment='Month Date')
    quater_code = Column('quater_code',String(30),comment='Quater')
    half_year_code = Column('half_year_code',String(30),comment='Half Year')
    full_year_code = Column('full_year_code',String(30),comment='Year')

class SpecialWorkDay(db.Model):
    __tablename__='mgmt_special_workday'
    day_date = Column('day_date',Date,primary_key=True,comment='Date')
    is_work = Column('is_work',Boolean,nullable=False,comment='Is Working Day')
    creation_date = Column('creation_date',DateTime,default=datetime.now)
    create_by = Column('create_by',String(32),default=current_user.login_name)
    
        