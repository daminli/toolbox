Ext.define('itsm.view.TicketAnalyze', {
	extend : 'Ext.container.Viewport',
	alias : 'itsm.ticketanalyze',
	controllers : ['TicketAnalyze'],
	padding : 5,
	initComponent : function() {
		var me = this;
		me.application.getController(me.controllers);

		me.ta_status = Ext.create('Ext.data.Store', {
					fields : ['text'],
					data : [{
								text : 'initial'
							}, {
								text : 'review'
							}, {
								text : 'confirmed'
							}]
				});

		me.release = Ext.create('common.store.SelectList');
		me.release.load({
					params : {
						name : 'release'
					}
				});

		me.problem_category = Ext.create('common.store.SelectList');
		me.problem_category.load({
					params : {
						name : 'problem_category'
					}
				});

		me.sub_biz = Ext.create('common.store.SelectList');
		me.sub_biz.load({
					params : {
						name : 'sub_biz'
					}
				});

		me.root_cause = Ext.create('itsm.store.RootCause');
		me.issue_problem = Ext.create('itsm.store.Issue');
		me.issue_category = Ext.create('itsm.store.IssueCategory');
		me.search_result = Ext.create('itsm.store.SearchResult');
		me.rc_category = Ext.create('itsm.store.RCCategory');

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
									xtype : 'datefield',
									name : 'from_date',
									fieldLabel : 'Creation Date',
									value : Ext.Date.add(new Date(),
											Ext.Date.DAY, -10)
								}, {
									fieldLabel : 'To',
									xtype : 'datefield',
									labelWidth : 30,
									labelAlign : 'right',
									name : 'to_date',
									value : (new Date)
								},{
									fieldLabel : 'Incident',
									xtype : 'textfield',
									labelAlign : 'right',
									name : 'incident_id',
									labelWidth : 70
								},
								{
									fieldLabel : 'Assign Group',
									xtype : 'textfield',
									labelAlign : 'right',
									name : 'assigned_group',
									labelWidth : 50
								}, {
									fieldLabel : 'Assignee',
									xtype : 'textfield',
									labelAlign : 'right',
									name : 'assignee',
									labelWidth : 50
								}, {
									fieldLabel : 'Status',
									name:'ta_status',
									labelAlign : 'right',
									xtype : 'combo',
									store : me.ta_status,
									queryMode : 'local',
									labelWidth : 50,
									width:200
								}, {
									text : 'Search',
									listeners : {
										click : {
											fn : me.onSearch,
											scope : me
										}
									}
								}]
							}]
						}, {
							xtype : 'form',
							bodyPadding : 10,
							anchor : '100% 12%',
							uid : 'detail_form',
							layout : {
								type : 'hbox',
								align : 'stretch'
							},
							frame : true,
							defaults : {
								labelWidth : 30,
								labelheight : 10,
								hideLabel : true,
								labelAlign : 'top',
								margin : '0 5 0 0'
							},
							items : [{
										xtype : 'textarea',
										name : 'summary',
										flex : 1,
										fieldLabel : 'summary'
									}, {
										xtype : 'textarea',
										name : 'notes',
										flex : 1,
										fieldLabel : 'Notes'
									}, {
										xtype : 'textarea',
										name : 'resolution',
										flex : 2,
										fieldLabel : 'Resolution'
									}]
						}, {
							xtype : 'gridpanel',
							region : 'center',
							header : false,
							anchor : '100% 80%',
							store : me.search_result,
							frame : true,
							margins : 5,
							columns : [{
										xtype : 'gridcolumn',
										dataIndex : 'incident_id',
										text : 'Incident Id',
										width : 130
									}, {
										xtype : 'gridcolumn',
										dataIndex : 'assignee',
										text : 'Assignee',
										width : 80
									}, {
										xtype : 'gridcolumn',
										dataIndex : 'ori_root_cause',
										text : 'Ori Root Cause',
										width : 200
									}, {
										xtype : 'gridcolumn',
										dataIndex : 'rc_category',
										text : 'RC Category',
										width : 150,
										editor : {
											xtype : 'combo',
											store : me.rc_category,
											queryMode : 'local',
											displayField : 'rc_category',
											listeners : {
												scope : me,
												'select' : me.select_rc
											}
										}
									}, {
										xtype : 'gridcolumn',
										dataIndex : 'root_cause',
										text : 'Root Cause',
										width : 200,
										editor : {
											xtype : 'combo',
											store : me.root_cause,
											queryMode : 'local',
											displayField : 'root_cause'
										}
									}, {
										xtype : 'gridcolumn',
										dataIndex : 'problem_category',
										text : 'Problem Category',
										width : 200,
										editor : {
											xtype : 'combo',
											store : me.problem_category,
											queryMode : 'local'
										}
									}, {
										xtype : 'gridcolumn',
										dataIndex : 'issue_category',
										text : 'Issue Category',
										width : 200,
										editor : {
											xtype : 'combo',
											store : me.issue_category,
											queryMode : 'local',
											displayField : 'issue_category',
											listeners : {
												scope : me,
												'select' : me.select_issue_category
											}
										}
									}, {
										xtype : 'gridcolumn',
										dataIndex : 'issue',
										text : 'Issue',
										width : 200,
										editor : {
											xtype : 'combo',
											store : me.issue_problem,
											queryMode : 'local',
											displayField : 'issue'
										}
									}, {
										xtype : 'gridcolumn',
										dataIndex : 'issue_comment',
										text : 'Comment',
										editor : 'textfield'
									}, {
										xtype : 'gridcolumn',
										dataIndex : 'ta_status',
										text : 'Status',
										editor : {
											xtype : 'combo',
											store : me.ta_status,
											queryMode : 'local'
										}
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
										dataIndex : 'release',
										text : 'Release',
										width : 100,
										editor : {
											xtype : 'combo',
											store : me.release,
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
						product_categorization_tier3 : me.context.record.data.product_categorization_tier3,
						issue_category : record[0].data.issue_category
					}
				});
	}
});
