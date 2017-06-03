
Ext.define('workflow_report.store.WflRunTrend', {
			extend : 'Ext.data.Store',
			requires : ['workflow_report.model.WflRunTrend'],
			constructor : function(cfg) {
				var me = this;
				cfg = cfg || {};
				me.callParent([Ext.apply({
							model : 'workflow_report.model.WflRunTrend',
							paramsAsHash : true,
							proxy : {
								type : 'direct',
								directFn : Remote.workflow_report.run_trend,
								reader : {
									type : 'json'
								}
							}
						}, cfg)]);
			}
		});