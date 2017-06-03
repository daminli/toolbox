

Ext.define('free_query.view.ReportInfoPanel', {
	extend : 'Ext.panel.Panel',
	alias : 'widget.ReportInfoPanel',
	layout : {
		type : 'vbox',
		padding : '5',
		align : 'stretch'
	},
	defaults : {
		margins : '0 0 5 0'
	},
	initComponent : function() {
		var me = this;

		var treeStore = Ext.create('free_query.store.FolderTree', {
					proxy : {
						type : 'ajax',
						url : '/free_query/report_folder?root_id=1',
						reader : {
							type : 'json'
						}
					}
				});
		// treeStore.load()

		Ext.applyIf(me, {
			items : [{
						xtype : 'form',
						title : 'Report Info',
						id : 'reportInfo_form',
						frame : true,
						width : 800,
						layout : 'anchor',
						border : false,
						bodyPadding : 10,
						fieldDefaults : {
							labelAlign : 'left',
							labelWidth : 100,
							labelStyle : 'font-weight:bold'
						},
						defaults : {
							anchor : '70%',
							margins : '0 0 10 0'
						},
						items : [{
									xtype : 'textfield',
									fieldLabel : 'Report Id',
									name : 'id',
									hidden : true,
									hideLabel : true
								}, {
									xtype : 'textfield',
									fieldLabel : 'Unique Name',
									name : 'name',
									allowBlank : false
								}, {
									xtype : 'textfield',
									fieldLabel : 'Display Name',
									name : 'display_name'
								}, {
									xtype : 'combo',
									fieldLabel : 'DataSource',
									width : 200,
									id : 'datasource',
									name : 'datasource',
									editable : false,
									store : Ext.create('Ext.data.Store', {
												fields : [{
															type : 'string',
															name : 'name'
														}],
												proxy : {
													type : 'ajax',
													url : "/common/get_data_source?ds_group=normal",
													reader : {
														type : 'json'
													}
												}
											}),
									queryMode : 'remote',
									displayField : 'name',
									valueField : 'name',
									allowBlank : false,
									emptyText : "Select a datasource"
								}, {
									xtype : 'treepicker',
									fieldLabel : 'Folder',
									id : 'folder_id',
									name : 'folder_id',
									displayField : 'text',
									store : treeStore,
									allowBlank : false,
									autoScroll:true
								}, {
									xtype : 'textareafield',
									grow : true,
									growMin : 100,
									growMax : 500,
									fieldLabel : 'Description',
									name : 'rpt_desc',
									allowBlank : false
								}, {
									xtype : 'textareafield',
									grow : true,
									growMin : 200,
									growMax : 250,
									fieldLabel : 'Sql Query',
									name : 'sql_query',
									allowBlank : false
								}],
						buttons : [{
									text : 'Next',
									id : 'next'
								}]
					}]
		});

		me.callParent(arguments);
	}
});
