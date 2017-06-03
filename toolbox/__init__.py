
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

app = Flask(__name__)
app.config.from_object('app_settings.DevelopmentConfig')

FlaskJSON(app)

db = SQLAlchemy(app,session_options={'autocommit': False})
cache = Cache(app)

def alcoram_json(obj):
    dicJson = {}
    dicJson["py/object"]=obj.__class__.__module__ + "." +obj.__class__.__name__
    for attrName in obj.__mapper__.columns.keys():
        dicJson[attrName]=getattr(obj,attrName)
    return dicJson

db.Model.__json__=alcoram_json

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