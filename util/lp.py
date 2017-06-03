# coding=utf-8
'''
Created on 2013-12-5

@author: lidm1
'''

import ldap

class Ldap(object):
    """
    Ldap for lenovo domain
    """
    def __init__(self):
        None
        
    def connect(self,user_name,password):
        try:
            SERVER = "ldap://lenovo.com:389"
            DN = user_name + "@lenovo.com"
            l = ldap.initialize(SERVER)
            l.protocol_version = 3
            l.set_option(ldap.OPT_REFERRALS, 0)
            l.simple_bind_s(DN, password)
            self.ldap_obj=l
        except:
            print('ldap connetc failed')
        
    def search(self,acc_name):
        Base = "DC=lenovo,DC=com"
        Scope = ldap.SCOPE_SUBTREE
        Filter = "(&(objectClass=user)(sAMAccountName="+acc_name+"))"
        Attrs = ["name", "userPrincipalName","departmentNumber", "telephoneNumber", "department",
                   "sAMAccountName", "mail", "manager", "title",
                   "msExchExtensionAttribute6", "employeeType", "l", "c",
                   "employeeNumber", "displayName"]
         
        r = self.ldap_obj.search(Base, Scope, Filter, Attrs)
        Type,user = self.ldap_obj.result(r,60)
        Name,Attrs = user[0]
        if hasattr(Attrs, 'has_key') and Attrs.has_key('displayName'):
            return Attrs
        return None
    
    
if __name__ == '__main__':
    l=Ldap()
    l.connect('lidm1','(dx2@2xmy)')
    print l.search('yanghs1')
    pass