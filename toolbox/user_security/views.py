# coding=utf-8
'''
Created on 2013-4-24

@author: lidm1
'''
import uuid ,json
from flask import request, url_for,session, redirect,render_template, current_app,g
from flask_json import json_response
from flask_login import logout_user, login_user, current_user
from .models import UserList
from datetime import date,datetime,timedelta
from flask_sqlalchemy_cache import FromCache

from ldap3 import Server, Connection, ALL

from . import auth

app=current_app
lm = current_app.login_manager
db=g.db
cache=g.cache

@lm.user_loader
def load_user(session_token):
    #app.logger.debug('Cache load:'+session_token)
    user=UserList.query.options(FromCache(cache)).filter(UserList.session_token==session_token).first()
    if user:
        #app.logger.debug('Cache load User:'+str(user))
        pass
    else:
        #app.logger.debug('DB load:'+session_token)
        user = UserList.query.filter(UserList.session_token==session_token).first()
        #app.logger.debug('DB load User:'+str(user))
    return user

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    """
    forbidden view
    when user haven't login, the request will redirect to the login page
    """
    session_id = request.args.get('sid',None)
    if session_id:
        result=sso_validlogin(session_id)
        if result['success']:
            user=UserList(login_name='lidm1',session_token=uuid.uuid1(),last_login_time=datetime.now())
            login_user(user, remember=True)
            #remove sid='' from query string, to avoid endless loop
            query_string=''
            for key in request.GET:
                if key!='sid':
                    query_string=query_string+key+'='+request.GET[key]
            if query_string:
                query_string='?'+query_string
            return redirect(location = request.current_route_url()+query_string)
    next_page = request.values.get('next',None)
    return render_template('login.html',next_page=next_page)

@auth.route('/valid_login', methods = ['POST','GET'])
def valid_login():
    """
    valid user login
    params : username,password
    """
    app.logger.debug(request.values)
    app.logger.debug(request.get_data())
    if request.values.get('username',None):
        params=request.values
    else:
        params=json.loads(request.get_data())
        
    user_name= params.get('username',None)
    password= params.get('password',None)
    if user_name and password:
        result = on_validlogin(user_name, password)
        if result["success"]:
            login_user(result['user'], remember=True)
            return json_response(success=True,redirect= url_for('init_page'))
        return json_response(success=False,errors=result['errors'])
    else:
        return json_response(success=False,errors=dict(message='username or password miss'))
    
@auth.route('/logout', methods = ['GET', 'POST'])
def logout(request):
    """
    logout remove the user from http headers 
    Redirect to the login page 
    """
    logout_user()
    return redirect(url_for('ext_page',package='main',page='Login'))
    
  
def on_validlogin(user_name, password):
    '''
      Validate username and password by AD
      :param user_name: The user login name.
      :type user: string
      :param password: The user password
      :type password: string    
    '''
    def update_user_attr(user_obj,user_entry):
        USER_ATTR_MAP = {'login_name':'sAMAccountName',
                         'first_name':'givenName',
                         'last_name':'sn',
                         'user_password':'sAMAccountName',
                         'email_address':'mail',
                         'org_name':'department',
                         'country':'c',
                         'state':'l',
                         'phone':'telephoneNumber'}
        for key,value in USER_ATTR_MAP.items():
            setattr(user_obj,key,getattr(user_entry,value).value)
            
    server = "ldap://lenovo.com:389"
    conn = Connection(server, 'lenovo\\'+user_name, password)
    if conn.bind():
        search_attrs = ['name', 'userPrincipalName','departmentNumber', 'telephoneNumber', 'department','sAMAccountName', 'mail', 'manager', 'title', 'employeeType', 'l', 'c','employeeNumber', 'displayName','givenName','sn']
        conn.search('dc=lenovo,dc=com', '(sAMAccountName='+user_name+')',attributes=search_attrs)
        user_entry = conn.entries[0]
        conn.unbind()
    else:
        return dict(success=False, 
                errors=dict(status='FAILED',
                           password= "invalid password"
        ))
    
    result = {}
    user = UserList.query.filter_by(login_name=user_name).first()
    if not user:
        user = UserList()
        result = dict(success=False,errors=dict(status='NEW',username= "New user created."))
        user.status = 'NEW'
        user.pwd_exp_date =  datetime(9999,12,31)
        user.user_grp_id = 'default'
    elif user.status=='INACTIVE':
        result = dict(success=False,errors=dict(status='INACTIVE',username= "User is inactive."))
    #elif user.pwd_exp_date<date.today():
        #result = dict(success=False,errors=dict(status='EXPIRED',username= "User is expired."))
    user.session_token=str(uuid.uuid1())
    user.last_login=datetime.now()
    user.last_session=datetime.now()
    update_user_attr(user,user_entry)
    db.session.merge(user)
    db.session.commit()
    if not result:
        result = dict(success=True,user=user)
    return result

def sso_validlogin(sid):
    '''
    data_source = DataSourceEngine('PRDPORTAL')
    conn = data_source.engine.connect()
    trans  = conn.begin()
    result=[]
    try:
        resultProxy = conn.execute('select * from PT_USER_LOGIN_LOG where sessionid =:sid and login_time>:login_time',dict(sid=sid,login_time=datetime.now()-timedelta(days=3.0/24.0)))
        result = resultProxy.first()
        resultProxy.close()
    finally:
        trans.commit()
        conn.close()
    print(result)
    if result:
        return dict(success=True,data=dict(user_name=result.login_name))
    else:
        return dict(success= False)
        '''
    return dict(success=False,data=dict(user_name='lidm1'))

@auth.route('/check', methods = ['GET', 'POST'])
def check():
    #app.logger.debug(str(session));
    try:
        if current_user.login_name:
            return json_response(headers_={'X-Viewer':'viewer'},user_name=current_user.login_name)
    except Exception as e:
        return json_response(status_=401)