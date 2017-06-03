Ext.define('workflow_report.view.WorkflowRunTrend', {
	extend : 'Ext.panel.Panel',
	alias : 'widget.WorkflowRunTrend',
	title : 'Run Trend',
	padding : 0,
	layout : {
		type : 'vbox'
	},
	initComponent : function() {
		var me = this;
		Ext.applyIf(me, {
			items : [{
						xtype : 'panel',
						title : 'Run Trend',
						flex : 1,
						frame:true,
						width:'100%',
						collapsible:true,
						layout : {
							type : 'vbox'
						},
						items : [{
									xtype : 'chart',
									style : 'background:#fff',
									animate : true,
									store : 'WflRunTrend',
									shadow : true,
									title : 'Run Trend',
									frame : true,
									flex : 1,
									width : '100%',
									legend : {
										position : 'right'
									},
									axes : [{
												type : 'Numeric',
												minimum : 0,
												position : 'left',
												fields : ['runtime', 'gatetime'],
												title : 'Workflow Run Time',
												minorTickSteps : 1,
												grid : {
													odd : {
														opacity : 1,
														fill : '#ddd',
														stroke : '#bbb',
														'stroke-width' : 0.5
													}
												}
											}, {
												type : 'Category',
												position : 'bottom',
												fields : ['run_day'],
												title : 'Run Day'
											}],
									series : [{
												type : 'line',
												highlight : {
													size : 7,
													radius : 7
												},
												axis : 'left',
												xField : 'run_day',
												yField : 'runtime',
												markerConfig : {
													type : 'cross',
													size : 4,
													radius : 4,
													'stroke-width' : 0
												}
											}, {
												type : 'line',
												highlight : {
													size : 7,
													radius : 7
												},
												axis : 'left',
												smooth : true,
												xField : 'run_day',
												yField : 'gatetime',
												markerConfig : {
													type : 'circle',
													size : 4,
													radius : 4,
													'stroke-width' : 0
												}
											}]
								}]
					}, {
						xtype : 'gridpanel',
						flex : 1,
						tutle : 'Run Log',
						width : '100%',
						store : 'WflRunTrend',
						margin : '5,0,0,0',
						collapsible:true,
						frame : true,
						columns : [{
									xtype : 'gridcolumn',
									dataIndex : 'system_name',
									text : 'System Name'
								}, {
									xtype : 'gridcolumn',
									dataIndex : 'runid',
									text : 'Run Id',
									width : 250
								}, {
									xtype : 'gridcolumn',
									dataIndex : 'workflow',
									text : 'Workflow'
								}, {
									xtype : 'gridcolumn',
									dataIndex : 'starttime',
									text : 'Start Time',
									width : 150
								}, {
									xtype : 'gridcolumn',
									dataIndex : 'endtime',
									text : 'End Time',
									width : 150
								}, {
									xtype : 'gridcolumn',
									dataIndex : 'status',
									text : 'Status'
								}, {
									xtype : 'gridcolumn',
									dataIndex : 'runtime',
									text : 'Runtime'
								}, {
									xtype : 'gridcolumn',
									dataIndex : 'gatetime',
									text : 'Gatetime'
								}, {
									xtype : 'gridcolumn',
									dataIndex : 'over_gatetime',
									text : 'Over Gatetime',
									width : 150
								}, {
									xtype : 'gridcolumn',
									dataIndex : 'is_break',
									text : 'Break'
								}]
					}]
		});
		me.callParent(arguments);
	}
});
