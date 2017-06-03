import json
from datetime import datetime

from flask import request, url_for, redirect,render_template, current_app,g
from flask_json import json_response, as_json
from flask_login import logout_user, login_user, login_required, current_user
from sqlalchemy.sql import text

from util import util


app=current_app
lm = current_app.login_manager
db=g.db

#@view_config(route_name='test_url', renderer='json')
def test_url(request):
    return None

#@extdirect_method(action='dict',request_as_last_param=True)
def get_model(params,request):
    '''
    get model defination
    '''
    prop_list=[]
    sql_text=None
    if not params:
        params=request.params
    if params['type']=='db_table':
        sql_text="select * from "+params['value']+" where rownum<1"
    if params['type']=='db_sql':
        sql_text="select * from ( "+params['value']+" ) where rownum<1"
    if sql_text:
        resultProxy = db.execute(text(sql_text))
        resultProxy.close()
        for col_name in resultProxy.keys():
            prop_list.append(col_name.lower())
    if params['type']=='cls_name':
        cls_name=params['value']
        d = cls_name.rfind(".")
        module=__import__(cls_name[0:d], globals(), locals(), [cls_name[d+1:len(cls_name)]])
        cls=getattr(module,cls_name[d+1:len(cls_name)])
        for attr in cls.__dict__.keys():
            if not attr.startswith("_"):
                prop_list.append(attr)
    if params['type']=='table':
        table=params['value']
        for t in db.Model.metadata.sorted_tables:
            if t.name==table:
                prop_list.append(t.columns.keys())
                break
    return json_response(fields=[dict(name=prop) for prop in prop_list])
