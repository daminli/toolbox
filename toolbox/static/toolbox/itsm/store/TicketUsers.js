Ext.define('itsm.store.TicketUsers', {
			extend : 'Ext.data.Store',
			requires : ['itsm.model.TicketUsers'],

			constructor : function(cfg) {
				var me = this;
				cfg = cfg || {};
				me.callParent([Ext.apply({
							model : 'itsm.model.TicketUsers',
							paramsAsHash : true,
							proxy : {
								type : 'direct',
								api : {
									read : Remote.itsm.get_ticket_users,
									create : Remote.itsm.save_ticket_users, // 1个参数
									update : Remote.itsm.save_ticket_users,// 2个参数
									destroy : Remote.itsm.save_ticket_users
								},
								reader : {
									type : 'json'
								}
							}
						}, cfg)]);
			}
		});