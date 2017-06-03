# coding=utf-8
'''
Created on 2013-4-24

@author: lidm1
'''
import uuid 
from flask import request, url_for, redirect,render_template, current_app,g
from flask_json import json_response
from flask_login import logout_user, login_user
from .models import UserList
from datetime import date,datetime,timedelta
from flask_sqlalchemy_cache import FromCache
from . import auth

app=current_app
lm = current_app.login_manager
db=g.db
cache=g.cache

@lm.user_loader
def load_user(session_token):
    app.logger.debug('Cache load:'+session_token)
    user=UserList.query.options(FromCache(cache)).filter(UserList.session_token==session_token).first()
    if user and user.last_session>datetime.now()-timedelta(1):
        app.logger.debug('Cache load User:'+str(user))
    else:
        app.logger.debug('DB load:'+session_token)
        user = UserList.query.filter(UserList.session_token==session_token,UserList.last_session>datetime.now()-timedelta(1)).first()
        app.logger.debug('DB load User:'+str(user))
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
    return render_template('login.html',page='login')

@auth.route('/valid_login', methods = ['POST'])
def valid_login():
    """
    valid user login
    params : userName,password
    """
    user_name= request.values.get('username',None)
    password= request.values.get('password',None)
    result = on_validlogin(user_name, password)
    if result["success"]:
        login_user(result['user'], remember=True)
        return json_response(success=True,redirect= url_for('init_page'))
    return json_response(success=False,errors=result['errors'])
    
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
        
    user = UserList.query.filter_by(login_name=user_name).first()
    if not user:
        return dict(success=False,errors=dict(username= "User is not exists."))
    if user.status!='ACTIVE':
        return dict(success=False,errors=dict(username= "User is inactive."))
    if user.pwd_exp_date<date.today():
        return dict(success=False,errors=dict(username= "User is expired."))
    
    user.session_token=str(uuid.uuid1())
    print(user.session_token)
    user.last_login=datetime.now()
    user.last_session=datetime.now()
    db.session.merge(user)
    db.session.commit()
    '''
    try:
        SERVER = "ldap://lenovo.com:389"
        DN = user_name + "@lenovo.com"
        secret = password
        un = user_name
        l = ldap.initialize(SERVER)
        l.protocol_version = 3
        l.set_option(ldap.OPT_REFERRALS, 0)
        l.simple_bind_s(DN, password)
    except ldap.INVALID_CREDENTIALS:
        return dict(success=False, 
                errors=dict(
                           password= "invalid password"
        ))
    except:
        return dict(success= False, errors=dict(username= 'Login failed. Try again.'))
    '''    
    return dict(success=True,user=user)

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