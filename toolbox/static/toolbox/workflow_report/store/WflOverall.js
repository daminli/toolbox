
Ext.define('workflow_report.store.WflOverall', {
			extend : 'Ext.data.TreeStore',
			requires : ['workflow_report.model.WflOverall'],
			constructor : function(cfg) {
				var me = this;
				cfg = cfg || {};
				me.callParent([Ext.apply({
							model : 'workflow_report.model.WflOverall',
							paramsAsHash : true,
							proxy : {
								type : 'direct',
								directFn : Remote.workflow_report.wfl_overall,
								reader : {
									type : 'json'
								}
							}
						}, cfg)]);
			}
		});