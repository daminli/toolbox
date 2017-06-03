Ext.define('itsm.controller.WorkLoadMgt', {
	extend : 'Ext.app.Controller',
	models : ['Project', 'ProjectTask'],
	stores : ['Project', 'ProjectTask'],
	views : ['WorkLoadMgt'],
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
			}
		});
	}
});
