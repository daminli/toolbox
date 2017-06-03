Ext.define('workflow_report.view.WorkflowOverall', {
	extend : 'Ext.panel.Panel',
	alias : 'widget.WorkflowOverall',
	title : 'Overall',
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
				//title : 'Workflow Overall',
				store : 'WflOverall',
				columns : [{
							xtype : 'treecolumn',
							dataIndex : 'runid',
							text : 'Run Id',
							width : 400
						}, {
							dataIndex : 'gatetime',
							text : 'Gatetime'
						}, {
							dataIndex : 'total_run',
							text : 'Total Run'
						}, {
							xtype : 'templatecolumn',
							text : 'Success Ratio',
							width : 250,
							sortable : true,
							dataIndex : 'full_success',
							align : 'center',
							tpl : Ext
									.create(
											'Ext.XTemplate',
											'<div  style="height: 20px; width: 250px;">',
											'<div style="height: 20px; width: {[values.full_success/values.total_run*220]}px;background-color:green; float:left;"></div>',
											'<div style="height: 20px; width: {[(values.total_run-values.full_success)/values.total_run*220]}px;;background-color:red;float:left;"></div></div>')
						}, {
							xtype : 'templatecolumn',
							dataIndex : 'full_success',
							text : 'Full Success',
							align : 'center',
							tpl : Ext
									.create(
											'Ext.XTemplate',
											'{[values.full_success?Math.round(values.full_success/values.total_run*100)+"%":null]}')
						}, {
							xtype : 'templatecolumn',
							dataIndex : 'break_success',
							text : 'Break Success',
							align : 'center',
							width : 120,
							tpl : Ext
									.create(
											'Ext.XTemplate',
											'{[values.full_success?Math.round(values.full_success/values.total_run*100)+"%":null]}')
						}, {
							dataIndex : 'overtime',
							text : 'Overtime'
						}, {
							dataIndex : 'break',
							text : 'Breaked'
						}, {
							dataIndex : 'completed',
							text : 'Completed'
						}, {
							dataIndex : 'failed',
							text : 'Failed'
						}]
			}]
		});
		me.callParent(arguments);
	}
});
