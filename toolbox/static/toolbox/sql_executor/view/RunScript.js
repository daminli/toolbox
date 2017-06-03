

Ext.define('sql_executor.view.RunScript', {
	extend : 'Ext.panel.Panel',
	alias : 'widget.RunScript',
	exec_id : '',
	run_log : '',
	readOnly : false,
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
		Ext.applyIf(me, {
			items : [{
				xtype : 'form',
				id : 'script_form',
				title : 'Run Scripts',
				collapsible : true,
				frame : true,
				layout : 'anchor',
				border : false,
				bodyPadding : 10,
				fieldDefaults : {
					labelAlign : 'top',
					labelWidth : 100,
					labelStyle : 'font-weight:bold'
				},
				defaults : {
					anchor : '80%',
					margins : '0 0 10 0'
				},
				dockedItems : [{
					dock : 'top',
					xtype : 'toolbar',
					items : [{
								glyph : 61515,
								xtype : 'button',
								text : 'Run',
								id : 'run_script',
								disabled : me.readOnly
							}, '-', {
								glyph : 61518,
								xtype : 'button',
								text : 'Run PL/SQL',
								id : 'run_plsql',
								disabled : me.readOnly
							}, '-', {
								xtype : 'combo',
								labelAlign : 'left',
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
												url : "/common/get_data_source?ds_group=sql_executor",
												reader : {
													type : 'json'
												}
											}
										}),
								queryMode : 'remote',
								displayField : 'name',
								valueField : 'name',
								allowBlank : false,
								msgTarget : 'side',
								emptyText : "Select a datasource",
								value : (me.readOnly)
										? me.run_log.data_source
										: ''
							}]
				}],
				items : [{
							xtype : 'textareafield',
							name : 'scripts',
							labelAlign : 'top',
							id : 'scripts',
							grow : true,
							growMin : 300,
							growMax : 500,
							margin : '0',
							allowBlank : false,
							msgTarget : 'tiltle',
							editable : !me.readOnly,
							value : (me.readOnly) ? me.run_log.script : ''
						}]
			}, {
				xtype : 'gridpanel',
				split : true,
				header : false,
				minHeight : 300,
				maxHeight : 400,
				id : 'RunDetailGrid',
				frame : true,
				store : 'RunDetail',
				plugins : [{
					ptype : 'rowexpander',
					rowBodyTpl : ['<p><b>Script:</b> {sql_text}</p><br>',
							'<p><b>Result: </b> {result}</p>']
				}],
				columns : [{
							xtype : 'gridcolumn',
							dataIndex : 'id',
							text : 'Id',
							width : 130
						}, {
							xtype : 'gridcolumn',
							dataIndex : 'sql_text',
							text : 'Sql Text',
							width : 450
						}, {
							xtype : 'gridcolumn',
							dataIndex : 'result',
							text : 'Result',
							width : 300,
							renderer : function(val, cellmeta, record) {
								if (record.data.status == 'success') {
									return '<span style="color:green;">' + val
											+ '</span>';
								} else if (record.data.status == 'failure') {
									return '<span style="color:red;">' + val
											+ '</span>';
								}
								return val;
							}
						}, {
							xtype : 'gridcolumn',
							dataIndex : 'status',
							text : 'Status',
							renderer : function(val) {
								if (val == 'success') {
									return '<span style="color:green;">' + val
											+ '</span>';
								} else if (val == 'failure') {
									return '<span style="color:red;">' + val
											+ '</span>';
								}
								return val;
							}
						}, {
							xtype : 'gridcolumn',
							dataIndex : 'run_by',
							text : 'Run By'
						}]

			}]
		});

		me.callParent(arguments);
		if (me.readOnly) {
			me.query('#datasource')[0].store.load();
		}

	}
});
