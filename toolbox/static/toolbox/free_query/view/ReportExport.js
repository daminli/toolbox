Ext.define('free_query.view.ReportExport', {
	extend : 'Ext.window.Window',
	alias : 'widget.ReportExport',
	initComponent : function() {
		var me = this;

		Ext.applyIf(me, {
			title : 'Report Export',
			height : 400,
			width : 800,
			layout : 'fit',
			items : []
		});

		me.callParent(arguments);
	}
});
