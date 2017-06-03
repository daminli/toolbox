

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

def includeme(config):
    config.add_route('selection_list', '/selection_list')
    config.add_route('save_data_source', '/save_data_source')
    config.add_route('test_data_source', '/test_data_source')
    config.add_route('get_data_source', '/get_data_source')
    config.add_route('del_data_source', '/del_data_source')
    config.add_route('test_url', '/test_url')