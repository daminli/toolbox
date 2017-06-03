# coding=utf-8
'''
Created on 2013-2-2

@author: lidm1
'''
import json
import datetime
from sqlalchemy import Numeric
import decimal
from sqlalchemy.engine.result import RowProxy
from sqlalchemy.util._collections import KeyedTuple
from cfg import Base
import cfg
import cx_Oracle

from pyramid.renderers import JSON 

custom_json_renderer_factory = JSON(ensure_ascii=False,encoding="utf-8")

def datetime_adapter(obj, request):
    return obj.strftime(cfg.DATETIME_FORMAT)

def date_adapter(obj, request):
    return obj.strftime(cfg.TIME_FORMAT)

def sqlalchemy_number_adapter(obj, request):
    return str(obj)

def sqlalchemy_orm_adapter(obj,request):
    dicJson = {}
    dicJson["py/object"]=obj.__class__.__module__ + "." +obj.__class__.__name__
    for attrName in obj.__mapper__.columns.keys():
        dicJson[attrName]=getattr(obj,attrName)
    return dicJson

def sqlalchemy_rowproxy_adapter(obj,request):
    return {cell[0]:cell[1] for cell in obj.items()}

def sqlalchemy_keyedtuple_adapter(obj,request):
    return {key:getattr(obj,key) for key in obj.keys()}

def cx_NUMBER_adapter(obj,request):
    return obj.getvalue()

def cx_CLOB_adapter(obj,request):
    return obj.getvalue().read()


custom_json_renderer_factory.add_adapter(datetime.datetime, datetime_adapter)
custom_json_renderer_factory.add_adapter(datetime.date, date_adapter)
custom_json_renderer_factory.add_adapter(Base, sqlalchemy_orm_adapter)
custom_json_renderer_factory.add_adapter(RowProxy, sqlalchemy_rowproxy_adapter)
custom_json_renderer_factory.add_adapter(KeyedTuple, sqlalchemy_keyedtuple_adapter)

custom_json_renderer_factory.add_adapter(decimal.Decimal, sqlalchemy_number_adapter)
custom_json_renderer_factory.add_adapter(cx_Oracle.NUMBER, cx_NUMBER_adapter)
custom_json_renderer_factory.add_adapter(cx_Oracle.CLOB, cx_CLOB_adapter)

#RowProxy