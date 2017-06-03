Ext.define('workflow_report.view.WorkflowNodeTrend', {
			extend : 'Ext.window.Window',
			alias : 'widget.WorkflowNodeTrend',
			title : 'Node Trend',
			padding : 0,
			layout : {
				type : 'vbox'
			},
			initComponent : function() {
				var me = this;
				Ext.applyIf(me, {
							items : [{
										xtype : 'chart',
										style : 'background:#fff',
										animate : true,
										store : 'WflNodeTrend',
										shadow : true,
										title : 'Node Trend',
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
													fields : ['runtime'],
													title : 'Run Time',
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
												}]
									}]
						});
				me.callParent(arguments);
			}
		});
