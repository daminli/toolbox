template = []
template.append(
    dict(
       template_id='resources_mgmt.projects',
       api_name='',
       upload_props = [
           dict(title_name='Project Name',prop_name='project_name',is_required=True,title_type='text'),
           dict(title_name='Summary',prop_name='summary',is_required=True,title_type='text'),
           dict(title_name='Planning Focal',prop_name='it_focal',is_required=True,title_type='text'),
           dict(title_name='IT Leader',prop_name='it_leader',is_required=True,title_type='text'),
           dict(title_name='Total internal MD',prop_name='int_md',is_required=True,title_type='text'),
           dict(title_name='Total external Cost$',prop_name='ext_cost',is_required=True,title_type='text'),
           dict(title_name='Start Date',prop_name='start_date',is_required=True,title_type='text'),
           dict(title_name='End Date',prop_name='end_date',is_required=True,title_type='text')
           ]
    ))

template.append(
    dict(
        template_id='resources_mgmt.curveplan',
        api_name='',
        upload_props = [
            dict(title_name='Project Name',prop_name='project_name',is_required=True,title_type='text'),
            dict(title_name='Resource Name',prop_name='resource_name',is_required=True,title_type='text'),
            dict(title_name='Module Name',prop_name='module_name',is_required=True,title_type='text'),
            dict(title_name='Checker',prop_name='cheker',is_required=True,title_type='text'),
            dict(title_name='test.curve_month',prop_name='man_day',is_required=True,title_type='rule',title_prop_name='month_date'),
            ]
    ))

template.append(
    dict(
        template_id='resources_mgmt.resources',
        api_name='',
        upload_props = [
            dict(title_name='Resource Name',prop_name='resource_name',is_required=True,title_type='text'),
            dict(title_name='Module Name',prop_name='module_name',is_required=True,title_type='text'),
            dict(title_name='Team Name',prop_name='team_name',is_required=True,title_type='text'),
            dict(title_name='Resource Type',prop_name='resource_type',is_required=True,title_type='text'),
            dict(title_name='Resource Rate',prop_name='resource_rate',is_required=True,title_type='text'),
            ]
        ))

template.append(
    dict(
        template_id='resources_mgmt.actural_timesheet',
        api_name='',
        upload_props = [
            dict(title_name='Resource Name',prop_name='resource_name',is_required=True,title_type='text'),
            dict(title_name='Project Name',prop_name='project_name',is_required=True,title_type='text'),
            dict(title_name='By Week/Day',prop_name='bucket_type',is_required=True,title_type='text'),
            dict(title_name='Work Date',prop_name='work_date',is_required=True,title_type='text'),
            dict(title_name='Work Hour',prop_name='work_hour',is_required=True,title_type='text')
            ]
        ))

template.append(
    dict(
        template_id='resources_mgmt.special_workday',
        api_name='',
        upload_props = [
            dict(title_name='Date',prop_name='day_date',is_required=True,title_type='text'),
            dict(title_name='Is Working Day',prop_name='is_work',is_required=True,title_type='text')
            ]
        ))