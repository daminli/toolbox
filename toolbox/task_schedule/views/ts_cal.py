# coding = utf8

from sqlalchemy.orm import joinedload, subqueryload
from sqlalchemy import and_
import json, datetime

from ..models import SystemList, ScheduleCalDefine, ScheduleCalDetail

from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from cfg import DBSession

@view_config(route_name='systemtree', renderer='json')
def system_tree(request):
    result = DBSession.query(SystemList).filter(SystemList.status == 'ACTIVE').order_by(SystemList.groupName, SystemList.systemName).all()
    systemTree = []
    groupName = 'NULL'
    systemList = []
    for row in result:
        if(groupName != row.groupName):
            groupName = row.groupName
            systemList = []
            systemTree.append({'text':row.groupName, 'leaf':'false', 'children':systemList})
        systemList.append({'text':row.systemName, 'leaf':'true'})
    return systemTree

@view_config(route_name='cal_define', renderer='json')
def cal_define(request):
    try:
        systemName = request.GET['systemName']
    except KeyError:
        return 'NO system Name Error'
    result = DBSession.query(ScheduleCalDefine).filter(ScheduleCalDefine.status == 'ACTIVE').filter(ScheduleCalDefine.systemName == systemName).order_by(ScheduleCalDefine.systemName, ScheduleCalDefine.timeCode, ScheduleCalDefine.runid).all()
    return result

@view_config(route_name='cal_detail', renderer='json')
def cal_detail(request):
    try:
        systemName = request.GET['systemName']
        fromDate = request.GET['fromDate']
        fromTime = request.GET['fromTime']
        toDate = request.GET['toDate']
        toTime = request.GET['toTime']
    except KeyError:
        return 'NO system Name Error' 
    
    fromDateTime = datetime.datetime.strptime(fromDate.split('T')[0] + ' ' + fromTime.split('T')[1], '%Y-%m-%d %H:%M:%S')
    toDateTime = datetime.datetime.strptime(toDate.split('T')[0] + ' ' + toTime.split('T')[1], '%Y-%m-%d %H:%M:%S')
    #return sqlalchjson.dumps(request.args)
    #return datetime.date.today().__str__()
    result = DBSession.query(ScheduleCalDetail)\
    .filter(and_(ScheduleCalDetail.systemName == systemName, \
                ScheduleCalDetail.startTime >= fromDateTime, \
                ScheduleCalDetail.startTime <= toDateTime))\
           .order_by(ScheduleCalDetail.systemName, ScheduleCalDetail.startTime, ScheduleCalDetail.runid).all()
    return result
