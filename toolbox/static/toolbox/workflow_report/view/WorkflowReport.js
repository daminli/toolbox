Ext.define('workflow_report.view.WorkflowReport', {
			extend : 'Ext.container.Viewport',
			alias : 'widget.WorkflowReport',
			controllers : ['WorkflowReport'],
			layout : {
				type : 'vbox'
			},
			initComponent : function() {
				var me = this;
				me.application.getController(me.controllers);

				Ext.applyIf(me, {
							items : [{
								xtype : 'form',
								flex : 1,
								width : '100%',
								bodyPadding : 10,
								layout : 'hbox',
								frame : false,
								fieldDefaults : {
									labelAlign : 'left',
									labelWidth : 100,
									labelStyle : 'font-weight:bold'
								},
								dockedItems : [{
									dock : 'top',
									xtype : 'toolbar',
									items : [{
										xtype : 'datefield',
										name : 'from_date',
										fieldLabel : 'From Date',
										allowBlank : false,
										value : (Ext.Date.add(new Date(),
												Ext.Date.DAY, -10))
									}, {

										fieldLabel : 'To',
										xtype : 'datefield',
										labelWidth : 30,
										labelAlign : 'right',
										name : 'to_date',
										allowBlank : false,
										value : (new Date())
									}, {
										xtype : 'button',
										text : 'Search'
									}]
								}]
							}, {
								xtype : 'tabpanel',
								frame : false,
								activeTab : 0,
								flex : 15,
								width : '100%',
								autoHeight : true,
								autoScroll : true,
								defaults : {
									height : 700,
									width:'100%'
								},
								items : [{
											xtype : 'WorkflowOverall'
										}, {
											xtype : 'WorkflowRunTrend'
										}, {
											xtype : 'WorkflowRunDetail'
										}]
							}]
						});

				me.callParent(arguments);
			}

		});