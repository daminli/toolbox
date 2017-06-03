Ext.define('workflow_report.model.WflOverall', {
			extend : 'Ext.data.Model',

			fields : [{
						name : 'team'
					}, {
						name : 'function_name'
					}, {
						name : 'system_name'
					}, {
						name : 'runid'
					},  {
						name : 'run_key'
					},{
						name : 'gatetime'
					}, {
						name : 'total_run'
					}, {
						name : 'full_success'
					}, {
						name : 'break_success'
					}, {
						name : 'overtime'
					}, {
						name : 'break'
					}, {
						name : 'failed'
					}, {
						name : 'completed'
					}, {
						name : 'canceled'
					}]
		});