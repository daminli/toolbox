
NAV_DATA={}
def includeme(config):
    config.add_route('systemtree', '/systemtree/')
    config.add_route('cal_define', '/cal_define/')
    config.add_route('cal_detail', '/cal_detail/')
    config.add_route('wfl_adj_list', '/wfl_adj_list')
    config.add_route('wfl_adj', '/wfl_adj/{adjname}')