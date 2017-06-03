Ext.define('free_query.view.ReportFilter', {
	extend : 'Ext.window.Window',
	alias : 'widget.ReportFilter',
	initComponent : function() {
		var me = this;

		Ext.applyIf(me, {
			title : 'Report Filter',
			height : 500,
			width : 800,
			layout : 'fit',
			items : []
		});

		me.callParent(arguments);

		Ext.Ajax.request({
			url : "/free_query/report_filter?id=" + me.report_id,
			success : function(response, config) {
				json = Ext.JSON.decode(response.responseText);
				filterFields = json;
				Ext.define('list_model', {
					extend : 'Ext.data.Model',
					fields : [{
						type : 'string',
						name : 'text'
					}, {
						type : 'string',
						name : 'value'
					}]
				});

				//Ext.Msg.alert('Warning!', response.responseText);
				me.filterForm = Ext.create('Ext.form.FormPanel', {
					bodyPadding : 10,
					fieldDefaults : {
						labelAlign : 'left',
						labelWidth : 120,
						anchor : '100%'
					},
					listeners : {
						afterRender : function(thisForm, options) {
							this.keyNav = Ext.create('Ext.util.KeyNav', this.el, {
								enter : me.onApplyClick,
								scope : me
							});
						}
					},
					autoScroll : true,
					items : filterFields,
					buttons : [{
						text : 'export',
						listeners : {
							click : {
								fn : me.onExport,
								scope : me
							}
						}
					}, '-', {
						text : 'clear',
						listeners : {
							click : {
								fn : me.onClearClick,
								scope : me
							}
						}
					}, '-', {
						text : 'Search',
						width : 150,
						listeners : {
							click : {
								fn : me.onApplyClick,
								scope : me
							}
						}
					}]
				});

				Ext.each(me.filterForm.query("combo"), function(comObj) {
					comObj.store = Ext.create('Ext.data.Store', {
						model : 'list_model',
						proxy : {
							type : 'ajax',
							url : "/free_query/filter_list?id=" + me.report_id + "&name=" + comObj.filter_name,
							reader : {
								type : 'json'
							}
						}
					});
				});
				me.add(me.filterForm);

			},
			failure : function() {
				Ext.Msg.alert('Warning!', 'There is some error when get filter ' + me.title + '!');
			}
		});
	},
	onExport : function(btn, e, eOpts) {
		me = this;
		if(!me.getFilter())
		{
			return;
		}
		me.parent.doExport();
	},
	onClearClick : function(btn, e, eOpts) {
		me = this;
		filter_form = me.query("form")[0];
		filter_form.form.reset();
	},
	onApplyClick : function(btn, e, eOpts) {
		me = this;
		if(!me.getFilter())
		{
			return;
		}
		me.close();
		//{params:{filters:Ext.JSON.encode(values)}}
		me.report_store.loadPage(1, {
			scope : me,
			callback : function(records, operation, success) {
				if (!success) {
					me.show();
					Ext.Msg.alert('Warning!', 'data load faild');
				} else {
					var sb = me.parent.query("statusbar")[0];
					if(me.report_store.totalCount<200)
					{
                        sb.setStatus({
                            text: me.report_store.totalCount + ' rows return！',
                            iconCls: 'x-status-valid'
                        });
					}
					else{
						sb.setStatus({
                            text: 'Warning! Only ' +me.report_store.totalCount + ' rows return！',
                            iconCls: 'x-status-error'
                        });
					}
				}
			}
		});
	},
	getFilter : function() {
		me = this;
		filter_form = me.query("form")[0].form;
		invalid_fields = filter_form.getFields().filterBy(function(field) {
			return !field.validate();
		});

		/*
		if filter type in number or date, there are three field for each filter if the invalid field is less than 3.
		should ignore the invalid.
		*/
		//begin remove ignore invalid filed
		var map = {};
		var len = invalid_fields.items.length;
		for (var j = 0; j < len; j++) {
			field = invalid_fields.items[j];
			if (field.filter_type == 'number' || field.filter_type == 'date') {
				if (!map[field.getName()]) {
					map[field.getName()] = 1;
				} else {
					map[field.getName()] = map[field.getName()] + 1;
				}
			}
		}
		var count = len;
		for (var i in map) {
			// remove the
			if (map[i] < 3) {
				count = count - map[i];
			}
		}
		//end remove ignore invalid filed
		//if count >0 there are some invalid filed do nothing
		if (count) {
			return false;
		}

		var values = [];
		fields = filter_form.getFields().items;
		fLen = fields.length;

		var field, val;

		for (var f = 0; f < fLen; f++) {
			field = fields[f];
			val = field.getSubmitValue();
			if (val == '') {
				continue;
			}
			//alert(val);
			filter = {};
			data = {};
			filter["field"] = field.getName();
			data["type"] = field.filter_type;
			data["comparison"] = field.comparison;
			data["value"] = val;
			filter["data"] = data;
			values.push(filter);
		}
		//alert(Ext.JSON.encode(values));
		//me.report_store.filter(values);
		//me.report_store.filter("login_name",'lidm1');
		me.report_store.filter_params = {
			filters : Ext.JSON.encode(values)
		};
		
		return true;
	}
});
