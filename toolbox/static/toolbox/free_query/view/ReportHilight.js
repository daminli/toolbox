Ext.define('free_query.view.ReportHilight', {
	extend : 'Ext.window.Window',
	alias : 'widget.ReportHilight',
	initComponent : function() {
		var me = this;

		Ext.applyIf(me, {
			title : 'Report Hight',
			height : 400,
			width : 800,
			layout : 'fit',
			items : []
		});

		me.callParent(arguments);
	}
});
