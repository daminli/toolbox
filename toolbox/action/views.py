# coding=utf-8
'''
Created on 2014-2-22

@author: lidm1
'''
import json
from datetime import datetime
import transaction
from xml.etree import ElementTree

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )
from pyramid.view import (
    view_config,
    forbidden_view_config,
    )
from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    )
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from pyramid_extdirect import extdirect_method
import venusian
from pyramid.security import authenticated_userid

import cfg
from util.id_generator import IdGenerator
from models import Action

DBSession = cfg.DBSession

def do_action(params,request):
    context={}
    req_data=request.json
    context['ui_name']=req_data['action']
    context['action']=req_data['method']
    context['user']=authenticated_userid(request)
    context['sid']=request.session.id
    assert(1==2)
    action = DBSession.query(Action).filter(Action.ui_name==req_data['action']).filter(Action.action_name==req_data['method']).first()
    return action.execute(params)

def dic2xml(data):
    #ElementTree
    pass

@extdirect_method(action='action',request_as_last_param=True)
def initial_action_api(reload,request):
    '''
       initial action api to extdirect. then call action in extjs like
       #========================================================================
       # Remote.ui_template.remove({
       #              input_data : "<roo><name>hello world</name></root>"
       #          }, function(result, event) {
       #              console.log(result);
       #              str = Ext.JSON.encode(result);
       #              Ext.ComponentQuery.query("textarea[name='result']")[0].setValue(str);
       #      }); 
       #========================================================================
       
       User can reload the action api from extjs
       #========================================================================
       # Remote.action.initial_action_api(true,function(result, event) {
       #              console.log(result);
       #      });
       #========================================================================
    '''
    actions = DBSession.query(Action).all()
    for action in actions:
        try:
            print(dict(ui_name=action.ui_name,action=action.action_name))
            extdirect_method(action=action.ui_name,method_name=action.action_name,request_as_last_param=True)(do_action)
        except KeyError, e:
            pass
    if reload:
        cfg.config.scan(categories=('extdirect',))  #reload api dict need scan again, because use venusian do decorator actions
        
initial_action_api(False,None)

