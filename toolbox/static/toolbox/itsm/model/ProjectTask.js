Ext.define('itsm.model.Project', {
			extend : 'Ext.data.Model',

			fields : [{
						name : 'id'
					}, {
						name : 'assign_group'
					}, {
						name : 'assignee'
					}, {
						name : 'man_day'
					}, {
						name : 'start_time',
						type : 'date'
					}, {
						name : 'end_time',
						type : 'date'
					}, {
						name : 'comments'
					}, {
						name : 'creation_date',
						type : 'date'
					}, {
						name : 'create_by'
					}]
		});