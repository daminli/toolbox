
from datetime import datetime
from flask_sqlalchemy import Model
from bokeh.core.properties import value

def sqlalcorm_json(obj):
    dicJson = {}
    dicJson["py/object"]=obj.__class__.__module__ + "." +obj.__class__.__name__
    for attrName in obj.__mapper__.columns.keys():
        data=getattr(obj,attrName)
        if type(data) is datetime:
            data=datetime_format(data)
        dicJson[attrName]=data
    return dicJson

Model.__json__=sqlalcorm_json

def datetime_format(obj):
    return obj.strftime('%Y-%m-%d %H:%M:%S')

#datetime.__json__=datetime_format
