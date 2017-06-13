
import os
from flask import Flask, Blueprint, url_for,g
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_cache import CachingQuery, FromCache
from flask_cache import Cache
from flask_login import LoginManager
from flask_openid import OpenID
from flask_mail import Mail
from flask_babel import Babel, lazy_gettext
from flask_json import FlaskJSON, JsonError, json_response, as_json


from app_settings import *

basedir=os.path.split(os.path.realpath(__file__))[0]
static_folder=os.path.realpath(os.path.join(basedir,'..'+os.path.sep+'..'+os.path.sep+'toolbox_www'))
#static_folder='..'+os.path.sep+'..'+os.path.sep+'toolbox_wwww'
app = Flask(__name__,static_folder=static_folder,static_url_path='/static')
app.config.from_object(os.getenv('APPLICATION_SETTINGS', 'config'))
app.debug=app.config.get('DEBUG',False)

if app.debug:
    from werkzeug.debug import DebuggedApplication
    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

FlaskJSON(app)

db = SQLAlchemy(app,session_options={'autocommit': False})
cache = Cache(app)
mail = Mail(app)
babel = Babel(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'auth.login'
lm.login_message = lazy_gettext('Please login to access this page.')
lm.login_message_category = "info"

from sqlalchemy import engine_from_config

with app.app_context():
    g.db=db
    g.cache=cache
    from toolbox import views,navigation,user_security,action,sql_executor,workflow_report,itsm,free_query
    import util
    NAV_DATA=navigation.NAV_DATA
    NAV_DATA.append(sql_executor.NAV_DATA)
    NAV_DATA.append(action.NAV_DATA)
    NAV_DATA.append(workflow_report.NAV_DATA)
    NAV_DATA.append(itsm.NAV_DATA)
    NAV_DATA.append(util.NAV_DATA)
    NAV_DATA.append(free_query.NAV_DATA)
    print(app.url_map)
    print('debug:'+str(app.debug))
    
def alcoram_json(obj):
    dicJson = {}
    dicJson["py/object"]=obj.__class__.__module__ + "." +obj.__class__.__name__
    for attrName in obj.__mapper__.columns.keys():
        dicJson[attrName]=getattr(obj,attrName)
    return dicJson

db.Model.__json__=alcoram_json    
    
class ReverseProxied(object):
    '''Wrap the application in this middleware and configure the 
    front-end server to add these headers, to let you quietly bind 
    this to a URL other than / and to an HTTP scheme that is 
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print(environ)
        print('script name:'+environ.get('SCRIPT_NAME', ''))
        print('path info:'+environ['PATH_INFO'])
        '''
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        print('x script name:'+environ.get('HTTP_X_SCRIPT_NAME', ''))
        print('path info:'+environ['PATH_INFO'])
        '''
        return self.app(environ, start_response)
    
#app.wsgi_app = ReverseProxied(app.wsgi_app)