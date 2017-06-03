# coding=utf-8
'''
Created on 2013-6-13  @author: lidm1
'''
import unittest

from pyramid import testing
import webtest

base_url='http://localhost:6543'

class Test(unittest.TestCase):
    
    _initial_flag=False


    def setUp(self):
        if not Test._initial_flag:
            from toolbox import main
            Test.testapp = webtest.TestApp('config:D:\\mydoc\\Workspace\\python_workspace\\toolbox\\development.ini#main')
            self.testapp = Test.testapp
            Test._initial_flag=True
        else:
            self.testapp = Test.testapp
            
        params=dict(userName='lidm1',password='lidm1')
        self.testapp.get(base_url+'/user_security/valid_login',params)


    def tearDown(self):
        testing.tearDown()
        pass


    def test_data_source(self):
        params=dict(name='ABPPOP4',user_name='ABPPOP4',password='ABPPOP4',tns_name='i2_uatmdm')
        res = self.testapp.get(base_url+'/sql_executor/test_data_source',params)
        print(res.body)
        self.failUnless('true' in res.body)
        pass
    
    def test_create_data_source(self):
        params=dict(name='ABPPOP4',user_name='ABPPOP4',password='ABPPOP4',db_connect='i2_uatmdm')
        res = self.testapp.get(base_url+'/sql_executor/test_data_source',params)
        print(res.body)
        self.failUnless('true' in res.body)
        
    def test_new_request(self):
        params=dict(summary='This is test for a new user execurte sql request')
        res = self.testapp.get(base_url+'/sql_executor/new_request',params)
        print(res.body)
        self.failUnless('new user execurte ' in res.body)
        
    def test_run_script(self):
        params=dict(scripts='''
        select * from user_role;
        insert into USER_ROLE values ('role1','role name 1');
        insert into USER_ROLE values ('role2','role name 2');
        insert into USER_ROLE values ('role3','role name 3');
        update USER_ROLE set name = 'role name 3 update'
        where id = 'role3';
        --this is a delete sql
        delete from user_role where id like 'role%';
        update USER_ROLE set name = 'role name 3 update'
        where id = 'role3';
        commit;
        ''', exec_id = 'EXEC-0000000042')
        res = self.testapp.get(base_url+'/sql_executor/run_script',params)
        print(res.body)
        #self.failUnless('new user execurte ' in res.body)
        
    def test_run_script_block(self):
        params=[]
        res = self.testapp.get(base_url+'/sql_executor/run_script_block',params)
        print(res.body)


if __name__ == "__main__":
    import sys;
    sys.argv = ['','Test.test_run_script']
    unittest.main()