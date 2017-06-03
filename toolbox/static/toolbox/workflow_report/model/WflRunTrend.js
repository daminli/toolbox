Ext.define('workflow_report.model.WflRunTrend', {
			extend : 'Ext.data.Model',
			fields : [{
						name : 'system_name'
					}, {
						name : 'runid'
					}, {
						name : 'run_key'
					}, {
						name : 'instance'
					}, {
						name : 'workflow'
					}, {
						name : 'starttime'
					}, {
						name : 'endtime'
					}, {
						name : 'status'
					}, {
						name : 'run_day'
					}, {
						name : 'runtime'
					}, {
						name : 'gatetime'
					}, {
						name : 'over_gatetime'
					}, {
						name : 'is_break'
					}]
		});