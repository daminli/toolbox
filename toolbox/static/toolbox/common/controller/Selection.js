Ext.define('common.controller.Selection', {
	extend : 'Ext.app.Controller',

	views : ['Selection'],
	models : ['Selection'],
	stores : ['Selection'],

	init : function(application) {
		me = this;
		this.control({
					"form[uid=search_form] button[text=Search]" : {
						click : me.doSearch
					},
					"gridpanel" : {
						selectionchange : function(row, records, eOpts) {
							if (records.length > 0) {
								selection_form = Ext.ComponentQuery
										.query("form[title=Selection]")[0].form;
								selection_form.setValues(records[0].data);
							}
						}
					},
					"button[text=Save]" : {
						click : function(btn, e, eOpts) {
							selection_form = Ext.ComponentQuery
									.query("form[title=Selection]")[0].form;
							btn.disable();
							Remote.selection.save_selections(selection_form
											.getValues(), {
										callback : function(form, action,
												success) {
											btn.enable();
											if (!success) {
												Ext.Msg.alert('Warning!',
														action.message);
											} else {
												me.doSearch();
											}
										}
									});
						}
					},
					"button[text=Delete]" : {
						click : function(btn, e, eOpts) {
							selection_form = Ext.ComponentQuery
									.query("form[title=Selection]")[0].form;
							btn.disable();
							Remote.selection.del_selections(selection_form
											.getValues(), {
										callback : function(form, action,
												success) {
											btn.enable();
											selection_form.reset();
											if (!success) {
												Ext.Msg.alert('Warning!',
														action.message);
											} else {
												me.doSearch();
											}
										}
									});
						}
					}
				});
	},
	doSearch : function(btn, e, eOpts) {
		search_form = Ext.ComponentQuery.query("form[uid=search_form]")[0].form;

		// search_form.submit();
		me.getStore('Selection').load({
					params : search_form.getValues()
				});
	},
	onLaunch : function() {

		this.getStore("Selection").load();

	}
});
