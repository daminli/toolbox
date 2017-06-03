Ext.define('sql_executor.view.SearchExecHistory', {
	extend : 'Ext.panel.Panel',
	alias : 'widget.SearchExecHistory',
	layout : {
		type : 'vbox',
		padding : '5',
		align : 'stretch'
	},
	defaults : {
		margins : '0 0 5 0'
	},
	title : 'Execute History',
	initComponent : function() {
		var me = this;

		Ext.applyIf(me, {
			items : [{
				xtype : 'form',
				region : 'center',
				height : 50,
				id : 'ExecSearchForm',
				bodyPadding : 10,
				layout : 'hbox',
				frame : false,
				fieldDefaults : {
								labelAlign : 'left',
								labelWidth : 100,
								labelStyle : 'font-weight:bold'
							},
				//title : 'Report Info',
				dockedItems : [{
					dock : 'top',
					xtype : 'toolbar',
					items : [{
						xtype : 'datefield',
						name : 'from_date',
						fieldLabel : 'Creation Date',
						value:(new Date)
					}, {

						fieldLabel : 'To',
						xtype : 'datefield',
						labelWidth : 30,
						labelAlign : 'right',
						name : 'to_date',
						value:(new Date)
					}, {
						xtype : 'textfield',
						fieldLabel : 'User',
						labelAlign : 'right',
						name : 'create_by'
					}, {
						text : 'Search',
						id : 'btnSearch'
					}]
				}]
			}, {
				xtype : 'gridpanel',
				header : true,
				minHeight:300,
				maxHeight:400,
				collapsible: true,
				id : 'ExecHisGrid',
				store : 'ExecHistory',
				title : 'Execute Requests',
				frame : true,
				columns : [{
					xtype : 'gridcolumn',
					dataIndex : 'id',
					text : 'Id',
					width : 130
				}, {
					xtype : 'gridcolumn',
					dataIndex : 'summary',
					text : 'Summary',
					width : 300
				}, {
					xtype : 'gridcolumn',
					dataIndex : 'creation_date',
					text : 'Createtion Date',
					width : 200
				}, {
					xtype : 'gridcolumn',
					dataIndex : 'create_by',
					text : 'User',
					width : 200
				}]
			}, {
				xtype : 'gridpanel',
				header : true,
				minHeight:200,
				maxHeight:400,
				collapsible: true,
				frame : true,
				bodyPadding : 10,
				id : 'RunLogGrid',
				store : 'RunLog',
				title : 'Run Log',
				plugins : [{
										ptype : 'rowexpander',
										rowBodyTpl : [
												'<p><b>Script:</b> {script}</p><br>',
												'<p><b>Result: </b> {result}</p>']
									}],
				columns : [{
					xtype : 'gridcolumn',
					dataIndex : 'id',
					text : 'Id',
					width : 130
				}, {
					xtype : 'gridcolumn',
					dataIndex : 'data_source',
					text : 'Data Source',
					width : 150
				}, {
					xtype : 'gridcolumn',
					dataIndex : 'start_time',
					text : 'Start Time',
					width : 200
				}, {
					xtype : 'gridcolumn',
					dataIndex : 'end_time',
					text : 'End Time',
					width : 200
				}, {
					xtype : 'gridcolumn',
					dataIndex : 'script',
					text : 'Script',
					width : 200
				}, {
					xtype : 'gridcolumn',
					dataIndex : 'result',
					text : 'Result',
					width : 200
				},{
					xtype : 'gridcolumn',
					dataIndex : 'status',
					text : 'Status',
					width : 200
				}, {
					xtype : 'gridcolumn',
					dataIndex : 'run_by',
					text : 'Run By',
					width : 200
				}]
			}]
		});

		me.callParent(arguments);
	}
});
