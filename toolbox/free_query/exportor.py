# coding=utf-8
'''
Created on 2013-6-4

@author: lidm1
'''

import csv,os,zipfile
from os.path import getsize
import codecs, cStringIO
from sqlalchemy.engine.result import RowProxy,ResultProxy
from .. import free_query
import cfg

def export(file_name,header,dataset,exp_type='direct',format='csv',zip='auto'):
    '''
        type: ['direct','achived']
                 direct : export to temp folder after export deleted
                 achived: export to server will keep to expired
        format:['csv', 'xls']
        zip: ['auto','yes','no']
               auto: if file is > 5M will zip auto, if file < 5M will not zip
               yes: zip always
               no: doesn't zip
    '''
    (dir_name, file_export) = os.path.split(file_name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name) 
    with open(file_name, 'wb') as file:
        file.write(codecs.BOM_UTF8)
        writer = UnicodeWriter(file,encoding="utf-8")
        writer.writerow(header)
        total_cnt=0
        if isinstance(dataset,ResultProxy):
            while not dataset.closed:
                result = dataset.fetchmany(10000)
                for row in result:
                    total_cnt+=1
                    if isinstance(row,RowProxy):
                        writer.writerow(list(row))
                    else:
                        writer.writerow(row)
        else:
            for row in dataset:
                total_cnt+=1
                if isinstance(row,RowProxy):
                    writer.writerow(list(row))
                else:
                    writer.writerow(row)
    file_size=getsize(file_name)
    zip_size=cfg.config.registry.settings.get('free_query.auto_zip_size',5)
    if file_size>zip_size*1024*1024:
        zip_filename=os.path.splitext(file_name)[0]+'.zip'
        with zipfile.ZipFile(zip_filename,'w') as z:
            print(file_name)
            z.write(file_name,file_export,zipfile.ZIP_DEFLATED)
            os.remove(file_name)
            file_name=zip_filename
    return dict(file_name=file_name,file_size=file_size,zip=zip,total_cnt=total_cnt)

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
        self.encoding = encoding

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode(self.encoding)

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
        self.encoding = encoding

    def next(self):
        row = self.reader.next()
        return [unicode(s, self.encoding) for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
        self.encoding = encoding

    def writerow(self, row):
        line = []
        for s in row:
            try:
                line.append(s.encode(self.encoding))
            except:
                line.append(s)
        self.writer.writerow(line)
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode(self.encoding)
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)