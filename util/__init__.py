from flask import Blueprint,current_app
from flask_login import current_user

app=current_app

common = app.blueprints.get('common',None)
if not common:
    common=Blueprint('common', 'util', template_folder='templates')
    from util import views,selection,upload,datasource,dictionary
    app.register_blueprint(common, url_prefix='/common')
    
def get_user():
    if current_user:
        user=current_user.login_name
    else:
        user=None
    return current_user.login_name

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