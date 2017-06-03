Ext.define('itsm.controller.TicketAnalyze', {
	extend : 'Ext.app.Controller',

	views : ['TicketAnalyze'],
	models : ['TicketAnalyze', 'SearchResult', 'IssueCategory',
			'TicketRootCause'],
	stores : ['TicketAnalyze', 'SearchResult', 'IssueCategory', 'Issue',
			'RCCategory', 'RootCause'],

	init : function(application) {
		me = this;
		this.control({
			"form[uid=search_form] button[text=Search]" : {
				click : me.doSearch
			},
			"gridpanel" : {
				selectionchange : function(row, records, eOpts) {
					if (records.length > 0) {
						incident_form = Ext.ComponentQuery
								.query("form[uid='detail_form']")[0].form;
						incident_form.setValues(records[0].data);
					}
				},
				beforeedit : function(editor, context, eOpts) {

					view = Ext.ComponentQuery.query("viewport")[0];
					view.context = context;
					view.issue_category.load({
								params : {
									assigned_group : context.record.data.assigned_group,
									product_categorization_tier3 : context.record.data.product_categorization_tier3
								}
							});

					view.problem_category.load({
								params : {
									name : 'problem_category'
								}
							});

					view.rc_category.load();

					if (context.record.data.issue_category) {
						view.issue_problem.load({
							params : {
								assigned_group : context.record.data.assigned_group,
								issue_category : context.record.data.issue_category
							}
						});
					}

					if (context.record.data.rc_category) {
						view.root_cause.load({
							params : {
								assigned_group : context.record.data.assigned_group,
								rc_category : context.record.data.rc_category
							}
						});
					}
				},
				edit : function(editor, context, eOpts) {
					// console.log(editor);
					view = Ext.ComponentQuery.query("viewport")[0];
					view.search_result.sync();
				}
			}
		});
	},
	doSearch : function(btn, e, eOpts) {
		search_form = Ext.ComponentQuery.query("form[uid=search_form]")[0].form;

		// search_form.submit();
		view = Ext.ComponentQuery.query("viewport")[0];
		view.search_result.load({
					params : search_form.getValues()
				});
	},
	onLaunch : function() {
		// this.getStore("TicketAnalyze").load();

	}
});
