# coding=utf-8
'''
Created on 2013-5-19

@author: lidm1
'''

class NoneReportId(Exception):
    """
    Miss report id
    """
    def __init__(self, error):
        Exception.__init__(self, '%s' % (error))
    def __str__(self):
        return repr(self.value)
        
class MissReqFilter(Exception):
    """
    Miss Required Filter
    """
    def __init__(self, error):
        Exception.__init__(self, ' miss required filter %s' % (error))
        self.error=error
    def __str__(self):
        return repr(self.error)
