import os
from flask import Flask, request, redirect, url_for,current_app
from werkzeug import secure_filename
from util import common
from flask_json import json_response
from openpyxl import load_workbook
import shutil


app=current_app

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
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],'inprocess', filename))
            template=request.values.get('template')
            data = readXlsxData(os.path.join(app.config['UPLOAD_FOLDER'],'inprocess', filename))
            shutil.move(os.path.join(app.config['UPLOAD_FOLDER'],'inprocess', filename),os.path.join(app.config['UPLOAD_FOLDER'],'archive', filename))
            return json_response(success=True,file=filename,data=data)
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
def doDataUpload(filename):
    return None

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