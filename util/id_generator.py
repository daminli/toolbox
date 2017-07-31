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
                idg_model=IdGModel.query.filter(IdGModel.name==self.name).first()
                self.generator=IdG(idg_model)
        except Exception as e:
            app.logger.error(str(e))
        finally:
            lock.release(self.name)
    
    def nextval(self):
        lock.acquire(self.name)
        try:
            temp = self.generator.nextval()
        finally:
            lock.release(self.name)
        return temp
    
class IdGModel(db.Model):
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

class IdG():
    def __init__(self,idGModel):
        self._name=idGModel.name
        self._prefix=idGModel.prefix if idGModel.prefix else ""
        self._postfix=idGModel.postfix if idGModel.postfix else ""
        self._seq_len=idGModel.seq_len
        self._fill_char=idGModel.fill_char if idGModel.fill_char else "0"
        self._seq_name = idGModel.seq_name
        self._start_num = idGModel.start_num
        self._end_num = idGModel.end_num
        self._db_seq = None
        
    def id_format(self):
        if self._seq_len:
            len_prefix = len(self._prefix)
            len_postfix = len(self._postfix)
            len_current_num = len(str(self._current_num))
            fill_len = self._seq_len-len_prefix-len_postfix-len_current_num
            return self._prefix+self._fill_char*fill_len+str(self._current_num)+self._postfix
        else:
            return self._prefix+str(self._current_num)+self._postfix
        
    def nextval(self):
        if not self._db_seq:
            self._db_seq = Sequence(self._seq_name,start=self._start_num,maxvalue=self._end_num,cycle=True)
            try:
                self._current_num=db.execute(self._db_seq)
            except Exception as e:
                app.logger.debug(str(e))
                self._db_seq.create(db.engine)
                db.session.execute(self._db_seq)
                self._current_num=db.session.execute(self._db_seq)
        else:
            self._current_num=db.session.execute(self._db_seq)
        return self.id_format()
