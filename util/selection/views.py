import json
from datetime import datetime

from flask import request, url_for, redirect,render_template, current_app,g
from flask_json import json_response, as_json
from flask_login import logout_user, login_user, login_required, current_user
from sqlalchemy.sql import text

from util.selection.models import Selection,CodeType,CodeValue
from util import common

db=g.db

@common.route('/selection_list',methods = ['GET'])
@login_required
def selection_list(request):
    """
    get the report folder tree structure json data
    """
    name = request.params['name']
    selection = db.query(Selection).filter(Selection.name==name).first()
    return as_json(selection.get_selection())

@common.route('/selections',methods = ['GET'])
@login_required
def get_selections(params,request):
    query = db.query(Selection)
    if params.get('name',''):
        query=query.filter(getattr(Selection,'name').like('%'+params['name']+'%'))
    result = query.all()
    return as_json(result)

@common.route('/selections',methods = ['POST'])
@login_required
def save_selections(params,request):
    selection = Selection(name=params['name'],type=params['type'],config=params['config'])
    if params.get('datasource',None):
        selection.datasource=params['datasource']
    result= db.merge(selection)
    return json_response(success=True,data=result)

@common.route('/selections',methods = ['DELETE'])
@login_required
def del_selections(params,request):
    selection = db.query(Selection).filter(Selection.name==params['name']).first()
    db.delete(selection)
    result=db.flush()
    return json_response(success=True,data=result)

    