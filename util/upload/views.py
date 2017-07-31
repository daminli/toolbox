import os
from flask import Flask, request, redirect, url_for,current_app
from werkzeug import secure_filename
from util import common
from flask_json import json_response
from openpyxl import load_workbook
import shutil
from .models import UploadTemplate,UploadProps,init_upload_tempate

from util.id_generator import IdGenerator
from . import test,upload_template
from celery.bin.celery import result

app=current_app

@common.route('/init_template', methods=['GET', 'POST'])
def init_template():
    temp=init_upload_tempate(upload_template.template)
    return json_response(template=temp)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
           
def isXlsxfile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ['xlsx']

@common.route('/data_upload', methods=['GET', 'POST'])
def data_upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and isXlsxfile(file.filename):
            template=request.values.get('template')
            try:
                data_upload = DataUpload(template,request.values)
                result=data_upload.do_upload(file)
            except Exception as e:
                raise e
                return json_response(success=False,message=str(e))
            return json_response(success=True,file=file.filename,data=result.get('data',None),titles=result.get('titles',None))
        else:
            if not isXlsxfile(file.filename):
                return json_response(success=False,message='only *.xlsx is supported' )
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
class DataUpload():
    def __init__(self,template,params):
        self.template=UploadTemplate.query.filter(UploadTemplate.template_id==template).first()
        if not self.template:
            raise UndefinedTemplate(template)
        upload_props=UploadProps.query.filter(UploadProps.template_id==template).order_by(UploadProps.seq_id).all()
        if not upload_props:
            raise NoUploadProps(template)
        else:
            self.upload_props=self.get_props(upload_props)
        self.params=params
            
    def do_upload(self,file):
        self.upload_id=IdGenerator('UPLOAD_ID').nextval()
        self.filename=self.upload_id+'.xlsx';
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],'inprocess', self.filename))
        data = readXlsxData(os.path.join(app.config['UPLOAD_FOLDER'],'inprocess', self.filename))
        data_start_line=self.template.start_line+(1 if self.template.has_title else 0)
        if len(data)<data_start_line:
            raise BlankDataFile(file.filename)
        else:
            #get title index
            if self.template.has_title:
                header=data[self.template.start_line-1]
                miss_props=[]
                for prop in self.upload_props:
                    try:
                        prop.index=header.index(prop.title_name)
                    except Exception as e:
                        if prop.is_required:
                            miss_props.append(prop.title_name)
                if miss_props:
                    raise MissProps(miss_props)
        # data convert from list to props
        ds=[]
        i=0
        for row in data[data_start_line-1:]:
            temp_row={}
            temp_row['__linenum__']=data_start_line+i
            i=i+1
            for prop in self.upload_props:
                temp_row[prop.prop_name]=row[prop.index]
            ds.append(temp_row)
        final_res={}
        if self.template.api_before:
            result=None
            exec('result='+self.template.api_before+'(template=self.template.template_id,data=ds)')
            final_res['api_before']=result
        if self.template.api_mode=='row':
            res_data=[]
            for row in ds:
                temp={}
                exec('result1='+self.template.api_name+'(template=self.template.template_id,data=row)')
                res_data.append(locals()['result1'])
            final_res['data']=res_data
        elif self.template.api_mode=='batch':
            result=None
            exec('result='+self.template.api_name+'(template=self.template.template_id,data=ds)')
            final_res['data']=result
        if self.template.api_after:
            result=None
            exec('result='+self.template.api_after)
            final_res['api_after']=result
        shutil.move(os.path.join(app.config['UPLOAD_FOLDER'],'inprocess', self.filename),os.path.join(app.config['UPLOAD_FOLDER'],'archive', self.filename))
        final_res['titles']=self.upload_props
        return final_res
    
    def get_props(self,upload_props):
        template=[]
        for prop in upload_props:
            if prop.title_type=='text':
                temp_prop=PropObject()
                temp_prop.title_name=prop.title_name
                temp_prop.prop_name=prop.prop_name
                temp_prop.is_required=prop.is_required
                temp_prop.title_prop_name=None
                template.append(temp_prop)
            elif prop.title_type=='rule':
                rule_props=None
                exec('rule_props='+prop.title_name+'(self.params)')
                for temp in rule_props:
                    temp_prop=PropObject()
                    temp_prop.title_name=temp.title_name
                    temp_prop.prop_name=prop.prop_name
                    temp_prop.is_required=prop.is_required
                    temp_prop.title_prop_name=prop.title_prop_name
                    template.append(temp_prop)
        return template
    
    def get_template_titles(self):
        template=[]
        for prop in self.upload_props:
            template.append(prop.title_name)
        return template

class PropObject():
    def __json__(self):
        temp={}
        for attrname in dir(self):
            if not attrname.startswith('__'):
                temp[attrname]=getattr(self,attrname)
        return temp

def readXlsxData(filename):
    wb = load_workbook(filename = filename)
    ws = wb.worksheets[0]
    data=[]
    for row in ws.rows:
        temp=[]
        for cell in row:
            temp.append(cell.value)
        data.append(temp)
    return data      

@common.route('/file_upload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return json_response(success=True,file=filename,template=request.values.get('template'))
        
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
      
class UndefinedTemplate(Exception):
    """
    No template defined
    """
    def __init__(self, error):
        self.error="Undefined upload template %s" % (error)
    def __str__(self):
        return repr(self.error)
    
class NoUploadProps(Exception):
    """
    no upload props defined
    """
    def __init__(self, error):
        self.error='No upload properties defined for %s' % (error)
    def __str__(self):
        return repr(self.error)
    
class BlankDataFile(Exception):
    """
    blank data file
    """
    def __init__(self, error):
        self.error='Your data file:  %s is empty' % (error)
    def __str__(self):
        return repr(self.error)

class MissProps(Exception):
    """
    blank data file
    """
    def __init__(self, error):
        self.error='Check your upload files miss titles: %s' % (error)
    def __str__(self):
        return repr(self.error)
    
class UploadException(Exception):
    """
    common upload exception
    """
    def __init__(self, error):
        self.error=error
    def __str__(self):
        return repr(self.error)