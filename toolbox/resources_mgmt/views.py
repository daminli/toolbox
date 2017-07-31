import json, uuid
from datetime import date,datetime,timedelta

from flask import request, url_for, redirect,render_template, current_app,g
from flask_json import json_response, as_json
from flask_login import logout_user, login_user, login_required, current_user
from flask_restful import Resource
from wtforms_alchemy import ModelForm

from util.id_generator import IdGenerator
from . import models


app=current_app
lm = current_app.login_manager
db=g.db
api=g.api

class Projects(Resource):
    def get(self,project_id=None,test_id=None):
        if project_id:
            msg='get project_id:'+project_id
        else:
            msg='get all project'
        form=ProjectForm()
        form_layout=[]
        for field in form:
            form_layout.append(field())
        return form_layout
    
    def post(self):
        msg='add project'
        return msg, 201
    
    def delete(self, project_id):
        msg='delete project:'+project_id
        return msg, 204

    def put(self, project_id):
        msg='update project:'+project_id
        return msg, 201

api.add_resource(Projects, '/res_mgmt/projects','/res_mgmt/projects/<string:project_id>')


class ProjectForm(g.ModelForm):
    class Meta:
        model = models.Projects
        include=['project_name']