# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) YEAR by lidm1.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""

from datetime import datetime
from sqlalchemy import (Date,DateTime,String,Column,Text,Integer,Boolean)
from sqlalchemy import text
from sqlalchemy.ext.hybrid import hybrid_property
from flask import g,current_app
from flask_login import current_user

from util.id_generator import IdGenerator
from dill.dill import check
from util import common,get_user


db=g.db
app=current_app

class Projects(db.Model):
    __tablename__ = 'mgmt_projects'
    project_name = Column('project_name',String(100),primary_key=True,info=dict(label='Project Name'))
    summary = Column('summary',Text,info=dict(label='Summary'))
    it_focal = Column('it_focal',String(30),nullable=False,info=dict(label='Planning Focal'))
    it_leader = Column('it_leader',String(30),nullable=False,info=dict(label='IT Leader'))
    int_md = Column('int_md',Integer,nullable=False,info=dict(label='Total internal MD'))
    ext_cost = Column('ext_cost',Integer,nullable=False,info=dict(label='Total external Cost$'))
    start_date = Column('start_date',Date,nullable=False,info=dict(label='Project start date'))
    end_date = Column('end_date',Date,nullable=False,info=dict(label='Project end date'))
    creation_date = Column('creation_date',DateTime,default=datetime.now,info=dict(label='Create Date'))
    create_by = Column('create_by',String(32),default=get_user,info=dict(label='Create By'))

class CurvePlan(db.Model):
    __tablename__='mgmt_projects_curve'
    project_name = Column('project_name',String(100),primary_key=True,info=dict(label='Project Name'))
    resource_name = Column('resource_name',String(30),primary_key=True,info=dict(label='Resource Name'))
    module_name = Column('module_name',String(100),info=dict(label='Module Name'))
    checker = Column('checker',String(30),nullable=False,info=dict(label='Checker'),doc='internal resource manager is checker; external resource module focal is checker')
    month_date = Column('month_date',Date,primary_key=True,info=dict(label='Month Date'))
    man_day = Column('man_day',Integer,nullable=False,default=0,info=dict(label='Man Days'))
    creation_date = Column('creation_date',DateTime,default=datetime.now,info=dict(label='Create Date'))
    create_by = Column('create_by',String(32),default=get_user,info=dict(label='Create By'))
    
class ActualRMS(db.Model):
    __tablename__='mgmt_rms_data'
    resource_name =  Column('resource_name',String(30),primary_key=True,info=dict(label='Resource Name'))
    project_name =  Column('project_name',String(100),primary_key=True,info=dict(label='Project Name'))
    bucket_type = Column('bucket_type',String(30),info=dict(label='By Week/Day'))
    work_date = Column('work_date',Date,primary_key=True,info=dict(label='Work Date'))
    checker = Column('checker',String(30),info=dict(label='Checker'))
    work_hour = Column('work_hour',Integer,nullable=False,info=dict(label='Work Hour'),default=0)
    creation_date = Column('creation_date',DateTime,default=datetime.now)
    create_by = Column('create_by',String(32),default=get_user)

class Resources(db.Model):
    __tablename__='mgmt_resources'
    resource_name = Column('resource_name',String(30),primary_key=True,info=dict(label='Resource Name'))
    team_name = Column('team_name',String(100),nullable=False,info=dict(label='Team/Company Name'))
    module_name = Column('module_name',String(100),info=dict(label='Module Name'))
    resource_type = Column('resource_type',String(30),nullable=False,default='internal',info=dict(label='internal/external'))
    resource_rate = Column('resource_rate',Integer,nullable=False,info=dict(label='Rate(RMB)'))
    creation_date = Column('creation_date',DateTime,default=datetime.now,info=dict(label='Create Date'))
    create_by = Column('create_by',String(32),default=get_user,info=dict(label='Create By'))
    
class ActualTimeSheet(db.Model):
    __tablename__='mgmt_actural_timesheet'
    resource_name =  Column('resource_name',String(30),primary_key=True,info=dict(label='Resource Name'))
    project_name =  Column('project_name',String(100),primary_key=True,info=dict(label='Project Name'))
    bucket_type = Column('bucket_type',String(30),info=dict(label='By Week/Day'))
    work_date = Column('work_date',Date,primary_key=True,info=dict(label='Work Date'))
    checker = Column('checker',String(30))
    work_hour = Column('work_hour',Integer,nullable=False,info=dict(label='Work Hour',default=0))
    creation_date = Column('creation_date',DateTime,default=datetime.now)
    create_by = Column('create_by',String(32),default=get_user)
    
class WorkCalendar(db.Model):
    __tablename__='mgmt_work_calendar'
    day_date = Column('day_date',Date,primary_key=True,info=dict(label='Date'))
    is_work = Column('is_work',Boolean,nullable=False,info=dict(label='Is Working Day'))
    week_date = Column('week_date',Date,info=dict(label='Week Date'))
    month_date = Column('month_date',Date,info=dict(label='Month Date'))
    quater_code = Column('quater_code',String(30),info=dict(label='Quater'))
    half_year_code = Column('half_year_code',String(30),info=dict(label='Half Year'))
    full_year_code = Column('full_year_code',String(30),info=dict(label='Year'))

class SpecialWorkDay(db.Model):
    __tablename__='mgmt_special_workday'
    day_date = Column('day_date',Date,primary_key=True,info=dict(label='Date'))
    is_work = Column('is_work',Boolean,nullable=False,info=dict(label='Is Working Day'))
    creation_date = Column('creation_date',DateTime,default=datetime.now)
    create_by = Column('create_by',String(32),default=get_user)