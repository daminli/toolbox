Ext.define('workflow_report.view.WorkflowRunDetail', {
	extend : 'Ext.panel.Panel',
	alias : 'widget.WorkflowRunDetail',
	title : 'Run Detail',
	layout : {
		type : 'vbox'
	},
	initComponent : function() {
		var me = this;
		Ext.applyIf(me, {
			items : [{
				xtype : 'treepanel',
				rootVisible : false,
				flex : 1,
				width : '100%',
				// title : 'Workflow Overall',
				store : 'WflRunDetail',
				columns : [{
							xtype : 'treecolumn',
							dataIndex : 'node_name',
							text : 'Node Name',
							width : 400
						}, {
							dataIndex : 'node_type',
							text : 'Node Type',
							width:200
						}, {
							dataIndex : 'runtime',
							text : 'Run Time'
						}, {
							xtype : 'templatecolumn',
							text : 'Time Line',
							width : 300,
							sortable : true,
							dataIndex : 'full_success',
							align : 'center',
							tpl : Ext
									.create(
											'Ext.XTemplate',
											'<div  style="vertical-align:middle;height: 16px; width: 250px;">',
											'<div style="vertical-align:middle;margin-top:5px;height: 6px; width: {[(values.start_time-values.wfl_starttime)/(values.wfl_endtime-values.wfl_starttime)*220]}px;background-color:green; float:left;"></div>',
											'<div style="vertical-align:middle;height: 16px; width: {[(values.end_time-values.start_time)/(values.wfl_endtime-values.wfl_starttime)*220]}px;background-color:red; float:left;"></div>',
											'<div style="vertical-align:middle;margin-top:5px;height: 6px; width: {[(values.wfl_endtime-values.end_time)/(values.wfl_endtime-values.wfl_starttime)*220]}px;background-color:grey; float:left;"></div>',
											'</div>')
						},{
							xtype:'datecolumn', 
							dataIndex : 'start_time',
							text : 'Start Time',
							width:150
						}, {
							xtype:'datecolumn', 
							dataIndex : 'end_time',
							text : 'End Time',
							width:150
						},{
							dataIndex : 'node_status',
							text : 'Status'
						} ]
			}]
		});
		me.callParent(arguments);
	}
});
