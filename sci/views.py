'''
Created on 2017-6-13
@author: wuqi
'''
import json, uuid
from datetime import date,datetime,timedelta

from flask import request, url_for, redirect,render_template, current_app,g
from flask_json import json_response, as_json

app=current_app
lm = current_app.login_manager
db=g.db

@app.route('/web',methods=['GET','POST'])   
def webServer():
    print (request.method)
    if request.method =='GET':
        print ("GET REQUEST") 
        return 'helloworld' 

    elif request.method =='POST':
        print ("POST REQUEST")
        data = request.get_data()
        return 'helloworld' ,data

@app.route('/webhana',methods=['GET','POST'])
def hanna():
    if request.method =='GET':
        res=db.session.execute("SELECT MTM,GEO,DN_NUM FROM SCI.Z_MBG_ORD_KPI limit 100").fetchall()
        return json_response(data=res)
#         return 'helloworld' 
    if request.method =='POST':
        print ("GET REQUEST") 
        return 'helloworld' 
    
@app.route('/url_map', methods = ['GET'])
def url_map():
    url_list=[]
    for rule in list(app.url_map.iter_rules()):
        url_list.append(rule.__repr__())
    url_list.sort()
    return json_response(url_rules=url_list,name=request.script_root)
