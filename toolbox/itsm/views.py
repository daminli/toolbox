import json
from datetime import datetime
import transaction

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
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from pyramid_extdirect import extdirect_method

import cfg
from util.id_generator import IdGenerator
from models import Project,MtpWindow,IssueCategory,TicketRootCause,TicketAnalyze,TicketUsers

DBSession = cfg.DBSession

@extdirect_method(action='itsm',request_as_last_param=True)
def get_issue(params,request):
    result = DBSession.query(IssueCategory.issue_category,IssueCategory.issue,IssueCategory.issue_comment).filter(IssueCategory.module==params['product_categorization_tier3']).filter(IssueCategory.issue_category==params['issue_category']).filter(IssueCategory.status=='ACTIVE').order_by(IssueCategory.issue).distinct().all()
    rlist=[]
    for obj in result:
        rlist.append({key:getattr(obj,key) for key in obj.keys()})
    return rlist

@extdirect_method(action='itsm',request_as_last_param=True)
def get_issue_category(params,request):
    result = DBSession.query(IssueCategory.issue_category,IssueCategory.module).filter(IssueCategory.module==params['product_categorization_tier3']).filter(IssueCategory.status=='ACTIVE').order_by(IssueCategory.issue_category).distinct().all()
    rlist=[]
    for obj in result:
        rlist.append({key:getattr(obj,key) for key in obj.keys()})
    return rlist

@extdirect_method(action='itsm',request_as_last_param=True)
def get_root_cause(params,request):
    result = DBSession.query(TicketRootCause.rc_category,TicketRootCause.root_cause).filter(TicketRootCause.rc_category==params['rc_category']).filter(TicketRootCause.status=='ACTIVE').order_by(TicketRootCause.root_cause).distinct().all()
    rlist=[]
    for obj in result:
        rlist.append({key:getattr(obj,key) for key in obj.keys()})
    return rlist

@extdirect_method(action='itsm',request_as_last_param=True)
def get_rc_category(params,request):
    result = DBSession.query(TicketRootCause.rc_category).filter(TicketRootCause.status=='ACTIVE').order_by(TicketRootCause.rc_category).distinct().all()
    rlist=[]
    for obj in result:
        rlist.append({key:getattr(obj,key) for key in obj.keys()})
    return rlist

@extdirect_method(action='itsm',request_as_last_param=True)
def get_ticket_analyze(params,request):
    sql_text='''
     SELECT a.INCIDENT_ID,
         REPORTED_DATE,
         SUBMIT_DATE,
         RESPONDED_DATE,
         RESOLVED_DATE,
         PENDING_TIME,
         REOPENED_DATE,
         PRIORITY,
         SERVICE_TYPE,
         SUMMARY,
         NOTES,
         a.ROOT_CAUSE ori_root_cause,
         RESOLUTION,
         a.STATUS,
         STATUS_REASON,
         PRODUCT_CATEGORIZATION_TIER1,
         PRODUCT_CATEGORIZATION_TIER2,
         closure_product_category_tier3 PRODUCT_CATEGORIZATION_TIER3,
         OPERATIONAL_CATEGORIZATION1,
         OPERATIONAL_CATEGORIZATION2,
         OPERATIONAL_CATEGORIZATION3,
         ASSIGNED_SUPPORT_ORGANIZATION,
         ASSIGNED_GROUP,
         ASSIGNEE,
         SUBMITTER,
         INTERNET_EMAIL,
         COUNTRY,
         RESPONSE_TIME_SLA,
         RESOLUTION_TIME_SLA,
         IS_RE_OPEN,
         GROUP_TRANSFERS,
         TOTAL_TRANSFERS,
         INDIVIDUAL_TRANSFERS,
         DEPARTMENT,
         CLOSED_DATE,
         SITE,
         AD_COUNTRY,
         PHONE_NUM,
         TEL,
         b.rc_category,
         b.root_cause root_cause,
         b.problem_category,
         b.issue_category,
         b.issue,
         b.issue_comment,
         b.sub_biz,
         b.release,
         b.ta_status
         FROM    z_itsm_incident a
         LEFT JOIN
            z_itsm_ticket_analyze b
         ON a.incident_id = b.incident_id
where a.closure_product_category_tier3 IN ('COST FCST')
                 AND a.assigned_group <> 'Monitoring'
    '''
    if params.get('assigned_group',''):
        list =",".join(["'"+temp+"'" for temp in params.get('assigned_group').split(",")])
        sql_text=sql_text+' and a.assigned_group in (' + list+')'
    if params.get('incident_id',None):
        sql_text=sql_text+' and a.incident_id = :incident_id'
    if params.get('ta_status',None):
        sql_text=sql_text+" and nvl(b.ta_status,'initial') = :ta_status"
    if params.get('assignee',None):
        sql_text=sql_text+' and assignee = :assignee'
    params['from_date']=datetime.strptime(params['from_date'],cfg.DATE_FORMAT)
    params['to_date']=datetime.strptime(params['to_date'],cfg.DATE_FORMAT)
    sql_text =sql_text+" and status<>'Cancelled' and a.submit_date >= :from_date and a.submit_date <= :to_date  order by submit_date"
    resultProxy = DBSession.execute(text(sql_text),params)
    result = resultProxy.fetchall()
    resultProxy.close()
    return result


@extdirect_method(action='itsm',request_as_last_param=True)
def save_ticket_analyze(params,request):
    params=request.json_body
    data=params['data'][0]
    print(request.json_body)
    ta = TicketAnalyze()
    for key in data.keys():
        if hasattr(ta,key):
            setattr(ta,key,data[key])
    DBSession.merge(ta)
    DBSession.flush()
    return dict(success=True)


@extdirect_method(action='itsm',request_as_last_param=True)
def get_ticket_users(params,request):
    query = DBSession.query(TicketUsers)
    if params.get('internet_email',''):
        query = query.filter(TicketUsers.internet_email==params['internet_email'])
    if params.get('itcode',''):
        query = query.filter(TicketUsers.itcode==params['itcode'])
    if params.get('unreview',''):
        query = query.filter(TicketUsers.function_group==None)
    result = query.all()
    return result

@extdirect_method(action='itsm',request_as_last_param=True)
def save_ticket_users(params,request):
    params=request.json_body
    data=params['data'][0]
    print(request.json_body)
    ta = TicketUsers()
    for key in data.keys():
        if hasattr(ta,key):
            setattr(ta,key,data[key])
    DBSession.merge(ta)
    DBSession.flush()
    return dict(success=True)

@extdirect_method(action='itsm',request_as_last_param=True)
def sync_ticket_users(params,request):
    Session=cfg.Session()
    if params['new_user']:
        Session.execute('''
        insert into z_itsm_conf_user_info
           (internet_email)
           select distinct internet_email from z_itsm_incident a where assigned_group='i2 COST FCST'
           and not exists (select 1 from z_itsm_conf_user_info b where b.internet_email=a.internet_email)
           and internet_email is not null 
        ''')
        Session.commit()
        
    Session.execute('''
        update z_itsm_conf_user_info
        set itcode =lower(substr(internet_email,1,instr(internet_email,'@')-1))
         where itcode is null and internet_email like '%@%' and  internet_email not like '% %'
        ''')
    Session.commit()
    
    if params['type']=='nc':
        user_list = DBSession.query(TicketUsers).filter(TicketUsers.email==None).filter(TicketUsers.itcode != None).all()
    if  params['type']=='full':
        user_list = DBSession.query(TicketUsers).filter(TicketUsers.itcode != None).all()
    
    from toolbox.common.lp import Ldap 
    l=Ldap()
    l.connect('lidm1','(dx2@2xmy)')
    for user in user_list:
        user_lp = l.search(user.itcode)
        if user_lp:
            user.country = user_lp['c'][0]
            user.last_name = user_lp['displayName'][0]
            user.first_name = user_lp['displayName'][0]
            user.email = user_lp['sAMAccountName'][0]+'@lenovo.com'
            user.org_id = user_lp.get('department',[None])[0]
            user.phone = user_lp.get('telephoneNumber',[None])[0];
            user.state = user_lp['l'][0];
            DBSession.merge(user)
    return dict(success=True,data=user_list)