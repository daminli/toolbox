Ext.define('common.view.Selection', {
	extend : 'Ext.container.Viewport',
	controllers : ['Selection'],
	padding : 5,
	initComponent : function() {
		var me = this;
		me.application.getController(me.controllers);

		Ext.applyIf(me, {
			items : [{
				xtype : 'panel',
				frame : true,
				header : true,
				minHeight : 600,
				title : 'Selection',
				layout : {
					type : 'hbox',
					padding : '5',
					align : 'left'
				},
				items : [{
							xtype : 'container',
							width : 800,
							layout : {
								type : 'vbox',
								padding : '5',
								align : 'stretch'
							},
							items : [{
										xtype : 'form',
										height : 50,
										uid : 'search_form',
										bodyPadding : 10,
										layout : 'hbox',
										frame : false,
										fieldDefaults : {
											labelAlign : 'left',
											labelWidth : 50,
											labelStyle : 'font-weight:bold'
										},
										dockedItems : [{
													dock : 'top',
													xtype : 'toolbar',
													items : [{
																xtype : 'textfield',
																fieldLabel : 'Name',
																labelAlign : 'left',
																name : 'name'
															}, {
																text : 'Search'
															}]
												}]
									}, {
										xtype : 'gridpanel',
										region : 'center',
										header : false,
										minHeight : 300,
										store : 'Selection',
										frame : false,
										margins : 5,
										columns : [{
													xtype : 'gridcolumn',
													dataIndex : 'name',
													text : 'Name',
													width : 200
												}, {
													xtype : 'gridcolumn',
													dataIndex : 'type',
													text : 'Type',
													width : 100
												}, {
													xtype : 'gridcolumn',
													dataIndex : 'config',
													text : 'Detail',
													width : 300
												},{
													xtype : 'gridcolumn',
													dataIndex : 'datasource',
													text : 'DataSource',
													width : 150
												}]
									}]
						}, {
							xtype : 'form',
							title : 'Selection',
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
												url : "/common/get_data_source",
												reader : {
													type : 'json'
												}
											}
										}),
								queryMode : 'remote',
								displayField : 'name',
								valueField : 'name',
								allowBlank : true,
								emptyText : "Select a datasource"
							}, {
								fieldLabel : 'Name',
								name : 'name',
								allowBlank : false
							}, {
								fieldLabel : 'Type',
								name : 'type',
								allowBlank : false
							}, {
								xtype : 'textareafield',
								fieldLabel : 'Detail',
								name : 'config',
								allowBlank : false
							}],
							buttons : [{
										text : 'Delete',
										id : 'btnDelete'
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
