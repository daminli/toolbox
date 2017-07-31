import json, uuid
from datetime import date,datetime,timedelta

from flask import request, url_for, redirect,render_template, current_app,g
from flask_json import json_response
from flask_login import login_required, current_user


from util.id_generator import IdGenerator
from . import executor, sqlexec
from .models import ExecHistory, ExecRunLog, ExecRunDetail


app=current_app
lm = current_app.login_manager
db=g.db

@sqlexec.route('/new_request',methods = ['GET','POST'])
@login_required
def new_request():
    """
    run sql script
    """
    user_id =  current_user.login_name
    params=request.values
    app.logger.debug(params)
    exec_history = ExecHistory(summary=params['summary'],create_by=user_id)
    result= db.session.merge(exec_history)
    db.session.flush()
    return json_response(success=True, data=result)

@sqlexec.route('/run_script',methods = ['POST'])
@login_required
def run_script():
    """
    run sql script
    """
    scripts = request.values['scripts']
    exec_id = request.values['exec_id']
    ds_name = request.values['datasource']
    user_id =  current_user.login_name
    result=executor.run_script(exec_id, scripts, ds_name, user_id)
    return json_response(success=result['success'],data=result['data'])

@sqlexec.route('/run_script_block',methods = ['POST'])
@login_required
def run_script_block(json_response):
    """
    run sql script block
    """
    scripts = request.values['scripts']
    exec_id = request.values['exec_id']
    ds_name = request.values['datasource']
    user_id =  current_user.login_name
    result = executor.run_script_block(exec_id, scripts, ds_name, user_id)
    return json_response(result=result)

@sqlexec.route('/get_history',methods = ['GET','POST'])
@login_required
def get_history():
    """
    get execute history
    """
    query = ExecHistory.query
    params=request.values
    if params.get('from_date',''):
        query=query.filter(getattr(ExecHistory, 'creation_date') >= datetime.strptime(params['from_date'],app.config['DATE_FORMAT']))
    if params.get('to_date',''):
        query=query.filter(getattr(ExecHistory, 'creation_date') <= datetime.strptime(params['to_date'],app.config['DATE_FORMAT']))
    if params.get('create_by',''):
        query=query.filter(getattr(ExecHistory, 'create_by') == params['create_by'])
    result= query.all()
    return json_response(result=result)

@sqlexec.route('/get_run_log',methods = ['GET'])
@login_required
def get_run_log():
    """
    get run log by exec_id
    """
    params=request.values
    result = ExecRunLog.query.filter(ExecRunLog.exec_id==params['exec_id']).all()
    return json_response(result=result)

@sqlexec.route('/get_run_detail',methods = ['GET'])
@login_required
def get_run_detail():
    """
    get sql run details by run_id
    """
    params=request.values
    result=ExecRunDetail.query.filter(ExecRunDetail.run_id==params['run_id']).all()
    return json_response(result=result)
