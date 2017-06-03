# coding=utf-8
'''
Created on 2013-6-15

@author: lidm1
'''
from datetime import datetime

from flask import g
from .models import ExecHistory,ExecRunLog,ExecRunDetail
from util.datasource.models import DataSourceEngine

db=g.db

def run_script(exec_id,scripts,ds_name,user_id):
    '''
    run script by split the sql
    '''
    run_log = ExecRunLog(exec_id=exec_id,script=scripts,start_time=datetime.now(),run_by=user_id,data_source=ds_name)
    db.begin(subtransactions=True)
    run_log= db.merge(run_log)
    db.commit()
    run_id = run_log.id
    #split the script to sql list
    sql_list = []
    for sql in scripts.split(';'):
        sql_list.append(sql.strip(' \n'))
    
    try:
        #execute script sql by sql
        result=[]
        failure=0
        run_details=[]
        error=None
        data_source = DataSourceEngine(ds_name)
        conn = data_source.engine.connect()
        trans  = conn.begin()
        try:
            for sql in sql_list:
                try:
                    if sql:
                        temp = ExecRunDetail(run_id =run_id,sql_text=sql,start_time=datetime.now(),run_by=user_id)
                        res = conn.execute(sql)
                        result.append('rowcount : '+str(res.rowcount))
                        temp.end_time = datetime.now()
                        temp.result = 'rowcount : '+str(res.rowcount)
                        temp.status = 'success'
                        run_details.append(temp)
                except Exception as e:
                    failure+=1
                    result.append(str(e))
                    temp.end_time = datetime.now()
                    temp.result = str(e)
                    temp.status = 'failure'
                    run_details.append(temp)
        finally:
            trans.commit()
            conn.close()
        
        #save the run detail log to database
        db.begin(subtransactions=True)
        db.add_all(run_details)
        db.commit()
    except Exception as e:
        #update the run log endtime, result and status
        run_log.end_time=datetime.now()
        run_log.result = str(e)
        error = str(e)
        run_log.status = 'failure'
        run_success=False
    else:
        #update the run log endtime, result and status
        run_log.end_time=datetime.now()
        run_log.result = '\n'.join(result)
        run_success=True
        if failure:
            run_log.status = 'success with gap'
        else:
            run_log.status = 'success'
    db.begin(subtransactions=True)
    db.merge(run_log)
    db.commit()
    return dict(success=run_success,data=dict(run_id=run_log.id,run_detail=run_details,error=error))

def run_script_block(exec_id,scripts,ds_name,user_id):
    '''
    run script by begin end block
    '''
    run_log = ExecRunLog(exec_id=exec_id,script=scripts,start_time=datetime.now(),run_by=user_id,data_source=ds_name)
    db.begin(subtransactions=True)
    run_log= db.merge(run_log)
    db.commit()
    run_id = run_log.id
    
    try:
        #execute script sql by sql
        result=[]
        failure=0
        run_details=[]
        error=None
        data_source = DataSourceEngine(ds_name)
        conn = data_source.engine.connect()
        trans  = conn.begin()
        try:
            try:
                if scripts:
                    temp = ExecRunDetail(run_id =run_id,sql_text=scripts,start_time=datetime.now(),run_by=user_id)
                    res = conn.execute(scripts)
                    result.append('rowcount : '+str(res.rowcount))
                    temp.end_time = datetime.now()
                    temp.result = 'rowcount : '+str(res.rowcount)
                    temp.status = 'success'
                    run_details.append(temp)
            except Exception as e:
                failure+=1
                result.append(str(e))
                temp.end_time = datetime.now()
                temp.result = str(e)
                temp.status = 'failure'
                run_details.append(temp)
        finally:
            trans.commit()
            conn.close()
        
        #save the run detail log to database
        db.begin(subtransactions=True)
        db.add_all(run_details)
        db.commit()
    except Exception as e:
        #update the run log endtime, result and status
        run_log.end_time=datetime.now()
        run_log.result = str(e)
        error = str(e)
        run_log.status = 'failure'
        run_success=False
    else:
        #update the run log endtime, result and status
        run_log.end_time=datetime.now()
        run_log.result = '\n'.join(result)
        run_success=True
        if failure:
            run_log.status = 'success with gap'
        else:
            run_log.status = 'success'
    db.begin(subtransactions=True)
    db.merge(run_log)
    db.commit()
    return dict(success=run_success,data=dict(run_id=run_log.id,run_detail=run_details,error=error))
        
