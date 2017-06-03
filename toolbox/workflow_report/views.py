import json
import itertools
import operator
from datetime import date,timedelta,datetime

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )
from pyramid.view import (
    view_config,
    forbidden_view_config,
    )
from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    )
from pyramid_extdirect import extdirect_method
from sqlalchemy.engine.result import RowProxy

import cfg

DBSession = cfg.DBSession

@extdirect_method(action='workflow_report', request_as_last_param=True)
def wfl_overall(params, request):
    from_date=params.get('from_date',date.today()+timedelta(days=-10))
    to_date=params.get('to_date',date.today())
    if isinstance(from_date,unicode):
        from_date=datetime.strptime(from_date,cfg.DATE_FORMAT)
    if isinstance(to_date,unicode):
        to_date=datetime.strptime(to_date,cfg.DATE_FORMAT)
    sql_query = '''
    SELECT a.team,
         a.function_name,
         a.system_name,
         a.runname,
         a.runid,
         a.run_key,
         COUNT (1) total_run,
         MAX (a.gatetime) gatetime,
         SUM (
            CASE
               WHEN    NVL (over_gatetime, 'NO') = 'YES'
                    OR NVL (IS_BREAK, 'NO') = 'YES'
                    OR NVL (b.status, 'CANCEL') = 'CANCEL'
               THEN
                  0
               ELSE
                  1
            END)
            full_success,
         SUM (
            CASE
               WHEN    NVL (over_gatetime, 'NO') = 'YES'
                    OR NVL (b.status, 'CANCEL') = 'CANCEL'
               THEN
                  0
               ELSE
                  1
            END)
            break_success,
         SUM (DECODE (NVL (over_gatetime, 'NO'),  'YES', 1,  'NO', 0)) overtime,
         SUM (DECODE (NVL (IS_BREAK, 'NO'),  'YES', 1,  'NO', 0)) BREAK,
         SUM (DECODE (NVL (b.status, 'CANCEL'), 'COMPLETED', 1, 0)) completed,
         SUM (DECODE (NVL (b.status, 'CANCEL'), 'COMPLETED', 0, 1)) failed
    FROM CONF_WFL_RUN a JOIN FC_WFL_RUN b ON a.run_key = b.run_key
   WHERE starttime BETWEEN :from_date AND :to_date
GROUP BY a.team,
         a.function_name,
         a.system_name,
         a.runname,
         a.runid,
         a.run_key
ORDER BY a.team,
         a.function_name,
         a.system_name,
         a.runid,
         a.run_key
    '''
    resultProxy = DBSession.execute(sql_query,dict(from_date=from_date,to_date=to_date))
    result = resultProxy.fetchall()
    treeResult = groupby(result, [dict(attr_name='team', name='runid'), dict(attr_name='function_name', name='runid', expanded=False), dict(attr_name='system_name', name='runid', expanded=True)])
    return dict(text='.' , children=treeResult)

def groupby(dict_list, group_list):
    if not group_list:
        result = []
        for temp in dict_list:
            if isinstance(temp, RowProxy):
                temp = dict(temp.items())
            temp['leaf'] = True
            result.append(temp)
        return result
    group_def = group_list[0]
    attr_name = group_def.get('attr_name')
    expanded = group_def.get('expanded', False)
    name = group_def.get('name', 'text')
    groupResult = []
    for group, children in itertools.groupby(dict_list, operator.itemgetter(attr_name)):
        groupResult.append({name:group, 'expanded':expanded, 'children':groupby(children, group_list[1:])})
    return groupResult

@extdirect_method(action='workflow_report', request_as_last_param=True)
def run_trend(params, request):
    from_date=params.get('from_date',date.today()+timedelta(days=-10))
    to_date=params.get('to_date',date.today())
    if isinstance(from_date,unicode):
        from_date=datetime.strptime(from_date,cfg.DATE_FORMAT)
    if isinstance(to_date,unicode):
        to_date=datetime.strptime(to_date,cfg.DATE_FORMAT)
    runid = params['runid']
    run_key=runid['run_key']
    sql_query='''
    SELECT TO_CHAR (starttime, 'mm/dd-hh24') run_day, a.*
    FROM FC_WFL_RUN a
   WHERE     run_key = :run_key
         AND STARTTIME BETWEEN :from_date AND :to_date
    ORDER BY run_day
    '''
    resultProxy = DBSession.execute(sql_query,dict(run_key=run_key,from_date=from_date,to_date=to_date))
    result = resultProxy.fetchall()
    return result

@extdirect_method(action='workflow_report', request_as_last_param=True)
def run_detail(params, request):
    def build_wfl_tree(res_list,sub_tree):
        if not sub_tree:
            sub_tree['node_name']='root'
            children=[]
            for row in res_list:
                if not row['parent_id']:
                    children.append(row)
                    if row['node_type'] in ['SubWorkflow','Procedure Group']:
                        row['expanded']=False
                        build_wfl_tree(res_list,row)
                    else:
                        row['leaf']=True
            sub_tree['children']=children
        else:
            children=[]
            for row in res_list:
                if row['parent_id']==sub_tree['instance_id'] and row['parent_node']==sub_tree['full_node_name']:
                    children.append(row)
                    if row['node_type']  in ['SubWorkflow','Procedure Group']:
                        row['expanded']=True
                        build_wfl_tree(res_list,row)
                    else:
                        row['leaf']=True
            sub_tree['children']=children
                
    run_instance=params['run_instance']
    system_name=run_instance['system_name']
    root_instance=run_instance['instance']
    sql_query='''
    SELECT a.system_name,
       a.instance_id,
       a.root_instance,
       a.template,
       a.wfl_svc,
       a.parent_id,
       a.parent_node,
       a.start_date,
       a.end_date,
       a.status,
       a.workflow_path,
       b.id,
       b.node_name,
       '//' || a.wfl_svc || '/' || a.template || '.' || b.node_name
          full_node_name,
       b.node_type,
       ROUND ( (b.end_time - b.start_time) * 24 * 60) runtime,
       b.start_time,
       b.end_time,
       b.status node_status,
       MIN (start_date) OVER () wfl_starttime,
       MAX (end_date) OVER () wfl_endtime
  FROM    fc_wfl_log a
       JOIN
          fc_wfl_task_log b
       ON a.system_name = b.system_name AND a.instance_id = b.instance_id
 WHERE     b.node_type NOT IN ('AndJoin', 'OrJoin','Start','Done')
       And round((b.end_time-b.start_time)*24*60)>0
       AND a.system_name = '''+"'"+system_name+"'"+'''
       AND a.root_instance = '''+"'"+root_instance+"'"+'''
       UNION ALL
SELECT system_name,
       instance instance_id,
       root_instance,
       NULL template,
       NULL wfl_svr,
       parent_id,
       parent_node,
       NULL start_date,
       NULL end_date,
       'COMPLETED' status,
       NULL workflow_path,
       node_name id,
       node_name,
       node_name full_node_name,
       node_type,
       round((end_time-start_time)*24*60) run_time,
       start_time,
       end_time,
       'COMPLETE' node_status,
       wfl_starttime,
       wfl_endtime
  FROM fc_wfl_sub_proc a
 WHERE a.system_name = '''+"'"+system_name+"'"+'''
       AND a.root_instance = '''+"'"+root_instance+"'"+'''
       and round((end_time-start_time)*24*60) >0
       ORDER BY wfl_starttime,start_time,node_name
    '''
    
    resultProxy = DBSession.execute(sql_query,dict(system_name=system_name,root_instance=root_instance))
    result = resultProxy.fetchall()
    
    res_list=[]
    for row in result:
        res_list.append(dict(row.items()))
    res_tree={}
    build_wfl_tree(res_list,res_tree)
    return res_tree

@extdirect_method(action='workflow_report', request_as_last_param=True)
def node_trend(params,request):
    from_date=params.get('from_date',date.today()+timedelta(days=-10))
    to_date=params.get('to_date',date.today())
    if isinstance(from_date,unicode):
        from_date=datetime.strptime(from_date,cfg.DATE_FORMAT)
    if isinstance(to_date,unicode):
        to_date=datetime.strptime(to_date,cfg.DATE_FORMAT)
    runid = params['runid']
    system_name = runid['system_name']
    run_key=runid['run_key']
    run_id=runid['runid']
    run_node=params['run_node']
    node_name=run_node['node_name']
    parent_node=run_node['parent_node']
    node_type=run_node['node_type']
    if not parent_node:
        parent_node='NULL'
    if node_type in ['Procedure Group','Procedure']:
        sql_query='''
        SELECT a.runid,
       a.instance instance_id,
       a.node_name,
       a.node_type,
       a.parent_node,
       a.root_instance,
       a.start_time,
       'COMPLETED' status,
       a.system_name,
       TO_CHAR (a.wfl_starttime, 'mm/dd-hh24') run_day,
       ROUND ( (a.end_time - a.start_time) * 24 * 60) runtime
  FROM fc_wfl_sub_proc a
  where system_name =:system_name and runid=:run_id  AND a.wfl_starttime BETWEEN :from_date AND :to_date and node_name =:node_name and parent_node =:parent_node order by start_time
        '''
    else:
        sql_query='''
        SELECT a.system_name,
           a.runid,
           a.run_key,
           a.instance root_instance,
           b.instance_id,
           TO_CHAR (a.starttime, 'mm/dd-hh24') run_day,
           b.template,
           c.node_name,
           c.node_type,
           b.workflow_path,
           b.parent_node,
           c.start_time,
           c.end_time,
           round((c.end_time - c.start_time)*24*60) runtime,
           c.status
      FROM fc_wfl_run a
           JOIN fc_wfl_log b
              ON a.instance = b.root_instance AND a.system_name = b.system_name
           JOIN fc_wfl_task_log c
              ON b.instance_id = c.instance_id AND b.system_name = c.system_name
     WHERE     a.system_name = :system_name
           AND a.run_key = :run_key
           AND a.starttime BETWEEN :from_date AND :to_date
           AND c.node_name = :node_name
           AND NVL (b.parent_node, 'NULL') =:parent_node
           order by run_day
            '''
    resultProxy = DBSession.execute(sql_query,dict(system_name=system_name,run_key=run_key,node_name=node_name,parent_node=parent_node,from_date=from_date,to_date=to_date,run_id=run_id))
    result = resultProxy.fetchall()
    return result