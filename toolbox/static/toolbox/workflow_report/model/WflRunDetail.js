Ext.define('workflow_report.model.WflRunDetail', {
			extend : 'Ext.data.Model',

			fields : [{
						name : 'node_name'
					}, {
						name : 'node_type'
					}, {
						name : 'runtime'
					}, {
						name : 'start_time',
						type : 'date'
					}, {
						name : 'end_time',
						type : 'date'
					}, {
						name : 'wfl_starttime',
						type : 'date'
					}, {
						name : 'wfl_endtime',
						type : 'date'
					}, {
						name : 'node_status'
					},{
						name : 'parent_node'
					}]
		});