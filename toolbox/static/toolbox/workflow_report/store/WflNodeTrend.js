
Ext.define('workflow_report.store.WflNodeTrend', {
			extend : 'Ext.data.Store',
			requires : ['workflow_report.model.WflNodeTrend'],
			constructor : function(cfg) {
				var me = this;
				cfg = cfg || {};
				me.callParent([Ext.apply({
							model : 'workflow_report.model.WflNodeTrend',
							paramsAsHash : true,
							proxy : {
								type : 'direct',
								directFn : Remote.workflow_report.node_trend,
								reader : {
									type : 'json'
								}
							}
						}, cfg)]);
			}
		});