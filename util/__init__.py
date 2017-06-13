

from flask import Blueprint, url_for, current_app

app=current_app

common = app.blueprints.get('common',None)
if not common:
    common=Blueprint('common', 'util', template_folder='templates')
    from util import datasource, selection, dictionary
    from . import views
    app.register_blueprint(common, url_prefix='/common')

PREFIX = '/extpage/common'   
        
NAV_DATA = dict(
               text='Configuration',
               expanded=False,
               children=[
                         dict(
                              text='DataSource',
                              target=PREFIX+'/DataSource/',
                              type='url'
                            ),
                         dict(
                              text='Selection',
                              target=PREFIX+'/Selection/',
                              type='url'
                            ),dict(
                              text='Model Creator',
                              target=PREFIX+'/ModelCreator/',
                              type='url'
                            )]
                    )