# coding = utf8

from sqlalchemy import *
from sqlalchemy.orm import validates,relationship, backref

from cfg import *

Base.query=DBSession.query_property()

class SystemList(Base):
    __tablename__ = 'tm_module_list'
    groupName = Column('group_name',String(100))
    systemName = Column('module_name',String(100),primary_key=True)
    status = Column('sys_ent_state',String(10))
    children = relationship("WflAdjustment", backref="SystemList")

    def __repr__(self):
        return 'group : %r; system : %r' % (self.groupName,self.systemName)
    
    
class ScheduleCalDefine(Base):
    __tablename__ = 'wfl_schedule_caldefine'
    systemName = Column('system_name',String(64),primary_key=True)
    runid = Column('runid',String(64),primary_key=True)
    timeCode = Column('time_code',String(10),primary_key=True)
    workflow = Column('workflow',String(64))
    configid = Column('configid',String(64))
    cycleType = Column('cycle_type',String(64))
    cycleNumber = Column('cycle_number',String(64),primary_key=True)
    service = Column('service',String(64))
    status = Column('status',String(10))
    
    def __repr__(self):
        return 'runid : %r; timecode : %r' % (self.runid,self.timeCode)
    
class ScheduleCalDetail(Base):
    __tablename__ = 'tm_all_tsui_caldetail'
    systemName = Column('system_name',String(64),primary_key=True)
    runid = Column('runid',String(64),primary_key=True)
    startTime = Column('starttime',DateTime,primary_key=True)
    startDate = Column('startdate',Date)
    workflow = Column('workflow',String(64))
    configid = Column('configid',String(64))
    service = Column('service',String(64))
    createBy = Column('create_by',String(64))
    runBy = Column('run_by',String(64))
    status = Column('status',String(64))
    
    def __repr__(self):
        return 'runid : %r; startTime : %r' % (self.runid,self.startTime)
    
class WflAdjustment(Base):
    __tablename__ = 'wfl_adj_log'
    systemName = Column('system_name',String(100),ForeignKey('tm_module_list.module_name'))
    adjBatchName = Column('adj_batch_name',String(100),primary_key=True)
    runId = Column('runid',String(64),primary_key=True)
    configId =  Column('configid',String(64),primary_key=True)
    startTime =  Column('starttime',DateTime,primary_key=True)
    action = Column('action',String(100))

    def __repr__(self):
        return 'adjBatchName: %r, system : %r, runId : %r, startTime: %r, action: %r' % (self.adjBatchName,self.systemName,self.runId,self.startTime,self.action)


class Outages(Base):
    __tablename__='outages'
    Name = Column(String(100),primary_key=True)
    Type = Column(String(10)) #Planed, Emergency
    Reason = Column(String(300))
    Impact = Column(String(300))
    StartTime = Column(DateTime)
    EndtTime = Column(DateTime)
    Notification = Column(Text) # Portal notification html information
    Status = Column(String(20)) # Draft, Prepare, Inprocess, Closed 
    
class OutagesScope(Base):
    __tablename__='outage_scope'
    outageName= Column(String(100),primary_key=True)
    systemName= Column(String(100),primary_key=True)
    

    
    