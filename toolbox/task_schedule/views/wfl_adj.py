# coding = utf8

from cfg import DBSession
from ..models import SystemList,WflAdjustment
from sqlalchemy.orm import joinedload,subqueryload
from pyramid.view import view_config

@view_config(route_name='wfl_adj_list', renderer='json')
def wfl_adj_list(request):
    result = DBSession.query(WflAdjustment.adjBatchName).group_by(WflAdjustment.adjBatchName).order_by(WflAdjustment.adjBatchName.desc()).all()
    adjList = []
    for row in result:
        adjList.append({'adjBatchName':row.adjBatchName})
    return adjList

@view_config(route_name='wfl_adj', renderer='json')
def wfl_adj(request):
    #import pydevd;pydevd.settrace()
    adjname = request.matchdict['adjname']
    result = DBSession.query(SystemList).join(WflAdjustment).filter(SystemList.systemName==WflAdjustment.systemName).filter(WflAdjustment.adjBatchName==adjname).order_by(SystemList.groupName).all()
    jsonResult={}
    groupList = []
    temGroup = ""
    temp = {}
    for row in result:
        if temGroup <> row.groupName:
            temGroup = row.groupName
            temp = {'runId':temGroup,'children':[]}
            groupList.append(temp)
        adjList = []
        for adj in row.children:
            if adj.adjBatchName == adjname:
                adjList.append({'runId':adj.runId,'startTime':adj.startTime,'action':adj.action,'leaf':True}) 
        temp['children'].append({'runId':row.systemName,'children':adjList})
    #groupList=[{'runId':'Test'},{'runId':'Test2'}]
    callBackKey = request.args.get('callback')
    if callBackKey is not None:
        return callBackKey+'('+groupList+');'
    else:
        return groupList