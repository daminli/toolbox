PREFIX = '/extpage/free_query'        
        
NAV_DATA = dict(
               text='Free Query',
               expanded=False,
               children=[dict(
                              text='View Report',
                              target=PREFIX+'/ViewReport/',
                              type='url'
                            ), 
                         dict(
                              text='Create Report',
                              target=PREFIX+'/CreateReport/',
                              type='url'
                            )]
                    )

def includeme(config):
    config.add_route('report_folder', '/report_folder')
    config.add_route('get_folder', '/get_folder')
    config.add_route('save_folder', '/save_folder')
    config.add_route('delete_folder', '/delete_folder')
    config.add_route('search_report', '/search_report')
    config.add_route('delete_report', '/delete_report')
    config.add_route('report_info', '/report_info')
    config.add_route('show_report', '/show_report')
    config.add_route('report_data', '/report_data')
    config.add_route('report_filter','/report_filter')
    config.add_route('filter_list','/filter_list')
    config.add_route('export_report','/export_report')
    config.add_route('download_report','/download_report/{url:.*}')
    
    config.add_route('save_report','/save_report')
    config.add_route('refresh_report_props','/refresh_report_props')
    config.add_route('get_report_props','/get_report_props')
    config.add_route('save_report_props','/save_report_props')