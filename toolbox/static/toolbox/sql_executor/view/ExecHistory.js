Ext.define('sql_executor.view.ExecHistory', {
	extend : 'Ext.container.Viewport',
	controllers : [ 'ExecHistory' ],

	initComponent : function() {
		var me = this;
		me.application.getController(me.controllers);

		Ext.applyIf(me, {
			items : [ {
				xtype : 'SearchExecHistory'
			}
			/*
			 * ,{ xtype : 'tabpanel', frame : false, activeTab : 0, id :
			 * 'ExecHistoryTabpanel', height : '100%', autoHeight : true,
			 * autoScroll : true, defaults : { height : 700 }, items : [{ xtype :
			 * 'SearchExecHistory' }] }
			 */
			]
		});
		me.callParent(arguments);
	}
});
