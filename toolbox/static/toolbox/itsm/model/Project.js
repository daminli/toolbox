Ext.define('itsm.model.Project', {
			extend : 'Ext.data.Model',
			fields : [{
						name : 'id'
					}, {
						name : 'category'
					}, {
						name : 'summary'
					}, {
						name : 'status'
					}, {
						name : 'assign_group'
					}, {
						name : 'assignee'
					}, {
						name : 'driven_type'
					}, {
						name : 'submit_date',
						type : 'date'
					}, {
						name : 'mtp_date',
						type : 'date'
					}, {
						name : 'owm_attend'
					}, {
						name : 'creation_date',
						type : 'date'
					}, {
						name : 'create_by'
					}]
		});