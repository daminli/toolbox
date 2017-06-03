Ext.define('itsm.store.SearchResult', {
			extend : 'Ext.data.DirectStore',
			requires : ['itsm.model.SearchResult'],

			constructor : function(cfg) {
				var me = this;
				cfg = cfg || {};
				me.callParent([Ext.apply({
							model : 'itsm.model.SearchResult',
							paramsAsHash : true,
							proxy : {
								type : 'direct',
								// directFn: Remote.itsm.get_ticket_analyze,
								api : {
									read : Remote.itsm.get_ticket_analyze,
									create : Remote.itsm.save_ticket_analyze, // 1个参数
									update : Remote.itsm.save_ticket_analyze,// 2个参数
									destroy : Remote.itsm.save_ticket_analyze
								},
								reader : {
									type : 'json'
								}
							}
						}, cfg)]);
			}
		});