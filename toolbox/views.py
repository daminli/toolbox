import re,os,time
from json import JSONEncoder

from flask import render_template,  redirect, url_for, g,current_app, request
from flask_login import current_user, login_required
from flask_sqlalchemy import get_debug_queries
from flask_json import json_response, as_json

from . import navigation
from datetime import datetime
import toolbox
import util
from _decimal import Decimal

app = current_app
db=g.db

@app.route('/', methods = ['GET', 'POST'])
def init_page():
    """
    the initial page for this project
    """
    return redirect(url_for('ext_page',package='main',page='MainPage'))

@app.route('/extpage', methods = ['GET', 'POST'])
@app.route('/extpage/<package>/<page>/', methods = ['GET', 'POST'])
@login_required
def ext_page(package,page):
    """
    Generate the extjs app html page
    """
    print(package+"->"+page)
    debug=True
    if debug:
        extjs='ext-all-debug.js'
    else:
        extjs='ext-all.js'
    user_acl=dict(view=True,create=True,edit=True,delete=False,upload=False)
    user_acl=JSONEncoder().encode(user_acl)
    
    path=app.static_folder+os.path.sep+'toolbox'
    class_paths=[]
    for temp in os.listdir(path):
        if os.path.isdir(path+os.path.sep+temp):
            class_paths.append(temp)
    return render_template('ext_page.html',page=page,package=package,class_paths=class_paths, logged_in='temp user',timeid=int(time.time()),extjs_libs=extjs,user_acl=user_acl)

@app.route('/navigation', methods = ['GET', 'POST'])
def get_navigation():
    """
    get the navigation tree data
    """
    def add_leaf(menu):
        """
        To set the leaf flag to the navigation data.
        It is necessary for the Ext.tree.Panel
        """
        try:
            child_tree = menu["children"]
            for temp in child_tree:
                add_leaf(temp)
                #add script_root before the navigation target
                if temp.get('type',None)=='url' and temp.get('target',None):
                    if temp['target'].startswith('/'):
                        temp['target']=request.script_root+temp['target']
        except KeyError:
            menu["leaf"]="true"
            
    navData=navigation.NAV_DATA
    
    for menu in navData:
        add_leaf(menu)
    return json_response(children=navData)

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_session = datetime.utcnow()
        '''
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()
        '''
    #g.locale = get_locale()

'''
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])
'''
    
@app.after_request
def after_request(response):
    db.session.commit()
    for query in get_debug_queries():
        if query.duration >= app.config['DATABASE_QUERY_TIMEOUT']:
            app.logger.warning("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" % (query.statement, query.parameters, query.duration, query.context))
    return response

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    #db.session.rollback()
    return render_template('500.html'), 500

@app.route('/favicon.ico', methods = ['GET', 'POST'])
def favicon_ico():
    """
    the initial page for this project
    """
    return redirect(url_for('static',filename='custom/images/favicon.ico'))

@app.route('/url_map', methods = ['GET'])
def url_map():
    url_list=[]
    for rule in list(app.url_map.iter_rules()):
        url_list.append(rule.__repr__())
    url_list.sort()
    return json_response(url_rules=url_list,name=request.script_root)

@app.route('/test',methods=['GET'])
def test():
    return json_response(data=dict(a=Decimal(9.3)))