Ext.define('itsm.view.TicketUsers', {
	extend : 'Ext.container.Viewport',
	controllers : ['TicketUsers'],
	padding : 5,
	initComponent : function() {
		var me = this;
		me.application.getController(me.controllers);

		me.sub_biz = Ext.create('common.store.SelectList');
		me.sub_biz.load({
					params : {
						name : 'sub_biz'
					}
				});
		me.function_group = Ext.create('common.store.SelectList');
		me.function_group.load({
					params : {
						name : 'function_group'
					}
				});

		Ext.applyIf(me, {
			layout : {
				type : 'anchor',
				padding : '5',
				align : 'left'
			},
			items : [{
				xtype : 'panel',
				frame : true,
				header : true,
				anchor : '100% 100%',
				title : 'Ticket Analyze',
				layout : {
					type : 'anchor',
					padding : '5',
					align : 'left'
				},
				items : [{
							xtype : 'form',
							bodyPadding : 10,
							anchor : '100% 8%',
							layout : 'hbox',
							uid : 'search_form',
							frame : true,
							dockedItems : [{
										dock : 'top',
										xtype : 'toolbar',
										items : [{
													fieldLabel : 'Itcode',
													xtype : 'textfield',
													labelAlign : 'right',
													name : 'itcode'
												}, {
													fieldLabel : 'Internal Email',
													xtype : 'textfield',
													name : 'internal_email',
													labelAlign : 'right'
												},
												{
												xtype:'checkboxfield',
												name:'unreview',
												fieldLabel : 'Un Review',
												labelAlign : 'right',
												labelWidth:80
												}, {
													xtype : 'button',
													text : 'Search'
												}, 
												{
												xtype:'checkboxfield',
												name:'new_user',
												fieldLabel : 'New User',
												labelAlign : 'right'
												},
													{
													xtype : 'button',
													text : 'Net Sync'
												}, {
													xtype : 'button',
													text : 'Full Sync'
												}]
									}]
						}, {
							xtype : 'gridpanel',
							region : 'center',
							header : false,
							anchor : '100% 80%',
							store : 'TicketUsers',
							frame : true,
							margins : 5,
							columns : [{
										xtype : 'gridcolumn',
										dataIndex : 'internet_email',
										text : 'internet email',
										width : 200
									}, {
										xtype : 'gridcolumn',
										dataIndex : 'itcode',
										text : 'Itcode',
										editor : 'textfield'
									}, {
										xtype : 'gridcolumn',
										dataIndex : 'first_name',
										text : 'first name',
										editor : 'textfield'
									}, {
										xtype : 'gridcolumn',
										dataIndex : 'last_name',
										text : 'Last Name',
										editor : 'textfield'
									}, {
										xtype : 'gridcolumn',
										dataIndex : 'user_type',
										text : 'User Type',
										editor : 'textfield'
									}, {
										xtype : 'gridcolumn',
										dataIndex : 'org_id',
										text : 'org',
										width : 200,
										editor : 'textfield'
									}, {
										xtype : 'gridcolumn',
										dataIndex : 'country',
										text : 'Country',
										editor : 'textfield'
									}, {
										xtype : 'gridcolumn',
										dataIndex : 'state',
										text : 'State',
										editor : 'textfield'
									}, {
										xtype : 'gridcolumn',
										dataIndex : 'phone',
										text : 'Phone',
										editor : 'textfield'
									}, {
										xtype : 'gridcolumn',
										dataIndex : 'sub_biz',
										text : 'Sub Biz',
										editor : {
											xtype : 'combo',
											store : me.sub_biz,
											queryMode : 'local',
											valueField : 'value'
										}
									}, {
										xtype : 'gridcolumn',
										dataIndex : 'function_group',
										text : 'Function Group',
										width : 150,
										editor : {
											xtype : 'combo',
											store : me.function_group,
											queryMode : 'local',
											valueField : 'value'
										}
									}],
							plugins : [Ext.create('Ext.grid.plugin.RowEditing',
									{
										clicksToEdit : 1
									})]
						}]
			}]
		});
		me.callParent(arguments);
	},
	select_rc : function(combo, record, index) {
		me = this;
		me.root_cause.load({
					params : {
						rc_category : record[0].data.rc_category
					}
				});
	},
	select_issue_category : function(combo, record, index) {
		me = this;
		me.issue_problem.load({
					params : {
						assigned_group : me.context.record.data.assigned_group,
						issue_category : record[0].data.issue_category
					}
				});
	}
});
