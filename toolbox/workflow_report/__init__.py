PREFIX = '/extpage/workflow_report'        
        
NAV_DATA = dict(
               text='Workflow Report',
               expanded=False,
               children=[dict(
                              text=' Dashbord',
                              target=PREFIX+'/WorkflowDashbord/',
                              type='url'
                            ), 
                         dict(
                              text='Reports',
                              target=PREFIX+'/WorkflowReport/',
                              type='url'
                            )]
                    )