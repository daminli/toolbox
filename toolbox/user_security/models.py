# coding=utf-8
'''
Created on 2013-4-24

@author: lidm1
'''
from datetime import date,datetime,timedelta

from flask import current_app,g
from sqlalchemy import (DateTime,String,Column,Text,Integer,Boolean,Date)
from sqlalchemy.orm import validates,relationship, backref
from flask_sqlalchemy_cache import CachingQuery

from flask_login import UserMixin

db=g.db
 
class UserList(db.Model):
    __tablename__ = 'user_list'
    query_class = CachingQuery
    login_name=Column('login_name',String(32),primary_key=True)
    first_name = Column('first_name',String(20))
    last_name = Column('last_name',String(20))
    user_password = Column('user_password',String(64))
    pwd_exp_date = Column('pwd_exp_date',Date)
    status = Column('status',String(10))
    user_grp_id=Column('user_grp_id',String(32))
    email_address = Column('email_address',String(64))
    session_token=Column('session_token',String(64))
    last_login=Column('last_login',DateTime)
    last_session=Column('last_session',DateTime)
    org_name = Column('org_name',String(64))
    country = Column('country',String(10))
    state = Column('state',String(30))
    phone = Column('phone', String(40))
    
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return self.session_token

class UserActivity(db.Model):
    __tablename__ = 'user_activity'
    id = Column('id',String(64),primary_key=True)
    name = Column('name',String(64))
    activity_type = Column('activity_type',String(10))

class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = Column('id',String(64),primary_key=True)
    name = Column('name',String(64))
    
class UserGroup(db.Model):
    __tablename__ = 'user_group'
    id = Column('id',String(64),primary_key=True)
    name = Column('name',String(64))
    
class UserRoleTemplate(db.Model):
    __tablename__ = 'user_role_template'
    role_id = Column('role_id',String(64),primary_key=True)
    activity_id = Column('activity_id',String(64),primary_key=True)
    access_level = Column('access_level',String(64))

class UserGrpRoleMap(db.Model):
    __tablename__ = 'user_grp_role_map'
    user_grp_id = Column('user_grp_id',String(64),primary_key=True)
    role_id = Column('role_id',String(64),primary_key=True)