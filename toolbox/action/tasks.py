# coding=utf-8
'''
Created on 2014-3-1

@author: lidm1
'''
from xml.etree import ElementTree
from datetime import datetime
import time
import cx_Oracle

import cfg
from util.datasource.models import DataSourceEngine


class Task(object):
    def __init__(self,action):
        pass
    
    def __new__(self,action):
        if action.action_type =='proc':
            return ProcTask(action)
        
    def execute(self):
        '''
        lock
        is_sync
        '''
        pass
        
class ProcTask(object):
    # this maps datatypes, pl/sq -> python
    TYPE_MAP={
        'RAW'            :cx_Oracle.BINARY,
        'BFILE'            :cx_Oracle.BFILE,
        'BLOB'            :cx_Oracle.BLOB,
        'CLOB'            :cx_Oracle.CLOB,
        'REF CURSOR'   :cx_Oracle.CURSOR,
        'DATE'            :cx_Oracle.DATETIME,
        'CHAR'            :cx_Oracle.FIXED_CHAR,
        'unhandled_LONG_BINARY'    :cx_Oracle.LONG_BINARY,
        'unhandled_LONG_STRING'    :cx_Oracle.LONG_STRING,
        'unhandled_NCLOB'    :cx_Oracle.NCLOB,
        'NUMBER'        :cx_Oracle.NUMBER,
        'FLOAT'            :cx_Oracle.NUMBER,
        'unhandled_OBJECT'    :cx_Oracle.OBJECT,
        'VARCHAR2'        :cx_Oracle.STRING,
        'TIMESTAMP'        :cx_Oracle.TIMESTAMP,
        'ROWID'            :cx_Oracle.ROWID,
        'CURSOR'        :cx_Oracle.CURSOR
    }
    
    def __init__(self,action):
        self.action=action
        task_cfg=ElementTree.fromstring(self.action.action_detail)
        if task_cfg.find('DATA_SOURCE'):
            self.ds_name=task_cfg.find('DATA_SOURCE')['Value']
        else:
            self.ds_name=cfg.config.registry.settings.get('action.defualt_datasource')
        proc=task_cfg.find('PROC_NAME')
        self.proc_info(proc)
    
    def proc_info(self,proc):
        self.proc_name=proc.attrib['Value']
        #get proc package and object
        temp=self.proc_name.split('.')
        db_obj=temp[0] #usered to get owner from DB
        if len(temp)==2:
            self.package=temp[0]
            self.object=temp[1]
        if len(temp)==1:
            self.package=None
            self.object=temp[0]
        ds=DataSourceEngine(self.ds_name)
        conn = ds.engine.connect()
        try:
            # get owner from data source user_name
            db_user=ds.datasource.user_name
            result = conn.execute('select * from user_objects where object_name =:object_name',dict(object_name=db_obj.upper())).fetchall()
            if result:
                if result[0]['object_type']=='SYNONYM':
                    result = conn.execute('select * from user_synonyms where synonym_name =:object_name',dict(object_name=db_obj.upper())).fetchall()
                    self.owner=result[0]['table_owner']
                else:
                    self.owner=db_user
            else:
                raise Exception('procedure does not exists :',self.proc_name,' ',db_user)
            #get proc paramters from db dictionay
            sql='''select *
                      from all_arguments
                      where 
                      object_name=:object
                       and owner=:owner
                       --and argument_name is not null
                        and package_name=:package
                      order by position'''
            if not self.package:
                sql='''select *
                          from all_arguments
                          where 
                          object_name=:object
                           and owner=:owner
                           --and argument_name is not null
                            and package_name is null
                          order by position'''
            result = conn.execute(sql,dict(object=self.object.upper(),owner=self.owner.upper(),package=self.package.upper())).fetchall()
            self.arguments=result
            if len(result)>0:
                if result[0]['position']==0:
                    self.call_type='procedure'
                else:
                    self.call_type='function'
        finally:
            conn.close()
    
    def execute(self,params):
        #parameter prepare for procedure
        output_data={}
        conn = DataSourceEngine(self.ds_name).engine.raw_connection()
        try:
            cursor= conn.cursor()
            try:
                call_params=[]
                return_type=None
                out_params=[]
                call_type='procedure'
                for arg in self.arguments:
                    if arg['position']==0:
                        call_type='function'
                        return_type=self.TYPE_MAP.get(arg['data_type'])
                    else:
                        if arg['in_out']=='OUT':
                            temp=cursor.var(self.TYPE_MAP.get(arg['data_type']))
                            call_params.append(temp)
                            out_params.append(dict(obj=temp,arg_name=arg['argument_name'],type=arg['data_type'],index=arg['position']-1))
                        if arg['in_out']=='IN':
                            param=params.get(arg['argument_name'].lower(),None)
                            #assert(1==2)
                            if not param:
                                call_params.append(param)
                            else:
                                if arg['data_type'] == 'DATE':
                                    if len(param)>10:
                                        temp=datetime.strptime(param,cfg.DATETIME_FORMAT)
                                    else:
                                        temp=datetime.strptime(param,cfg.DATE_FORMAT)
                                    call_params.append(temp)
                                else:
                                    if arg['data_type'] == 'TIMESTAMP':
                                        temp=datetime.strptime(param,cfg.TIMESTAMP_FORMAT)
                                        call_params.append(temp)
                                    else:
                                        call_params.append(param)
                if call_type=='procedure':
                    cursor.callproc(self.proc_name,call_params)
                    for output in out_params:
                        if output['type'] in ['CLOB' ,'BLOB']:
                            temp=call_params[output['index']].getvalue().read()
                        else:
                            temp=call_params[output['index']].getvalue()
                        output_data[output['arg_name'].lower()]=temp
                else:
                    output_data=cursor.callfunc(self.proc_name,return_type,call_params)
            finally:
                cursor.close()
        finally:
            conn.close()
        return output_data
        
        