
from flask import Blueprint, url_for, current_app

app=current_app

freequery = app.blueprints.get('free_query',None)
if not freequery:
    freequery=Blueprint('free_query', 'free_query', template_folder='templates')
    from . import views
    app.register_blueprint(freequery, url_prefix='/free_query')

PREFIX = '/extpage/free_query'
        
NAV_DATA = dict(
               text='Free Query',
               expanded=False,
               children=[dict(
                              text='View Report',
                              target=PREFIX+'/ViewReport/',
                              type='url'
                            ), 
                         dict(
                              text='Create Report',
                              target=PREFIX+'/CreateReport/',
                              type='url'
                            )]
                    )