from flask import g
from toolbox.user_security.models import UserActivity
import random

db=g.db

def add_user_activity(template,data):
    temp=[True,False]
    if random.choice(temp):
        data['__success__']=True
        return data
    else:
        data['__success__']=False
        data['__row__']='data update failed'
        data['__msg__']=dict(success=False,name='activity name not exists')
    return data