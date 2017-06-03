Ext.define('common.view.DataSource', {
	extend : 'Ext.container.Viewport',
	controllers : ['DataSource'],

	padding : 5,
	initComponent : function() {
		var me = this;
		me.application.getController(me.controllers);

		me.ds_type_store = Ext.create('common.store.SelectList');
		me.ds_type_store.load({
					params : {
						name : 'datasource_type'
					}
				});
				
		me.ds_group_store = Ext.create('common.store.SelectList');
		me.ds_group_store.load({
					params : {
						name : 'datasource_group'
					}
				});

		Ext.applyIf(me, {
			items : [{
						xtype : 'panel',
						frame : true,
						header : true,
						minHeight : 600,
						title : 'Data Source',
						layout : {
							type : 'hbox',
							padding : '5',
							align : 'left'
						},
						items : [{
									xtype : 'gridpanel',
									region : 'center',
									header : false,
									minHeight : 300,
									width : 800,
									id : 'DataSourceGrid',
									store : 'DataSource',
									frame : false,
									margins : 5,
									columns : [{
												xtype : 'gridcolumn',
												dataIndex : 'name',
												text : 'Name'
											}, {
												xtype : 'gridcolumn',
												dataIndex : 'user_name',
												text : 'User Name'
											}, {
												xtype : 'gridcolumn',
												dataIndex : 'db_connect',
												text : 'DB Connect',
												width : 200
											}, {
												xtype : 'gridcolumn',
												dataIndex : 'ds_type',
												text : 'Type'
											},
											 {
												xtype : 'gridcolumn',
												dataIndex : 'ds_group',
												text : 'Group'
											}, {
												xtype : 'gridcolumn',
												dataIndex : 'last_modified_by',
												text : 'Modified By'
											}, {
												xtype : 'gridcolumn',
												dataIndex : 'last_modified_date',
												text : 'Modified Time',
												width : 200
											}]
								}, {
									xtype : 'form',
									title : 'Data Source',
									id : 'datasource_form',
									frame : false,
									width : 400,
									layout : 'anchor',
									border : false,
									bodyPadding : 10,
									margins : 5,
									fieldDefaults : {
										labelAlign : 'left',
										labelWidth : 100,
										labelStyle : 'font-weight:bold'
									},
									defaults : {
										anchor : '80%',
										margins : '0 0 10 0'
									},
									defaultType : 'textfield',
									items : [{
												fieldLabel : 'Name',
												name : 'name',
												allowBlank : false
											}, {
												fieldLabel : 'User Name',
												name : 'user_name',
												allowBlank : false
											}, {
												fieldLabel : 'Password',
												name : 'password',
												inputType : 'password',
												allowBlank : false,
												emptyText : 'password'
											}, {
												fieldLabel : 'DB Connect',
												name : 'db_connect'
											}, {
												fieldLabel : 'Type',
												name : 'ds_type',
												xtype : 'combo',
												store : me.ds_type_store,
												queryMode : 'local',
												valueField : 'value'
											},{
												fieldLabel : 'Group',
												name : 'ds_group',
												xtype : 'combo',
												store : me.ds_group_store,
												queryMode : 'local',
												valueField : 'value'
											}],
									buttons : [{
												text : 'Delete',
												id : 'btnDelete'
											}, '-', {
												text : 'Test Connect',
												id : 'btnTest'
											}, '-', {
												text : 'Save',
												id : 'btnSave'
											}]
								}]
					}]
		});
		me.callParent(arguments);
	}
});
