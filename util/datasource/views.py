import json
from datetime import datetime

from flask import request, url_for, redirect,render_template, current_app,g
from flask_json import json_response, as_json
from flask_login import logout_user, login_user, login_required, current_user

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from util.id_generator import IdGenerator
from util import common
from util.datasource.models import DataSource, DataSourceEngine


app=current_app
lm = current_app.login_manager
db=g.db

@common.route('/data_source',methods = ['POST'])
@login_required
def save_data_source():
    """
    create data source
    """
    params=request.params
    data_source = DataSource(name=params['name'],user_name=params['user_name'],db_connect=params['db_connect'])
    data_source.ds_type=params.get('ds_type',None)
    data_source.ds_group=params.get('ds_group',None)
    data_source.password=params['password']
    user_id =  current_user.login_name
    data_source.create_by=user_id
    data_source.last_modified_by=user_id
    result= db.merge(data_source)
    return json_response(success=True,data=result)

@common.route('/data_source',methods = ['DELETE'])
@login_required
def del_data_source():
    """
    delete data source
    """
    params=request.params
    data_source = db.query(DataSource).filter(DataSource.name==params['name']).first()
    db.delete(data_source)
    result=db.flush()
    return json_response(success=True,data=result)

@common.route('/data_source',methods = ['GET'])
@login_required
def get_data_source():
    """
    run sql script
    """
    params=request.params
    query = db.query(DataSource)
    if params.get('ds_group',''):
        query=query.filter(getattr(DataSource,'ds_group' )== params['ds_group'])
    data_source=query.all()
    return as_json(data_source)
    
@common.route('/data_source/test',methods = ['GET'])
@login_required
def test_data_source(request):
    """
    create data source
    """
    try:
        db_engine = create_engine('oracle://'+request.params['user_name']+':'+request.params['password']+'@'+request.params['db_connect'],poolclass=NullPool)
        # create a db connection
        conn = db_engine.connect()
        try:
            resultProxy = conn.execute('select * from dual')
            result = resultProxy.fetchall()
            resultProxy.close()
            if len(result)==1:
                return dict(success=True,data=result)
            else:
                return dict(success=False,data=result)
        except Exception as e:
            return dict(success=False,data=str(e))
        finally:
            conn.close()
    except Exception as e:
        print(e)
        return json_response(success=False,data=str(e))
    
