Ext.define('free_query.view.ReportPropPanel', {
			extend : 'Ext.panel.Panel',
			alias : 'widget.ReportPropPanel',
			report_id : '123',
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

				me.filter_type = Ext.create('common.store.SelectList');
				me.filter_type.load({
							params : {
								name : 'filter_type'
							}
						});
				me.selection = Ext.create('common.store.SelectList');
				me.selection.load({
							params : {
								name : 'selection'
							}
						});

				Ext.applyIf(me, {
							items : [{
										xtype : 'form',
										title : 'Report Query',
										id : 'report_query',
										frame : true,
										width : 800,
										layout : 'anchor',
										border : false,
										bodyPadding : 10,
										fieldDefaults : {
											labelAlign : 'top',
											labelWidth : 100,
											labelStyle : 'font-weight:bold'
										},
										defaults : {
											anchor : '90%',
											margins : '0 0 10 0'
										},
										items : [{
													xtype : 'textfield',
													fieldLabel : 'Report Id',
													name : 'id',
													hidden : true,
													hideLabel : true
												}, {
													xtype : 'textareafield',
													fieldLabel : 'Sql Query',
													name : 'sql_query',
													labelAlign : 'top',
													height : 150,
													margin : '0',
													allowBlank : false,
													msgTarget : 'under'
												}],
										buttons : [{
													text : 'Refresh Props',
													id : 'refresh_props'
												}]
									}, {
										xtype : 'gridpanel',
										id : 'ReportPropGrid',
										store : 'ReportProp',
										minHeight : 200,
										maxHeight : 400,
										frame : true,
										bodyPadding : 10,
										defaults : {
											xtype : 'gridcolumn'
										},
										columns : [{
													header : 'No.',
													dataIndex : 'seq',
													width : 50
												}, {
													header : 'Column',
													dataIndex : 'col_name',
													width : 200
												}, {
													header : 'Dispaly Name',
													dataIndex : 'display_name',
													editor : {
														xtype : 'textfield',
														allowBlank : false
													},
													width : 250
												}, {
													xtype : 'checkcolumn',
													header : 'Filter',
													disabled : true,
													dataIndex : 'is_filter',
													editor : {
														xtype : 'checkbox'
													}
												}, {
													xtype : 'checkcolumn',
													header : 'Required',
													disabled : true,
													dataIndex : 'req_filter',
													editor : {
														xtype : 'checkbox'
													}
												},{
													header : 'Filter Type',
													dataIndex : 'filter_type',
													editor : {
														xtype : 'combo',
														store : me.filter_type,
														queryMode : 'local',
														valueField : 'value'
													},
													width : 150
												},
												 {
													header : 'Selection',
													dataIndex : 'selection',
													editor : {
														xtype : 'combo',
														store : me.selection,
														queryMode : 'local',
														valueField : 'value'
													},
													width : 150
												}, {
													header : 'Width',
													dataIndex : 'width',
													editor : 'numberfield',
													width : 150
												}],
										plugins : [Ext.create(
												'Ext.grid.plugin.RowEditing', {
													clicksToEdit : 1
												})]
									}]
						});

				me.callParent(arguments);
				if (me.readOnly) {
					me.query('#datasource')[0].store.load();
				}

			}
		});
