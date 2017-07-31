import json
from datetime import datetime

from flask import request, url_for, redirect,render_template, current_app,g
from flask_json import json_response, as_json
from flask_login import logout_user, login_user, login_required, current_user
from sqlalchemy.sql import text

import util
from util import common

from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired


app=current_app
lm = current_app.login_manager
db=g.db

@common.route('/get_model',methods = ['GET','POST'])
def get_model():
    '''
    get model defination
    '''
    prop_list=[]
    sql_text=None
    params=request.values
    if db.engine.dialect.name=='oracle':
        row_limit=' where rownum<=1'
    if db.engine.dialect.name in ['postgresql','hana']:
        row_limit=' limit 1'
    if params['type']=='db_table':
        sql_text="select * from "+params['value']+row_limit
    if params['type']=='db_sql':
        sql_text="select * from ( "+params['value']+" ) a"+row_limit
    if sql_text:
        resultProxy = db.session.execute(text(sql_text))
        resultProxy.close()
        for col_name in resultProxy.keys():
            label=" ".join([temp.capitalize() for temp in col_name.split('_')])
            prop_list.append(dict(name=col_name.lower(),label=label))
    if params['type']=='cls_name':
        cls_name=params['value']
        d = cls_name.rfind(".")
        module=__import__(cls_name[0:d], globals(), locals(), [cls_name[d+1:len(cls_name)]])
        cls=getattr(module,cls_name[d+1:len(cls_name)])
        for attr in cls.__dict__.keys():
            if not attr.startswith("_"):
                col=getattr(cls,attr)
                prop_list.append(dict(name=str(col.name),label=col.info.get('label',str(col.name))))
    if params['type']=='table':
        table=params['value']
        for t in db.Model.metadata.sorted_tables:
            if t.name==table:
                for col in t.get_children():
                    prop_list.append(dict(name=str(col.name),label=col.info.get('label',str(col.name))))
                break
    return json_response(fields=[dict(name=prop['name'],dataindex=prop['name'],text=prop['label']) for prop in prop_list])
