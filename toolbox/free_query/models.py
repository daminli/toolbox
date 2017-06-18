# coding=utf-8
'''
Created on 2013-5-8

@author: lidm1
'''
from datetime import datetime
import types

from flask import g
from sqlalchemy import (DateTime,String,Column,Text,Integer,Boolean,Index,text)
from sqlalchemy.orm import (validates,relationship, backref)

from . import exportor

from .exceptions import MissReqFilter
from util.selection.models import Selection
from util.datasource.models import DataSourceEngine
from util.id_generator import IdGenerator

import cfg

db=g.db


Base=db.Model

class Reports(Base):
    __tablename__ = 'fq_reports'
    id = Column('id',String(32),primary_key=True,default = IdGenerator('REPORT_ID').nextval)
    name = Column('name',String(64))
    display_name = Column('display_name',String(64))
    rpt_desc = Column('rpt_desc',String(300))
    folder_id = Column('folder_id',String(32))
    sql_query = Column('sql_query',Text)
    datasource = Column('datasource',String(32))
    status=Column('sys_ent_status',String(10),default='ACTIVE')
    creation_date = Column('creation_date',DateTime,default =datetime.now)
    create_by = Column('create_by',String(32))
    __table_args__ = (Index('my_index', 'name', 'folder_id',unique=True),)
    
class FolderTree(Base):
    __tablename__ = 'fq_folder_tree'
    id = Column('id',String(32),primary_key=True,default = IdGenerator('RPT_FOLDER').nextval)
    name = Column('name',String(64))
    parent_id = Column('parent_id',String(32))
    creation_date = Column('creation_date',DateTime,default =datetime.now)
    create_by = Column('create_by',String(32))
    
class ReportProp(Base):
    __tablename__ = 'fq_report_prop'
    rpt_id = Column('rpt_id',String(32),primary_key=True)
    col_name = Column('col_name',String(30),primary_key=True)
    data_type = Column('data_type',String(30))
    display_name = Column('display_name',String(64))
    format = Column('format',String(64))
    seq = Column('seq',Integer)
    is_filter = Column('is_filter',Boolean,default =False)
    req_filter = Column('req_filter',Boolean,default=False)
    filter_type = Column('filter_type',String(32))
    selection=Column('selection',String(32))
    width = Column('width',Integer)
    
class ExportLog(Base):
    __tablename__ = 'fq_export_log'
    id = Column('id',String(32),primary_key=True,default = IdGenerator('RPT_EXP').nextval)
    rpt_id = Column('rpt_id',String(32))
    url = Column('url',String(100))
    start_time = Column('start_time',DateTime)
    query_end_time = Column('query_end_time',DateTime)
    end_time = Column('end_time',DateTime)
    status = Column('status',String(32))
    total_cnt = Column('total_cnt',Integer)
    exp_type = Column('exp_type',String(10))
    format=Column('format',String(10))
    zip=Column('zip',String(10))
    file_size=Column('file_size',Integer)
    export_by = Column('export_by',String(32))
    
class DownloadLog(Base):
    __tablename__ = 'fq_download_log'
    id = Column('id',String(32),primary_key=True)
    exp_id = Column('exp_id',String(32))
    download_date = Column('download_date',DateTime)
    download_by = Column('download_by',String(30))
    
class UdReports(Base):
    __tablename__ = 'fq_ud_reports'
    id = Column('id',String(32),primary_key=True)
    rpt_id = Column('rpt_id',String(32))
    owner = Column('owner',String(32))
    folder_id = Column('folder_id',String(32))
    creation_date = Column('creation_date',DateTime)
    create_by = Column('create_by',String(32))
    
class UdReportsDetail(Base):
    __tablename__ = 'fq_ud_reports_detail'
    ud_rpt_id = Column('ud_rpt_id',String(32),primary_key=True)
    ud_type = Column('ud_type',String(32),primary_key=True)
    ud_detail = Column('ud_detail',Text)
    
    
class FreeQuery(object):
    """
    This class is main_logic for free Query
    """
    def __init__(self,report_id):
        assert report_id is not None
        self.report_id = report_id
        self.report = Reports.query.filter(Reports.id == self.report_id).first()
        assert self.report
        self.rpt_props =None
        result=ReportProp.query.filter(ReportProp.rpt_id == self.report_id).order_by(ReportProp.seq).all()
        self.rpt_props =result
        self.data_source = DataSourceEngine(self.report.datasource)
        
    def get_sql(self, selectors=[],filters=[],groups=[],distinct=False,sorters=[],pages=[]):
        """
        generate sql from sql_query and report_prop
        
        selectors : the return columns 
                        sample: [" rownum row_num"]
        filters: filter params
                 sample: []
        """
        base_sql =  self.report.sql_query
        assert base_sql is not None
        if distinct:
            select_sql = 'select distinct '
        else:
            select_sql = 'select '
        if not selectors:
            selectors=[] #don't change selectors directly
            #selectors.append("rownum row_num")
            for prop in self.rpt_props:
                selectors.append(prop.col_name)
        select_sql += ", " . join(selectors)
        select_sql += " from "
        condition = self.build_where(filters)
        
        order_sql = self.build_sort(sorters)
        group_sql = self.build_group(groups)
        sql_text = select_sql + "("+base_sql+") as a " +condition["where_sql"] + group_sql + order_sql
        return dict(sql_text=sql_text,params=condition["params"])
    
    def check_req_filter(self,filters):
        """
        check the required filters
        """
        for prop in self.rpt_props:
            if prop.req_filter:
                hasFilter=False
                for filter in filters:
                    if filter["field"].lower()==prop.col_name.lower():
                        hasFilter=True
                        break
                if not hasFilter:
                    raise MissReqFilter(prop.col_name)
        return True
    
    def build_where(self,filters=[]):
        """
        build where sql
        filter sample data : [
           {"field":"company","data":{"type":"string","value":"A"}},
           {"field":"price","data":{"type":"numeric","comparison":"gt","value":30}},
           {"field":"size","data":{"type":"list","value":["medium","large"]}}
           ]
        """
        def build_condition(filter):
            try:
                filter_type = filter["data"]["type"]
                comparison = filter["data"].get("comparison","null")
                field_name = filter["field"]
                field_value = filter["data"]["value"]
                param_key = field_name+"_"+comparison
                if filter_type == "list":
                    list =",".join(["'"+temp+"'" for temp in field_value])
                    return field_name +" in ("+list+")"
                if filter_type == "string":
                    if comparison == "contain":
                        params[param_key] = "%"+field_value+"%"
                        return field_name +" like :"+param_key
                    if comparison == "start_with":
                        params[param_key] = field_value+"%"
                        return field_name +" like :"+param_key
                    if comparison == "end_with":
                        params[param_key] = "%"+field_value
                        return field_name +" like :"+param_key
                    if comparison == "in":
                        list =",".join(["'"+temp+"'" for temp in field_value.split(",")])
                        return field_name +" in ("+list+")"
                    if comparison == "eq":
                        params[param_key] = field_value
                        return field_name +" = :"+param_key
                    
                    try:
                        i = field_value.index("*")
                        field_value = field_value.replace("*", "%")
                        params[param_key] = field_value
                        return field_name +" like :"+param_key
                    except ValueError:
                        pass
                    
                    try:
                        i = field_value.index(",")
                        list =",".join(["'"+temp+"'" for temp in field_value.split(",")])
                        return field_name +" in ("+list+")"
                    except ValueError:
                        params[param_key] = field_value
                        return field_name +" = :"+param_key
                    
                if filter_type == "number":
                    params[param_key] = field_value
                    if comparison == "eq":
                        return field_name +" = :"+param_key
                    if comparison == "gt":
                        return field_name +" > :"+param_key
                    if comparison == "lt":
                        return field_name +" < :"+param_key
                if filter_type == "date":
                    if type(field_value) is not type(datetime.now()):
                        params[param_key] = datetime.strptime(field_value,cfg.DATE_FORMAT)
                    else:
                        print(field_value+'*******************************')
                        params[param_key] = field_value
                    if comparison == "eq":
                        return field_name +" = :"+param_key
                    if comparison == "gt":
                        return field_name +" > :"+param_key
                    if comparison == "lt":
                        return field_name +" < :"+param_key
            except KeyError:
                return filter["field"] +" ="+ filter["data"]["value"]
            
        params={}
        where_sql = " and ".join([build_condition(filter) for filter in filters])
        where_sql = "  where " + where_sql if where_sql else ""
        return dict(where_sql=where_sql,params=params)
        
    def build_sort(self,sorters=[]):
        """
        build order by sql:
        sorters sample data : [{"sort":"name","dir":"desc"}]
        """
        order_sql = ", ".join([sort["sort"]+" "+sort["dir"] for sort in sorters])
        return " order by " + order_sql if order_sql else ""
    
    def build_group(self,groups=[]):
        """
        build group by sql:
        sorters sample data : ["name","type"]
        """
        group_sql = ", ".join(groups)
        
        return " group by " + group_sql if group_sql else ""
    
    def get_result(self,filters=[],sorters=[],pages={"start":0,"end":50}):
        """
        get the report result data
        """
        pages={"start":0,"end":200}
        self.check_req_filter(filters)
        sql = self.get_sql(filters=filters,sorters=sorters,pages=pages)
        sql_text = sql["sql_text"]
        params=sql["params"]
        
        conn = self.data_source.engine.connect()
        try:
            '''
            try:
                self.rowcount = self.rowcount
            except AttributeError:
                self.rowcount=conn.execute(text("select count(1) from ("+sql_text+") "),params).scalar()
            '''
            if self.data_source.engine.dialect.name=='oracle':
                sql_text = "select rownum row_num,b.* from ("+sql_text+") as b where rownum <="+str(pages['end'])
            if self.data_source.engine.dialect.name=='postgresql':
                sql_text = "select b.* from ("+sql_text+") as b limit "+str(pages['end'])
            if self.data_source.engine.dialect.name=='hana':
                assert(1==2)
            resultProxy=conn.execute(text(sql_text),dict(params,**pages))
            result = resultProxy.fetchall()
            self.rowcount=resultProxy.rowcount
            resultProxy.close()
        finally:
            conn.close()
        return dict(total_count=self.rowcount,data=result)
    
    def export_report(self,filters=[],sorters=[],exp_dir=None,user_id=None,exp_type='direct',format='csv',zip='auto'):
        """
        export report data to excel
        type: ['direct','achived']
                 direct : export to temp folder after export deleted
                 achived: export to server will keep to expired
        format:['csv', 'xls']
        zip: ['auto','yes','no']
               auto: if file is > 5M will zip auto, if file < 5M will not zip
               yes: zip always
               no: doesn't zip
        """
        DBSession=db.session
        exp_log=ExportLog(rpt_id=self.report_id,start_time=datetime.now())
        DBSession.begin(subtransactions=True)
        exp_log.status='initial'
        exp_log.export_by=user_id
        exp_log= DBSession.merge(exp_log)
        DBSession.commit()
        self.check_req_filter(filters)
        sql = self.get_sql(filters=filters,sorters=sorters)
        sql_text = sql["sql_text"]
        params=sql["params"]
        
        exp_log.status='query'
        exp_log= DBSession.merge(exp_log)
        DBSession.commit()
        conn = self.data_source.engine.connect()
        try:
            resultProxy=conn.execute(text(sql_text),params)
            exp_log.status='export'
            exp_log.exp_type=exp_type
            exp_log.format=format
            exp_log.query_end_time=datetime.now()
            exp_log= DBSession.merge(exp_log)
            DBSession.commit()
            file_name=self.get_export_filename()
            header=[]
            for prop in self.rpt_props:
                header.append(prop.display_name)
            file_info=exportor.export(exp_dir+'/'+file_name+'.'+format,header,resultProxy,exp_type=exp_type,format=format,zip=zip)
        finally:
            resultProxy.close()
            conn.close()
        
        exp_log.status='done'
        exp_log.file_size=file_info['file_size']
        exp_log.url=file_info['file_name'][len(exp_dir)+1:]
        exp_log.total_cnt=file_info['total_cnt']
        exp_log.format=format
        exp_log.zip=file_info['zip']
        exp_log.end_time=datetime.now()
        exp_log= DBSession.merge(exp_log)
        DBSession.commit()
        return exp_log
    
    def get_export_filename(self):
        return 'public/'+self.report.display_name+'-'+datetime.now().strftime("%Y%m%d%H%M%S")
    
    def get_data_model(self):
        """
        get data model for extjs grid
        """
        data_model=[]
        for prop in self.rpt_props:
            data_model.append(dict(name=prop.col_name.lower()))
        return data_model
        
    def get_column_model(self):
        """
        get the column model for extjs grid
        """
        column_model = []
        for prop in self.rpt_props:
            column = dict(header=prop.display_name,dataIndex=prop.col_name.lower())
            if prop.width:
                column['width']=int(prop.width)
            column_model.append(column)
        return column_model
    
    def get_filter_model(self):
        """
         get the report filter model to generate filter form
        """
        filter_model=[]
        for prop in self.rpt_props:
            if prop.is_filter:
                print(str(prop.filter_type))
                filter = dict(label=prop.display_name,name=prop.col_name.lower(),filter_type=prop.filter_type,width=prop.width,req_filter=prop.req_filter)
                filter_model.append(filter)
        return filter_model
    
    def get_filter_list(self,filter_name,filters=[]):
        """
         get the report filter selection list
        """
        DBSession=db.session
        for prop in self.rpt_props:
            if  prop.col_name.lower()==filter_name.lower() and prop.filter_type=='list' and prop.selection:
                selection = DBSession.query(Selection).filter(Selection.name==prop.selection).first()
                return selection.get_selection()
        sql = self.get_sql(selectors=[filter_name+" text",filter_name+" value"],filters=filters,groups=[filter_name],sorters=[dict(sort=filter_name,dir="asc")],distinct=True)
        sql_text = sql["sql_text"]
        params=sql["params"]
        conn = self.data_source.engine.connect()
        try:
            resultProxy = conn.execute(text(sql_text),params)
            result = resultProxy.fetchall()
            resultProxy.close()
        finally:
            conn.close()
        return result
    
    def refresh_props(self):
        DBSession=db.session
        if self.data_source.engine.dialect.name=='oracle':
            sql_text = "select * from ("+self.report.sql_query+") as a where rownum<1"
        if self.data_source.engine.dialect.name=='postgresql':
            sql_text = "select * from ("+self.report.sql_query+") as a limit 1"
        if self.data_source.engine.dialect.name=='hana':
            assert(1==2)
        conn = self.data_source.engine.connect()
        try:
            resultProxy = conn.execute(text(sql_text))
            resultProxy.close()
        finally:
            conn.close()
        seq=0
        prop_list=[]
        for col_name in resultProxy.keys():
            temp_prop=None
            seq=seq+1
            col_name = col_name.upper()
            for prop in self.rpt_props:
                if prop.col_name == col_name:
                    temp_prop=prop
                    break
            if temp_prop:
                self.rpt_props.remove(temp_prop)
            else:
                temp_prop=ReportProp(rpt_id=self.report_id,col_name=col_name)
                temp_prop.display_name = ' '.join([name.capitalize() for name in col_name.split('_')])
            temp_prop.seq=seq
            prop_list.append(temp_prop)
        for prop in self.rpt_props:
            DBSession.delete(prop)
        DBSession.flush()
        for prop in prop_list:
            DBSession.merge(prop)
        DBSession.flush()
        self.rpt_props = DBSession.query(ReportProp).filter(ReportProp.rpt_id == self.report_id).order_by(ReportProp.seq).all()
        
    def get_props(self):
        return self.rpt_props
    
    def req_filter(self):
        for prop in self.rpt_props:
            if prop.req_filter:
                return True
        return False