import json
from datetime import datetime

from flask import request, url_for, redirect,render_template, current_app,g
from flask_json import json_response, as_json
from flask_login import logout_user, login_user, login_required, current_user
from sqlalchemy.sql import text

from util.selection.models import Selection,CodeType,CodeValue
from util import common

db=g.db

@common.route('/selectlist/',methods = ['GET'])
@login_required
def get_selectlist():
    """
    get the select list base on the selection defination
    """
    name = request.values['name']
    selection = Selection.query.filter(Selection.name==name).first()
    return json_response(selectlist=selection.get_selectlist())

@common.route('/selections/',methods = ['GET'])
@login_required
def get_selections():
    query = Selection.query
    params=request.values
    if params.get('name',''):
        query=query.filter(getattr(Selection,'name').like('%'+params['name']+'%'))
    result = query.all()
    return json_response(selections=result)

@common.route('/selections/',methods = ['POST'])
@login_required
def save_selections():
    params=request.values
    selection = Selection(name=params['name'],type=params['type'],config=params['config'])
    if params.get('datasource',None):
        selection.datasource=params['datasource']
    result= db.session.merge(selection)
    return json_response(success=True,selection=result)

@common.route('/selections/',methods = ['DELETE'])
@login_required
def del_selections():
    params=request.values
    selection = Selection.query.filter(Selection.name==params['name']).first()
    db.session.delete(selection)
    result=db.session.flush()
    return json_response(success=True,data=result)

    