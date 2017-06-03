import json,os

from pyramid.response import (FileResponse,Response)
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

import cfg
from models import FolderTree, Reports, FreeQuery,ReportProp
from util.id_generator import IdGenerator
from exceptions import MissReqFilter
from .. import free_query

DBSession=cfg.DBSession

def getChildFolder(parent_folder):
    '''
    get whole report folder tree structure 
    '''
    temps = DBSession.query(FolderTree).filter(FolderTree.parent_id == parent_folder['id']).all()
    if temps.__len__() == 0:
        parent_folder['leaf'] = "true"
    else:
        parent_folder['children'] = []
    for temp in temps:
        folder = dict(
                        id=temp.id,
                        text=temp.name,
                        activity=temp.name,
                        expanded=True
                    )
        parent_folder['children'].append(folder)
        getChildFolder(folder)

@view_config(route_name='report_folder', renderer='json')
def report_folder(request):
    """
    get the report folder tree structure json data
    """
    if request.params.get('root_id',False):
        temp = DBSession.query(FolderTree).filter(FolderTree.id == request.params.get('root_id')).first()
        report_folder = dict(
                id=temp.id,
                text=temp.name,
                expanded=True)
        getChildFolder(report_folder)
        return [report_folder]
    else:
        temp = DBSession.query(FolderTree).filter(FolderTree.id == '2').first()
        private_folder = dict(
                id=temp.id,
                text=temp.name,
                expanded=True)
        getChildFolder(private_folder)
        temp = DBSession.query(FolderTree).filter(FolderTree.id == '1').first()
        public_folder = dict(
                id=temp.id,
                text=temp.name,
                expanded=True)
        getChildFolder(public_folder)
        return [private_folder, public_folder]
    
@view_config(route_name='get_folder', renderer='json')
def get_folder(request):
    folder_id = request.params['folder_id']
    folders = DBSession.query(FolderTree).filter(FolderTree.id == folder_id).all()
    return folders

@view_config(route_name='save_folder', renderer='json')
def save_folder(request):
    params = request.params
    print(params)
    folder=None
    if params.get('id',None):
        folder = DBSession.query(FolderTree).filter(FolderTree.id==params['id']).first()
    if not folder:
        folder = FolderTree()
    for key in params.keys():
        if hasattr(folder, key)  and key!='id':
            setattr(folder,key,params[key])
    folder.create_by=authenticated_userid(request)
    folder = DBSession.merge(folder)
    DBSession.flush()
    return dict(success=True,data=folder)

@view_config(route_name='delete_folder', renderer='json')
def delete_folder(request):
    params = request.params
    folder_id =request.params['id']
    sub_folder = DBSession.query(FolderTree).filter(FolderTree.parent_id==folder_id).all()
    if sub_folder:
        return dict(success=False,data=dict(error='Sub folder found'))
    reports = DBSession.query(Reports).filter(Reports.folder_id==folder_id).all()
    if reports:
        return dict(success=False,data=dict(error='Reports found in this folder'))
    folder = DBSession.query(FolderTree).filter(FolderTree.id==folder_id).first()
    if folder:
        DBSession.delete(folder)
        DBSession.flush()
    return dict(success=True,data=folder)

@view_config(route_name='search_report', renderer='json')
def search_report(request):
    """
    get the report folder tree structure json data
    """
    params = request.params
    print(params)
    query = DBSession.query(Reports)
    if params.get('folder_id',None):
        query= query.filter(Reports.folder_id == params['folder_id'])
    if params.get('id',None):
        query= query.filter(Reports.id == params['id'])
    query= query.filter(Reports.status == 'ACTIVE')
    reports = query.all()
    return reports

@view_config(route_name='show_report', renderer='json')
def show_report(request):
    """
    get the report column and fields
    """
    report_id = request.params['id']
    free_query = FreeQuery(report_id)
    return dict(columns=free_query.get_column_model(), fields=free_query.get_data_model(),req_filter=free_query.req_filter())

@view_config(route_name='report_data', renderer='json')
def report_data(request):
    """
    get the report json data
    #http://localhost:6543/free_query/report_data?id=2&_dc=1369040490834&page=1&start=0&limit=50
    """
    filters=json.loads(request.params.get("filters","[]")) #the filter object is a string, need convert to python objects
    pages = {}
    pages["start"] = request.params.get("start", 0)
    pages["end"] = int(pages["start"]) + int(request.params.get("limit", 50))
    sorters = []
    try:
        sorters.append(dict(sort=request.params["sort"], dir=request.params["dir"]))
    except KeyError, e:
        pass
    report_id = request.params['id']
    free_query = FreeQuery(report_id)
    result = free_query.get_result(pages=pages,filters=filters, sorters=sorters)
    return result

@view_config(route_name='report_filter', renderer='json')
def report_filter(request):
    """
    get report filter model to generate filter form
    filter_type:
    string   :  {
                fieldLabel: 'Default',
                type: 'textfield'
                name: 'basic',
                value: 1,
                minValue: 1,
                maxValue: 125
            }
     number : {
                fieldLabel: 'Default',
                type: 'numberfield',
                name: 'basic',
                allowBlank: false
     },
     date : {
               fieldlabel:'start date',
               type:'datefield',
               name:'start_date',
               allowBlank: true
     },
     list: {
          complex
     }
    """
    report_id = request.params['id']
    free_query = FreeQuery(report_id)
    filter_model = free_query.get_filter_model()
    filter_form = []
    for filter in filter_model:
        filter_field = {}
        filter_type = filter["filter_type"]
        if filter_type == 'string':
            filter_field = dict(fieldLabel=filter["label"], filter_type=filter_type, xtype='textfield', name=filter["name"],allowBlank=not filter['req_filter'])
        if filter_type == 'date':
            filter_field = dict(xtype='container',
                                layout='hbox', margin='0 0 5 0',
                                items=[dict(xtype='datefield', filter_type=filter_type, comparison='eq', name=filter["name"], fieldLabel=filter["label"],allowBlank=not filter['req_filter']),
                                        dict(xtype='datefield', filter_type=filter_type, comparison='gt', name=filter["name"], margin='0 0 0 50', labelWidth=30, fieldLabel='From',allowBlank=not filter['req_filter']),
                                        dict(xtype='datefield', filter_type=filter_type, comparison='lt', name=filter["name"], margin='0 0 0 5', labelWidth=20, fieldLabel='To',allowBlank=not filter['req_filter'])
                                        ])
        if filter_type == 'number':
            filter_field = dict(xtype='container',
                                layout='hbox', margin='0 0 5 0',
                                items=[
                                        dict(xtype='numberfield', name=filter["name"] , filter_type=filter_type, comparison='eq', fieldName=filter["name"], fieldLabel=filter["label"],allowBlank=not filter['req_filter']),
                                        dict(xtype='numberfield', name=filter["name"], filter_type=filter_type, comparison='gt', margin='0 0 0 50', labelWidth=20, fieldLabel='>',allowBlank=not filter['req_filter']),
                                        dict(xtype='numberfield', name=filter["name"], filter_type=filter_type, comparison='lt', margin='0 0 0 20', labelWidth=20, fieldLabel='<',allowBlank=not filter['req_filter'])
                                        ])
        if filter_type == 'list':
            filter_field = dict(xtype="combo",
                        fieldLabel=filter["label"],
                        multiSelect=True,
                        displayField='text',
                        valueField='value',
                        filter_type=filter_type,
                        name=filter["name"],
                        filter_name=filter["name"],
                        queryMode='remote',
                        allowBlank=not filter['req_filter'])
        filter_form.append(filter_field)
    return filter_form

@view_config(route_name='filter_list', renderer='json')
def filter_list(request):
    """
    get the filter selection list for the list filter type
    """
    report_id = request.params['id']
    filter_name = request.params['name']
    filters = []
    try:
        query = request.params["query"]
        # {"field":"company","data":{"type":"string","value":"A"}},
        if query:
            filters = [dict(field=filter_name, data=dict(type="string", comparison="contain", value=query))]
    except KeyError:
        pass
    free_query = FreeQuery(report_id)
    filter_list = free_query.get_filter_list(filter_name, filters=filters)
    return filter_list

@view_config(route_name='export_report', renderer='json')
def export_report(request):
    """
    export report data to excel
    """
    exp_dir=cfg.config.registry.settings.get('free_query.export_dir')
    filters=json.loads(request.params.get("filters","[]")) #the filter object is a string, need convert to python objects
    print('*'*40)
    print(filters)
    sorters = []
    try:
        sorters.append(request.params["sorters"])
    except KeyError, e:
        pass
    report_id = request.params['id']
    free_query = FreeQuery(report_id)
    exp_info = free_query.export_report(filters=filters, sorters=sorters,exp_dir=exp_dir,user_id=authenticated_userid(request))
    return dict(data=exp_info,success=True)

@view_config(route_name='download_report')
def download_report(request):
    settings =cfg.config.registry.settings
    exp_dir=settings.get('free_query.export_dir')
    url=request.matchdict['url']
    full_name=exp_dir+'/'+url
    response= FileResponse(full_name, request=request)
    (dir_name, file_name) = os.path.split(full_name)
    response.content_disposition = 'attachment; filename="'+file_name+'"'
    return response

@view_config(route_name='save_report', renderer='json')
def save_report(request):
    '''
    save report to data base
    params['report'] :  report's basic information
    params['report_props'] :  report's basic information
    '''
    params = request.params
    report=None
    if params.get('id',None):
        report = DBSession.query(Reports).filter(Reports.id==params['id']).first()
    if not report:
        report = Reports()
    for key in params.keys():
        if hasattr(report, key)  and key!='id':
            setattr(report,key,params[key])
    report.create_by=authenticated_userid(request)
    report = DBSession.merge(report)
    DBSession.flush()
    return dict(success=True,data=report)

@view_config(route_name='delete_report', renderer='json')
def delete_report(request):
    params = request.params
    report_id =request.params['id']
    report = DBSession.query(Reports).filter(Reports.id==report_id).first()
    if not report:
        return dict(success=False,data=dict(error="report doesn't exits"))
    else:
        report.status='DELETED'
        DBSession.merge(report)
        DBSession.flush()
    return dict(success=True,data=report)

@view_config(route_name='refresh_report_props', renderer='json')
def refresh_report_props(request):
    '''
    refresh report props
    params['report_id'] :  the report to refresh
    '''
    report_id = request.params['report_id']
    free_query = FreeQuery(report_id)
    free_query.refresh_props()
    return free_query.get_props()

@view_config(route_name='get_report_props', renderer='json')
def get_report_props(request):
    '''
    get report props by report_id
    '''
    report_id = request.params.get('report_id',None)
    if report_id:
        free_query = FreeQuery(report_id)
        return free_query.get_props()
    else:
        return save_report_props(request)
    

@view_config(route_name='save_report_props', renderer='json')
def save_report_props(request):
    '''
    save report to data base
    params['report'] :  report's basic information
    params['report_props'] :  report's basic information
    '''
    rpt_props=request.json_body
    print(request.json_body)
    rpt_prop = ReportProp()
    for key in rpt_props.keys():
        if hasattr(rpt_prop,key):
            setattr(rpt_prop,key,rpt_props[key])
    DBSession.merge(rpt_prop)
    DBSession.flush()
    return dict(success=True)
