from util import lock
from sqlalchemy import (DateTime,String,Column,Text,Integer,Boolean,BigInteger)
from sqlalchemy.orm import validates,relationship, backref
from sqlalchemy import text
from sqlalchemy.schema import Sequence

from flask import g,current_app
from kombu.utils import nested
from builtins import Exception
from traitlets.config.application import catch_config_error

app=current_app
db=g.db

class IdGenerator():
    """
    generate the id number for Object, data is store in database sys_id_generator
    like sales_order : SO000001
    """
    _id_generators = {}
    def __new__(cls, *args, **kwargs):
        """
        make sure for one generator name just have on instance
        """
        name=args[0]
        if name not in cls._id_generators:
            orig = super(IdGenerator,cls)
            cls._id_generators[name] = orig.__new__(cls)
        return cls._id_generators[name]
        
    def __init__(self,name):
        self.name=name
        lock.acquire(self.name)
        try:
            if not getattr(self,'generator',None):
                self.generator=IdG.query.filter(IdG.name==self.name).first()
        except Exception as e:
            app.logger.error(str(e))
        finally:
            lock.release(self.name)
        
    def currval(self):
        return self.generator.currval()
    
    def nextval(self):
        lock.acquire(self.name)
        try:
            temp = self.generator.nextval()
            with db.session.begin_nested():
                db.session.merge(self.generator)
            app.logger.debug(self.name+'->curr_id:'+temp)
            #app.logger.debug(self.name+'->db_curr:'+IdG.query.filter(IdG.name==self.name).first().currval())
        finally:
            lock.release(self.name)
        return temp
    
class IdG(db.Model):
    __tablename__ = 'sys_id_generator'
    name = Column('name',String(32),primary_key=True)
    display_name = Column('display_name',String(64))
    start_num = Column('start_num',BigInteger)
    end_num = Column('end_num',BigInteger)
    seq_name = Column('seq_name',String(30),nullable=False)
    prefix = Column('prefix',String(30))
    postfix = Column('postfix',String(30))
    seq_len = Column('seq_len',Integer,nullable=False)
    fill_char = Column('fill_char',String(1))
    _db_seq=None
    
    def id_format(self):
        prefix=self.prefix if self.prefix else ""
        postfix=self.postfix if self.postfix else ""
        if self.seq_len:
            fill_char=self.fill_char if self.fill_char else "0"
            len_prefix = len(self.prefix) if self.prefix else 0
            len_postfix = len(self.postfix) if self.postfix else 0
            len_current_num = len(str(self.current_num)) if self.current_num else 0
            fill_len = self.seq_len-len_prefix-len_postfix-len_current_num
            return prefix+fill_char*fill_len+str(self.current_num)+postfix
        else:
            return prefix+str(self.current_num)+self.postfix
        
    def fill_seq(self,fill_char="0",prefix="",postfix="",curremt_num=0):
        fill_len = self.seq_len-len(self.prefix)-len(self.postfix)-len(self.current_num)
        return self.prefix+self.current_num+self.postfix
        
        
    def nextval(self):
        if not self._db_seq:
            self._db_seq = Sequence(self.seq_name,start=self.start_num,maxvalue=self.end_num,cycle=True)
            try:
                self.current_num=db.execute(self._db_seq)
            except Exception as e:
                app.logger.debug(str(e))
                self._db_seq.create(db.engine)
                db.session.execute(self._db_seq)
                self.current_num=db.session.execute(self._db_seq)
        else:
            self.current_num=db.session.execute(self._db_seq)
        return self.id_format()
