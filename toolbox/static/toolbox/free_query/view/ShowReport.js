Ext.define('free_query.view.ShowReport', {
	extend : 'Ext.panel.Panel',
	alias : 'widget.ShowReport',
	layout : {
		type : 'border'
	},
	initComponent : function() {
		var me = this;
		Ext.Ajax.request({
			url : "/free_query/show_report?id=" + me.report_id,
			success : function(response, config) {
				json = Ext.JSON.decode(response.responseText);
				columns = json.columns;

				me.req_filter = json.req_filter;

				Ext.define('report_model', {
					extend : 'Ext.data.Model',
					fields : json.fields
				});

				// create the Data Store
				var store = Ext.create('Ext.data.Store', {
					//pageSize : 200,
					model : 'report_model',
					remoteSort : true,
					proxy : {
						type : 'ajax',
						url : "/free_query/report_data?id=" + me.report_id,
						timeout : 600000,
						reader : {
							type : 'json',
							root : 'data',
							totalProperty : 'total_count'
						},
						// sends single sort as multi parameter
						simpleSortMode : true,
						remoteSort : true
					}
				});
				store.on("beforeload", function(storeObj, operation, eOpts) {
					Ext.apply(storeObj.proxy.extraParams, storeObj.filter_params);
					//alert(Ext.JSON.encode(storeObj.filter_params));
					return true;
				});
				me.report_store = store;
				me.add(Ext.create('Ext.grid.Panel', {
					viewConfig : {
						enableTextSelection : true
					},
					store : store,
					region : 'center',
					columns : columns,
					header : false,
					tbar : {
						itemId : 'tbar',
						items : [{
							xtype : 'button',
							text : 'Reload',
							glyph : 61473,
							listeners : {
								click : {
									fn : me.doReload,
									scope : me
								}
							}
						}, '-', '-', {
							xtype : 'button',
							text : 'Filter',
							glyph : 61616,
							listeners : {
								click : {
									fn : me.onFilter,
									scope : me
								}
							}
						}, '-',
						/*{
						 xtype : 'button',
						 text : 'Hilight',
						 glyph : 61675,
						 listeners : {
						 click : {
						 fn : me.onHilight,
						 scope : me
						 }
						 }
						 }, '-', {
						 text : 'Chart',
						 glyph : 61568,
						 listeners : {
						 click : {
						 fn : me.onChart,
						 scope : me
						 }
						 }
						 }, */'-', {
							glyph : 61465,
							text : 'Export',
							listeners : {
								click : {
									fn : me.onExport,
									scope : me
								}
							}
						}]
					},
					// paging bar on the bottom
					/*
					 bbar : Ext.create('Ext.PagingToolbar', {
					 store : store,
					 displayInfo : true,
					 displayMsg : 'Displaying record {0} - {1} of {2}',
					 emptyMsg : "No data to display"
					 })
					 */
					bbar : Ext.create('Ext.ux.StatusBar', {
						//id : 'result-statusbar',
						defaultText : 'Search Result'
					})
				}));

				if (me.req_filter) {
					me.onFilter();
				} else {

					me.report_store.load({
						scope : me,
						callback : function(records, operation, success) {
							if (!success) {
								Ext.Msg.alert('Warning!', 'data load faild');
							} else {
								var sb = me.query("statusbar")[0];
								if (me.report_store.totalCount < 200) {
									sb.setStatus({
										text : me.report_store.totalCount + ' rows return！',
										iconCls : 'x-status-valid'
									});
								} else {
									sb.setStatus({
										text : 'Warning! Only ' + me.report_store.totalCount + ' rows return！',
										iconCls : 'x-status-error'
									});
								}
							}
						}
					});
				}
			},
			failure : function() {
				Ext.Msg.alert('Warning!', 'There is some error when open report ' + me.title + '!');
			}
		});

		Ext.applyIf(me);

		me.callParent(arguments);
	},
	doReload : function(btn, e, eOpts) {
		me = this;
		me.report_store.reload({
			scope : me,
			callback : function(records, operation, success) {
				if (!success) {
					Ext.Msg.alert('Warning!', 'data load faild');
				} else {
					var sb = me.query("statusbar")[0];
					if (me.report_store.totalCount < 200) {
						sb.setStatus({
							text : me.report_store.totalCount + ' rows return！',
							iconCls : 'x-status-valid'
						});
					} else {
						sb.setStatus({
							text : 'Warning! Only ' + me.report_store.totalCount + ' rows return！',
							iconCls : 'x-status-error'
						});
					}
				}
			}
		});
	},
	onFilter : function(btn, e, eOpts) {
		me = this;
		if (!me.filterWin) {
			me.filterWin = Ext.create("free_query.view.ReportFilter", {
				title : 'Report Filter',
				report_id : me.report_id,
				closable : !me.req_filter,
				closeAction : 'hide',
				maximizable : true,
				autoScroll : true,
				frame : true,
				scripts : true,
				report_store : me.report_store,
				parent : me
			});
		}
		me.filterWin.show();
	},
	onExport : function(btn, e, eOpts) {
		me = this;
		me.doExport(btn, e, eOpts);
		return;
		Ext.create("free_query.view.ReportExport", {
			title : 'Report Export',
			report_id : me.report_id,
			closable : true,
			autoScroll : true,
			frame : true,
			scripts : true
		}).show();
	},
	doExport : function(btn, e, eOpts) {
		me = this;

		Ext.MessageBox.show({
			title : 'Please wait',
			progressText : 'Initializing...',
			width : 300,
			progress : true,
			closable : true
		});

		var temp = me.report_store.sorters.items;
		sorters = {}
		if (temp.length > 0) {
			sorters = {
				sort : temp[0].property,
				dir : temp[0].direction
			};
		}

		Ext.Ajax.request({
			url : "/free_query/export_report",
			params : {
				id : me.report_id,
				filters : (me.report_store.filter_params) ? me.report_store.filter_params : '[]',
				sorters : sorters
			},
			waitMsg : " data export is running",
			success : function(response, config) {
				clearInterval(me.interval);
				Ext.MessageBox.hide();
				json = Ext.JSON.decode(response.responseText);
				Dg.common.msg('Data Export Finished ', 'report ' + me.title + ' data export successful');
				window.location.href = '/free_query/download_report/' + json.data.url;
			},
			failure : function() {
				clearInterval(me.interval);
				Ext.MessageBox.hide();
				Ext.Msg.alert('Warning!', 'report export faild ' + me.title + '!');
			}
		});

		// this hideous block creates the bogus progress
		var f = function(starttime) {
			return function() {
				var runtime = ((new Date()) - starttime);
				var i = (runtime / 1000) % 10 / 10;
				Ext.MessageBox.updateProgress(i, 'data export is running - ' + Math.floor(runtime / 1000 / 60) + ' : ' + Math.floor((runtime / 1000)) % 60);
			};
		};

		me.interval = setInterval(f((new Date())), 1000);
		/*
		 setTimeout(function() {
		 clearInterval(me.interval);
		 }, 500 * 100);
		 */
	},
	onHilight : function(btn, e, eOpts) {
		me = this;
		Ext.create("free_query.view.ReportHilight", {
			title : 'Report Hilight',
			report_id : me.report_id,
			closable : true,
			autoScroll : true,
			frame : true,
			scripts : true
		}).show();
	},
	onChart : function(btn, e, eOpts) {
		me = this;
		Ext.create("free_query.view.ReportChart", {
			title : 'Report Chart',
			report_id : me.report_id,
			closable : true,
			autoScroll : true,
			frame : true,
			scripts : true
		}).show();
	},
	destroy : function() {
		me = this;
		if (me.filterWin) {
			me.filterWin.destroy();
		}
		if (me.exportWin) {
			me.exportWin.destroy();
		}
	}
});
