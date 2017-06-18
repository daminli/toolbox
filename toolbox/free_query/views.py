import json, uuid, os
from datetime import date,datetime,timedelta

from flask import request, url_for, redirect,render_template, current_app,g,send_from_directory
from flask_json import json_response, as_json
from flask_login import logout_user, login_user, login_required, current_user


from util.id_generator import IdGenerator
from .models import FolderTree, Reports, FreeQuery,ReportProp

from .exceptions import MissReqFilter
from .. import free_query
from . import freequery
import cfg

app=current_app
lm = current_app.login_manager
db=g.db



def getChildFolder(parent_folder):
    '''
    get whole report folder tree structure 
    '''
    temps = FolderTree.query.filter(FolderTree.parent_id == parent_folder['id']).all()
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

@freequery.route('/report_folder',methods = ['GET','POST'])
@login_required
def report_folder():
    """
    get the report folder tree structure json data
    """
    if request.values.get('root_id',False):
        temp = FolderTree.query.filter(FolderTree.id == request.values.get('root_id')).first()
        report_folder = dict(
                id=temp.id,
                text=temp.name,
                expanded=True)
        getChildFolder(report_folder)
        return json_response(children=report_folder)
    else:
        temp = FolderTree.query.filter(FolderTree.id == '2').first()
        private_folder = dict(
                id=temp.id,
                text=temp.name,
                expanded=True)
        getChildFolder(private_folder)
        temp = FolderTree.query.filter(FolderTree.id == '1').first()
        public_folder = dict(
                id=temp.id,
                text=temp.name,
                expanded=True)
        getChildFolder(public_folder)
        return json_response(children=public_folder) 
    
@freequery.route('/get_folder',methods = ['GET','POST'])
@login_required
def get_folder():
    folder_id = request.values['folder_id']
    folders = FolderTree.query.filter(FolderTree.id == folder_id).all()
    return json_response(data=folders)

@freequery.route('/save_folder',methods = ['GET','POST'])
@login_required
def save_folder():
    params = request.values
    folder=None
    if params.get('id',None):
        folder = FolderTree.query.filter(FolderTree.id==params['id']).first()
    if not folder:
        folder = FolderTree()
    for key in params.keys():
        if hasattr(folder, key)  and key!='id':
            setattr(folder,key,params[key])
    folder.create_by=current_user.login_name
    folder = db.session.merge(folder)
    db.session.flush()
    return json_response(success=True,data=folder)


@freequery.route('/delete_folder',methods = ['GET','POST'])
@login_required
def delete_folder():
    params = request.values
    folder_id =request.values['id']
    sub_folder = FolderTree.query.filter(FolderTree.parent_id==folder_id).all()
    if sub_folder:
        return json_response(success=False,data=dict(error='Sub folder found'))
    reports = Reports.query.filter(Reports.folder_id==folder_id).all()
    if reports:
        return json_response(success=False,data=dict(error='Reports found in this folder'))
    folder = FolderTree.query.filter(FolderTree.id==folder_id).first()
    if folder:
        db.session.delete(folder)
        db.session.flush()
    return json_response(success=True,data=folder)

@freequery.route('/search_report',methods = ['GET','POST'])
@login_required
def search_report():
    """
    get the report folder tree structure json data
    """
    params = request.values
    query = Reports.query
    if params.get('folder_id',None):
        query= query.filter(Reports.folder_id == params['folder_id'])
    if params.get('id',None):
        query= query.filter(Reports.id == params['id'])
    query= query.filter(Reports.status == 'ACTIVE')
    reports = query.all()
    return json_response(data=reports)


@freequery.route('/show_report',methods = ['GET','POST'])
@login_required
def show_report():
    """
    get the report column and fields
    """
    report_id = request.values['id']
    free_query = FreeQuery(report_id)
    return json_response(columns=free_query.get_column_model(), fields=free_query.get_data_model(),req_filter=free_query.req_filter())

@freequery.route('/report_data',methods = ['GET','POST'])
@login_required
def report_data():
    """
    get the report json data
    #http://localhost:6543/free_query/report_data?id=2&_dc=1369040490834&page=1&start=0&limit=50
    """
    filters=json.loads(request.values.get("filters","[]")) #the filter object is a string, need convert to python objects
    pages = {}
    pages["start"] = request.values.get("start", 0)
    pages["end"] = int(pages["start"]) + int(request.values.get("limit", 50))
    sorters = []
    try:
        sorters.append(dict(sort=request.values["sort"], dir=request.values["dir"]))
    except KeyError as e:
        pass
    report_id = request.values['id']
    free_query = FreeQuery(report_id)
    result = free_query.get_result(pages=pages,filters=filters, sorters=sorters)
    return json_response(**result)

@freequery.route('/report_filter',methods = ['GET','POST'])
@login_required
def report_filter():
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
    report_id = request.values['id']
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
    return json_response(filter_form=filter_form)

@freequery.route('/filter_list',methods = ['GET','POST'])
@login_required
def filter_list():
    """
    get the filter selection list for the list filter type
    """
    report_id = request.values['id']
    filter_name = request.values['name']
    filters = []
    try:
        query = request.values["query"]
        # {"field":"company","data":{"type":"string","value":"A"}},
        if query:
            filters = [dict(field=filter_name, data=dict(type="string", comparison="contain", value=query))]
    except KeyError:
        pass
    free_query = FreeQuery(report_id)
    filter_list = free_query.get_filter_list(filter_name, filters=filters)
    return json_response(filter_list=filter_list)

@freequery.route('/export_report',methods = ['GET','POST'])
@login_required
def export_report():
    """
    export report data to excel
    """
    exp_dir=cfg.FREE_QUERY_EXP_DIR
    filters=json.loads(request.values.get("filters","[]")) #the filter object is a string, need convert to python objects
    print('*'*40)
    print(filters)
    sorters = []
    try:
        sorters.append(request.values["sorters"])
    except KeyError as e:
        pass
    report_id = request.values['id']
    free_query = FreeQuery(report_id)
    exp_info = free_query.export_report(filters=filters, sorters=sorters,exp_dir=exp_dir,user_id=current_user.login_name)
    return json_response(data=exp_info,success=True)

@freequery.route('/download_report',methods = ['GET','POST'])
@login_required
def download_report():
    exp_dir=cfg.FREE_QUERY_EXP_DIR
    url=request.matchdict['url']
    full_name=exp_dir+'/'+url
    (dir_name,file_name)= os.path.split(full_name)
    return send_from_directory(dir_name,file_name,as_attachment=True)

@freequery.route('/save_report',methods = ['GET','POST'])
@login_required
def save_report():
    '''
    save report to data base
    params['report'] :  report's basic information
    params['report_props'] :  report's basic information
    '''
    params = request.values
    report=None
    if params.get('id',None):
        report = Reports.query.filter(Reports.id==params['id']).first()
    if not report:
        report = Reports()
    for key in params.keys():
        if hasattr(report, key)  and key!='id':
            setattr(report,key,params[key])
    report.create_by=current_user.login_name
    report = db.session.merge(report)
    db.session.flush()
    return json_response(success=True,data=report)

@freequery.route('/delete_report',methods = ['GET','POST'])
@login_required
def delete_report():
    params = request.valuess
    report_id =request.params['id']
    report = Reports.query.filter(Reports.id==report_id).first()
    if not report:
        return dict(success=False,data=dict(error="report doesn't exits"))
    else:
        report.status='DELETED'
        db.session.merge(report)
        db.session.flush()
    return json_response(success=True,data=report)

@freequery.route('/refresh_report_props',methods = ['GET','POST'])
@login_required
def refresh_report_props():
    '''
    refresh report props
    params['report_id'] :  the report to refresh
    '''
    report_id = request.values['report_id']
    free_query = FreeQuery(report_id)
    free_query.refresh_props()
    return json_response(report_props=free_query.get_props())

@freequery.route('/get_report_props',methods = ['GET','POST'])
@login_required
def get_report_props():
    '''
    get report props by report_id
    '''
    report_id = request.values.get('report_id',None)
    if report_id:
        free_query = FreeQuery(report_id)
        return json_response(report_props=free_query.get_props())
    else:
        return json_response(report_props=save_report_props(request))
    

@freequery.route('/save_report_props',methods = ['GET','POST'])
@login_required
def save_report_props():
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
    db.session.merge(rpt_prop)
    db.session.flush()
    return json_response(success=True)
