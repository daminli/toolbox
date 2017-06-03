Ext.define('sql_executor.controller.ExecHistory', {
	extend : 'Ext.app.Controller',

	views : ['ExecHistory', 'SearchExecHistory'],
	models : ['ExecHistory', 'RunLog', 'RunDetail'],
	stores : ['ExecHistory', 'RunLog', 'RunDetail'],

	init : function(application) {
		me = this;
		this.control({
			"#btnSearch" : {
				click : function(btn, e, eOpts) {
					search_form = Ext.ComponentQuery.query("#ExecSearchForm")[0].form;
					data = search_form.getValues();
					me.getStore("ExecHistory").load({
								params : data
							});
				}
			},
			"#ExecHisGrid" : {
				selectionchange : function(row, records, eOpts) {
					me.getStore("RunLog").load({
								params : {
									exec_id : records[0].data.id
								}
							});
				}
			},
			"#RunLogGrid" : {
				'cellclick' : function(grid, td, cellIndex, record, tr,
						rowIndex, e, eOpts) {
					if (grid.getHeaderAtIndex(cellIndex).dataIndex == 'script') {
						Ext.Msg.alert('Script', record.data.script);
					}
					if (grid.getHeaderAtIndex(cellIndex).dataIndex == 'result') {
						Ext.Msg.alert('Result', record.data.result);
					}
					return;
				},
				'itemdblclick' : function(grid, record, item, index, e, eOpts) {

					var vrTabpanel = Ext.ComponentQuery
							.query("#ExecHistoryTabpanel")[0];
					if (vrTabpanel.items.length > 1) {
						var tab = Ext.getCmp('ViewRunLog');
						vrTabpanel.remove(tab);
					}
					var newPage = Ext.create("sql_executor.view.RunScript", {
								title : record.data.id,
								run_id : record.data.id,
								exec_id : record.data.exec_id,
								run_log : record.data,
								readOnly : true,
								closable : true,
								id : 'ViewRunLog'
							});
					vrTabpanel.add(newPage);
					vrTabpanel.show();
					vrTabpanel.setActiveTab(newPage);
					me.getStore("RunDetail").load({
								params : {
									run_id : record.data.id
								}
							});
				}
			}
		});
	}

});
