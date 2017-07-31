from flask import Blueprint, url_for, current_app

app=current_app

res_mgmt = app.blueprints.get('res_mgmt',None)
if not res_mgmt:
    res_mgmt=Blueprint('res_mgmt', 'res_mgmt', template_folder='templates')
    from . import views
    app.register_blueprint(res_mgmt, url_prefix='/res_mgmt')

PREFIX = '/extpage/res_mgmt'
NAV_DATA = dict(
               text='Resource Management',
               expanded=True,
               children=[dict(
                              text='Projects',
                              target=PREFIX+'/Projects/',
                              type='url'
                            ), 
                         dict(
                              text='Curve Plan',
                              target=PREFIX+'/CurvePlan/',
                              type='url'
                            ),
                         dict(
                              text='Time Sheet',
                              target=PREFIX+'/TimeSheet/',
                              type='url'
                            ),
                         dict(
                              text='Work Calendar',
                              target=PREFIX+'/WorkCalendar/',
                              type='url'
                            )]
                    )
    
    