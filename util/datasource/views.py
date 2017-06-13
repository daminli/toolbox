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

@common.route('/datasources/',methods = ['POST'])
@login_required
def save_datasource():
    """
    create data source
    """
    params=request.values
    data_source = DataSource(name=params['name'],user_name=params['user_name'],db_connect=params['db_connect'])
    data_source.ds_type=params.get('ds_type',None)
    data_source.ds_group=params.get('ds_group',None)
    data_source.password=params['password']
    user_id =  current_user.login_name
    data_source.create_by=user_id
    data_source.last_modified_by=user_id
    result= db.session.merge(data_source)
    return json_response(success=True,data=result)

@common.route('/datasources/',methods = ['DELETE'])
@login_required
def del_datasource():
    """
    delete data source
    """
    params=request.params
    data_source = db.query(DataSource).filter(DataSource.name==params['name']).first()
    db.session.delete(data_source)
    result=db.session.flush()
    return json_response(success=True,data=result)

@common.route('/datasources/',methods = ['GET'])
@login_required
def get_datasource():
    """
    get datasource list
    """
    params=request.values
    query = DataSource.query
    if params.get('ds_group',''):
        query=query.filter(getattr(DataSource,'ds_group' )== params['ds_group'])
    data_source=query.all()
    return json_response(datasources=data_source)
    
@common.route('/datasources/',methods = ['PUT'])
@login_required
def test_datasource():
    """
    test data source connection
    """
    params=request.values
    try:
        db_engine = create_engine(params['ds_type']+'://'+params['user_name']+':'+params['password']+'@'+params['db_connect'],poolclass=NullPool)
        # create a db connection
        conn = db_engine.connect()
        #return dict(success=True,data='connect success')
        try:
            trans=conn.begin()
            trans.commit()
            return json_response(success=True)
        except Exception as e:
            app.logger.error(str(e))
            return dict(success=False,data=str(e))
        finally:
            conn.close()
    except Exception as e:
        app.logger.error(str(e))
        return json_response(success=False,data=str(e))
    return json_response(success=False)
    
