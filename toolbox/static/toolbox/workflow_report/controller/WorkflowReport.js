Ext.define('workflow_report.controller.WorkflowReport', {
	extend : 'Ext.app.Controller',
	models : ['WflOverall', 'WflRunTrend', 'WflRunDetail', 'WflNodeTrend'],
	stores : ['WflOverall', 'WflRunTrend', 'WflRunDetail', 'WflNodeTrend'],
	views : ['WorkflowOverall', 'WorkflowRunTrend', 'WorkflowRunDetail',
			'WorkflowNodeTrend'],
	onLaunch : function() {
		// this.getStore("WflOverall").load({});
		this.params = {};
	},
	init : function(application) {
		this.control({
			"WorkflowOverall treepanel" : {
				itemdblclick : function(panel, record, item, index, e, eOpts) {
					me = this;

					wflTabs = Ext.ComponentQuery
							.query("WorkflowReport tabpanel")[0];
					var tab = wflTabs.down('WorkflowRunTrend');
					wflTabs.setActiveTab(tab);
					data = Ext.ComponentQuery.query('WorkflowReport form')[0].form
							.getValues();
					this.params.from_date = data.from_date;
					this.params.to_date = data.to_date;
					this.params.runid = record.data;
					this.getStore("WflRunTrend").load({
								params : this.params
							});
				}
			},
			"WorkflowReport form button[text='Search']" : {
				click : function(btn) {
					data = btn.up().up().form.getValues();
					this.getStore("WflOverall").load({
								params : data
							});
					this.params.from_date = data.from_date;
					this.params.to_date = data.to_date;
				}
			},
			"WorkflowRunTrend gridpanel" : {
				itemdblclick : function(panel, record, item, index, e, eOpts) {
					me = this;

					wflTabs = Ext.ComponentQuery
							.query("WorkflowReport tabpanel")[0];
					var tab = wflTabs.down('WorkflowRunDetail');
					wflTabs.setActiveTab(tab);
					this.params.run_instance = record.data;
					this.getStore("WflRunDetail").load({
								params : this.params
							});
				}
			},
			"WorkflowRunDetail treepanel" : {
				itemdblclick : function(panel, record, item, index, e, eOpts) {
					me = this;
					this.params.run_node = record.data;
					data = Ext.ComponentQuery.query('WorkflowReport form')[0].form
							.getValues();
					this.params.from_date = data.from_date;
					this.params.to_date = data.to_date;

					Ext.create("workflow_report.view.WorkflowNodeTrend", {
								title : this.params.run_node.node_name,
								closable : true,
								maximizable : true,
								autoScroll : true,
								frame : true,
								scripts : true,
								parent : me,
								width:800,
								height:400
							}).show();
					this.getStore("WflNodeTrend").load({
								params : this.params
							});
				}
			}
			,
		});
	}
});
