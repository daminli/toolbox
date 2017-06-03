import re,os,time
from json import JSONEncoder

from flask import render_template,  redirect, url_for, g,current_app
from flask_login import current_user, login_required
from flask_json import json_response

import util
from util import common
from toolbox.sql_executor.models import ExecHistory

app = current_app
db=g.db


@common.route('/idg_test', methods = ['GET', 'POST'])
def idg_test():
    
    
    idg_exec=util.id_generator.IdGenerator('EXEC_HISTORY')
    result=[]
    for i in list(range(1)):
        result.append(idg_exec.nextval())
        #app.logger.info('exec_id: %s',str(i))
    
    data=[]
    
    for i in list(range(2)):
        temp=ExecHistory(summary="test summary",create_by='lidm1')
        db.session.add(temp)
        data.append(temp)
    db.session.commit()
    
    for i in list(range(1)):
        result.append(idg_exec.nextval())
    return json_response(ids=result,data=data)