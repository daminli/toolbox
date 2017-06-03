
Ext.define('workflow_report.store.WflRunDetail', {
			extend : 'Ext.data.TreeStore',
			requires : ['workflow_report.model.WflRunDetail'],
			constructor : function(cfg) {
				var me = this;
				cfg = cfg || {};
				me.callParent([Ext.apply({
							model : 'workflow_report.model.WflRunDetail',
							autoLoad: false,
							paramsAsHash : true,
							proxy : {
								type : 'direct',
								directFn : Remote.workflow_report.run_detail,
								reader : {
									type : 'json'
								}
							}
						}, cfg)]);
			}
		});