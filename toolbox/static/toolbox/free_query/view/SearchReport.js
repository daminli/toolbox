Ext.define('free_query.view.SearchReport', {
	extend : 'Ext.panel.Panel',
	alias : 'widget.searchreport',
	layout : {
		type : 'border'
	},
	title : 'Search Report',
	initComponent : function() {
		var me = this;

		Ext.applyIf(me, {
					items : [{
								region : 'west',
								split : true,
								id : 'NavigationPanel',
								maxWidth : 400,
								minWidth : 100,
								width : 200,
								header : false,
								xtype : 'treepanel',
								store : 'FolderTree',
								rootVisible : false
							}, {
								xtype : 'panel',
								region : 'center',
								split : true,
								stateId : 'mainnav.west',
								stateful : true,
								id : 'ContentPanel',
								title : 'Report List',
								header : true,
								layout : 'border',
								items : [{
											xtype : 'gridpanel',
											region : 'center',
											split : true,
											header : false,
											id : 'ReportGrid',
											store : 'Reports',
											columns : [{
														xtype : 'gridcolumn',
														dataIndex : 'display_name',
														text : 'Report Name',
														width : 400
													}, {
														xtype : 'datecolumn',
														dataIndex : 'creation_date',
														text : 'Modified Date',
														width : 200

													}, {
														xtype : 'gridcolumn',
														dataIndex : 'create_by',
														text : 'Owner',
														width : 200
													}]
										}, {
											xtype : 'panel',
											region : 'south',
											height : 350,
											id:'infopanel',
											layout : {
												type : 'card'
											},
											items : [
											{
														xtype : 'folderform',
														id : 'ReportFolderForm',
														bodyPadding : 10,
														title : 'Folder Info'
													},{
														xtype : 'reportform',
														id : 'ReportInfoForm',
														bodyPadding : 10,
														title : 'Report Info'
													}
											]
										}]

							}]
				});

		me.callParent(arguments);
	}
});
