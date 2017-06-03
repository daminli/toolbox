PREFIX = '/extpage/action'        
        
NAV_DATA = dict(
               text='PL/SQL Proxy',
               expanded=False,
               children=[
                         dict(
                              text='Do Action',
                              target=PREFIX+'/DoAction/',
                              type='url'
                            )]
                    )

def includeme(config):
    pass