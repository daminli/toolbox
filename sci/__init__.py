
import os
from flask import Flask, Blueprint, url_for,g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_json import FlaskJSON, JsonError, json_response, as_json


from cfg import *

app = Flask(__name__)
app.config.from_object(os.getenv('APPLICATION_SETTINGS', 'config'))
app.debug=app.config.get('DEBUG',False)

if app.debug:
    from werkzeug.debug import DebuggedApplication
    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

FlaskJSON(app)

db = SQLAlchemy(app,session_options={'autocommit': False})

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'auth.login'
lm.login_message_category = "info"

with app.app_context():
    g.db=db
    from sci import views

from util import json_render


