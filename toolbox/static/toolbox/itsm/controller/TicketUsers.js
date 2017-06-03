Ext.define('itsm.controller.TicketUsers', {
	extend : 'Ext.app.Controller',

	views : ['TicketUsers'],
	models : ['TicketUsers'],
	stores : ['TicketUsers'],

	init : function(application) {
		me = this;
		this.control({
					"form[uid=search_form] button[text=Search]" : {
						click : me.doSearch
					},
					"form[uid=search_form] button[text='Net Sync']" : {
						click : me.doNetSync
					},
					"form[uid=search_form] button[text='Full Sync']" : {
						click : me.doFullSync
					},
					"gridpanel" : {
						edit : function(editor, context, eOpts) {
							me.getStore('TicketUsers').sync();
						},
						beforeedit : function(editor, context, eOpts) {

							view = Ext.ComponentQuery.query("viewport")[0];
							view.function_group.load({
										params : {
											name : 'function_group'
										}
									});
						}
					}
				});
	},
	doSearch : function(btn, e, eOpts) {
		search_form = Ext.ComponentQuery.query("form[uid=search_form]")[0].form;

		me.getStore('TicketUsers').load({
					params : search_form.getValues()
				});
	},
	doFullSync : function(btn, e, eOpts) {
		search_form = Ext.ComponentQuery.query("form[uid=search_form]")[0].form;
		if (search_form.getValues().new_user == 'on') {
			new_user = true;
		} else {
			new_user = false;
		}
		Remote.itsm.sync_ticket_users({
					type : 'full',
					new_user : new_user
				}, function(result, event) {
					clearInterval(me.interval);
					if (!event.status) {
						Ext.Msg.alert('Warning!',
								'User Information Sync Failed');
					}
				});
		// this hideous block creates the bogus progress
		var f = function(starttime) {
			return function() {
				var runtime = ((new Date()) - starttime);
				var i = (runtime / 1000) % 10 / 10;
				Ext.MessageBox.updateProgress(i, 'Sync User Information - '
								+ Math.floor(runtime / 1000 / 60) + ' : '
								+ Math.floor((runtime / 1000)) % 60);
			};
		};

		me.interval = setInterval(f((new Date())), 1000);
	},
	doNetSync : function(btn, e, eOpts) {
		search_form = Ext.ComponentQuery.query("form[uid=search_form]")[0].form;
		if (search_form.getValues().new_user == 'on') {
			new_user = true;
		} else {
			new_user = false;
		}
		Remote.itsm.sync_ticket_users({
					type : 'nc',
					new_user : new_user
				}, function(result, event) {
					clearInterval(me.interval);
					if (!event.status) {
						Ext.Msg.alert('Warning!',
								'User Information Sync Failed');
					}
				});
		// this hideous block creates the bogus progress
		var f = function(starttime) {
			return function() {
				var runtime = ((new Date()) - starttime);
				var i = (runtime / 1000) % 10 / 10;
				Ext.MessageBox.updateProgress(i, 'Sync User Information - '
								+ Math.floor(runtime / 1000 / 60) + ' : '
								+ Math.floor((runtime / 1000)) % 60);
			};
		};

		me.interval = setInterval(f((new Date())), 1000);
	},
	onLaunch : function() {
		// this.getStore("TicketAnalyze").load();

	}
});
