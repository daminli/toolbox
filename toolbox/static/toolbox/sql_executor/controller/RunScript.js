/*
 * File: app/controller/Navigation.js
 * 
 * This file was generated by Sencha Architect version 2.2.2.
 * http://www.sencha.com/products/architect/
 * 
 * This file requires use of the Ext JS 4.2.x library, under independent
 * license. License of Sencha Architect does not include license for Ext JS
 * 4.2.x. For more details see http://www.sencha.com/license or contact
 * license@sencha.com.
 * 
 * This file will be auto-generated each and everytime you save your project.
 * 
 * Do NOT hand edit this file.
 */

Ext.define('sql_executor.controller.RunScript', {
	extend : 'Ext.app.Controller',

	views : ['ExecuteSql', 'RunScript'],
	models : ['RunDetail'],
	stores : ['RunDetail'],

	init : function(application) {
		me = this;
		this.control({
			"#run_script" : {
				click : function(btn, e, eOpts) {
					run_script = Ext.ComponentQuery.query("#RunScriptPanel")[0];
					script_form = Ext.ComponentQuery.query("#script_form")[0].form;
					data = script_form.getValues();
					if (data.datasource == '') {
						Ext.Msg
								.alert('Warning!',
										'Please select a datasource!');
						return;
					}
					if (data.scripts == '') {
						Ext.Msg.alert('Warning!', "Script can't be null!");
						return;
					}
					btn.disable();
					script_form.submit({
								url : '/sql_executor/run_script?exec_id='
										+ run_script.exec_id,
								method : 'POST',
								waitMsg:"scripts is running",  
								success : function(form, action) {
									me.getStore("RunDetail").load({
												params : {
													run_id : action.result.data.run_id
												}
											});
									Ext.Msg.alert('Warning!',
											'script run success');
									btn.enable();

								},
								failure : function(form, action) {
									if (action.failureType == SERVER_INVALID) {
										Ext.Msg.alert('Warning!',
												'script run faild! '+action.result.data.error);
									}
									if (action.failureType == CONNECT_FAILURE) {
										Ext.Msg.alert('Warning!',
												'Server is unreachable!');
									}
									btn.enable();
								}
							});
				}
			},
			"#run_plsql" : {
				click : function(btn, e, eOpts) {
					run_script = Ext.ComponentQuery.query("#RunScriptPanel")[0];
					script_form = Ext.ComponentQuery.query("#script_form")[0].form;
					data = script_form.getValues();
					if (data.datasource == '') {
						Ext.Msg
								.alert('Warning!',
										'Please select a datasource!');
						return;
					}
					if (data.scripts == '') {
						Ext.Msg.alert('Warning!', "Script can't be null!");
						return;
					}
					script_form.submit({
								url : '/sql_executor/run_script_block?exec_id='
										+ run_script.exec_id,
								method : 'POST',
								waitMsg:"scripts is running",  
								success : function(form, action) {
									me.getStore("RunDetail").load({
												params : {
													run_id : action.result.data.run_id
												}
											});
									Ext.Msg.alert('Warning!',
											'script run success');

								},
								failure : function(form, action) {
									if (action.failureType == SERVER_INVALID) {
										Ext.Msg.alert('Warning!',
												'script run faild');
									}
									if (action.failureType == CONNECT_FAILURE) {
										Ext.Msg.alert('Warning!',
												'Server is unreachable!');
									}
								}
							});
				}
			}
		});

	}

});
