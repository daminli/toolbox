
from datetime import datetime
from flask_sqlalchemy import Model
from sqlalchemy.engine.result import RowProxy
from flask_json import JSONEncoderEx
from flask import current_app

def sqlalcorm_json(obj):
    dicJson = {}
    dicJson["py/object"]=obj.__class__.__module__ + "." +obj.__class__.__name__
    for attrName in obj.__mapper__.columns.keys():
        data=getattr(obj,attrName)
        if type(data) is datetime:
            data=datetime_format(data)
        dicJson[attrName]=data
    return dicJson

def rowproxy_json(obj):
    return {cell[0]:cell[1] for cell in obj.items()}

def datetime_format(obj):
    fmt = current_app.config.get('JSON_DATETIME_FORMAT')
    return obj.strftime(fmt)


#set custom json allways in highest priority
ori_default=JSONEncoderEx.default
def defult_json(self, o):
    if current_app.config.get('JSON_USE_ENCODE_METHODS'):
        if hasattr(o, '__json__'):
            return o.__json__()
        elif hasattr(o, 'for_json'):
            return o.for_json()
    return ori_default(self,o)
JSONEncoderEx.default=defult_json

#datetime.__json__=datetime_format
Model.__json__=sqlalcorm_json
RowProxy.__json__=rowproxy_json

