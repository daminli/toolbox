
from flask import Blueprint, url_for, current_app

app=current_app

sqlexec = app.blueprints.get('sqlexec',None)
if not sqlexec:
    sqlexec=Blueprint('sqlexec', 'sql_executor', template_folder='templates')
    from . import views
    app.register_blueprint(sqlexec, url_prefix='/sql_executor')

PREFIX = '/extpage/sql_executor'        
        
NAV_DATA = dict(
               text='Execute Sql',
               expanded=True,
               children=[dict(
                              text='Execute',
                              target=PREFIX+'/ExecuteSql/',
                              type='url'
                            ), 
                         dict(
                              text='History',
                              target=PREFIX+'/ExecHistory/',
                              type='url'
                            )]
                    )
    
    