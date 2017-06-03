PREFIX = '/extpage/itsm'        
        
NAV_DATA = dict(
               text='Daily Operation',
               expanded=False,
               children=[dict(
                              text='Ticekt Analyze',
                              target=PREFIX+'/TicketAnalyze/',
                              type='url'
                            ), 
                         dict(
                              text='Ticekt Users',
                              target=PREFIX+'/TicketUsers/',
                              type='url'
                            ), 
                         dict(
                               text='Create Project',
                               target=PREFIX+'/create_project/',
                               type='url'
                            ),
                         dict(
                               text='Workload Management',
                               target=PREFIX+'/WorkLoadMgt/',
                               type='url'
                            )]
                    )


NAV_DATA1 = dict(
               text='Incident Analyze',
               expanded=False,
               children=[dict(
                              text='Dashboard',
                              target=PREFIX+'/dashboard/',
                              type='url'
                            ), 
                         dict(
                              text='Reason Analyze',
                              children=[dict(
                                    text='View By Reason',
                                    target=PREFIX+'/view_by_reason/',
                                    type='url'
                                ),dict(
                                    text='Reason Adj',
                                    target=PREFIX+'/reason_adj/',
                                    type='url'
                                ), dict(
                                    text='Reason Category'  
                                ), dict(
                                    text='Hot Issue'  
                                )]
                            ), 
                         dict(
                               text='Trend Analyze',
                               target=PREFIX+'/trend_analyze/',
                               type='url'
                            ),
                         dict(
                               text='Incident Time',
                               target=PREFIX+'/trend_analyze/',
                               type='url'
                            ),  
                         dict(
                               text='User Incident',
                               target=PREFIX+'/user_incident/',
                               type='url'
                            ),
                         dict(
                               text='Monitor Incident',
                               target=PREFIX+'/monitor_incident/',
                               type='url'
                            ),
                         dict(
                               text='Personal View',
                               target=PREFIX+'/personal_view/',
                               type='url'
                            )]
                    )
