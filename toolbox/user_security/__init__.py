
from flask import Blueprint, url_for, current_app

app=current_app

auth = app.blueprints.get('auth',None)
if not auth:
    auth=Blueprint('auth', 'user_security', template_folder='templates')
    from . import views
    app.register_blueprint(auth, url_prefix='/auth')

    

def groupfinder(userid, request):
    """
    get the user Principal list
    """
    acl = ['page:main.MainPage', 
           'page:sql_executor.ExecuteSql', 
           'page:sql_executor.ExecHistory',
           'page:free_query.ViewReport',
           'page:free_query.CreateReport',
           'page:free_query.EditReport',
           'page:workflow_report.WorkflowReport',
            'page:itsm.TicketAnalyze',
            'page:itsm.TicketUsers',
           'page:itsm.WorkLoadMgt',
           'page:itsm.CreateProject',
           'page:itsm.Dashboard',
           'page:common.DataSource',
           'page:common.Selection',
           'page:common.ModelCreator',
           'page:common.Dg',
           'page:tools.IconsGlyph',
           'page:action.DoAction']
    return acl
    
class RootFactory(object):
    """
    base on the request context set the function __acl__
    """
    @property
    def __acl__(self):
        acl=[]
        if 'page' in self.request.matchdict and 'package' in self.request.matchdict:
            page = self.request.matchdict['page']
            package = self.request.matchdict['package']
            if page in ['Login']:
                None
                #acl = [(Allow, Everyone, 'view')]
            else:
                None
                #acl = [(Allow, 'page:'+package+'.' + page, 'view')]
        return acl

    def __init__(self, request):
        self.request = request

PREFIX = '/extpage/user_security'        
        
NAV_DATA = dict(
               text='User Security',
               expanded=False,
               children=[dict(
                              text='Users',
                              target=PREFIX+'/user/',
                              type='url'
                            ), 
                         dict(
                               text='User Group',
                               target=PREFIX+'/user_group/',
                               type='url'
                            ), 
                         dict(
                               text='User Role',
                               target=PREFIX+'/user_role/',
                               type='url'
                            ), 
                         dict(
                               text='User Activity',
                               target=PREFIX+'/user_activity/',
                               type='url'
                            )]
                    )
