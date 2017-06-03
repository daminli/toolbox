Ext.define('workflow_report.model.WflNodeTrend', {
			extend : 'Ext.data.Model',
			fields : [{
						name : 'system_name'
					}, {
						name : 'runid'
					}, {
						name : 'run_key'
					}, {
						name : 'root_instance'
					}, {
						name : 'instance_id'
					}, {
						name : 'template'
					}, {
						name : 'start_time'
					}, {
						name : 'end_time'
					}, {
						name : 'status'
					}, {
						name : 'run_day'
					}, {
						name : 'runtime'
					}, {
						name : 'node_name'
					}, {
						name : 'node_type'
					}, {
						name : 'workflow_path'
					}, {
						name : 'parent_node'
					}]
		});