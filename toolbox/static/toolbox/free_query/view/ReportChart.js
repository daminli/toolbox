Ext.define('free_query.view.ReportChart', {
	extend : 'Ext.window.Window',
	alias : 'widget.ReportChart',
	initComponent : function() {
		var me = this;

		Ext.applyIf(me, {
			title : 'Report Chart',
			height : 400,
			width : 800,
			layout : 'fit',
			items : []
		});

		me.callParent(arguments);
	}
});
