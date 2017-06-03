Ext.define('sql_executor.view.ExecuteSql', {
	extend : 'Ext.container.Viewport',
	controllers : ['RunScript'],
	layout : 'card',
	activeItem : 0, // index or id
	initComponent : function() {
		var me = this;
		me.application.getController(me.controllers);

		Ext.applyIf(me, {
			items : [{
				xtype : 'panel',
				layout : {
					type : 'vbox',
					padding : '5',
					align : 'left'
				},
				defaults : {
					margins : '0 0 5 0'
				},
				items : [{
					xtype : 'form',
					title : 'Execute Request',
					id : 'request_form',
					frame : true,
					width : 800,
					layout : 'anchor',
					border : false,
					bodyPadding : 10,
					fieldDefaults : {
						labelAlign : 'top',
						labelWidth : 100,
						labelStyle : 'font-weight:bold'
					},
					defaults : {
						anchor : '90%',
						margins : '0 0 10 0'
					},
					items : [{
						xtype : 'textareafield',
						fieldLabel : 'Summary',
						name : 'summary',
						labelAlign : 'top',
						height : 200,
						margin : '0',
						allowBlank : false,
						msgTarget : 'under',
						minLength : '20',
						emptyText : "Please input your execute reason! Can't be blank and min length is 20 "
					}],
					buttons : [{
						text : 'Next',
						listeners : {
							click : function(btn, e, eOpts) {
								request_form = me.query("#request_form")[0].form;
								if (!request_form.isValid())
									return;
								request_form.submit({
									url : '/sql_executor/new_request',
									method : 'POST',
									success : function(form, action) {
										run_script = me
												.query("#RunScriptPanel")[0];
										run_script.exec_id = action.result.data.id;
										me.getLayout()
												.setActiveItem(++me.activeItem);

									},
									failure : function(form, action) {
										if (action.failureType == SERVER_INVALID) {
											Ext.Msg.alert('Warning!',
													'request create faild!');
										}
										if (action.failureType == CONNECT_FAILURE) {
											Ext.Msg.alert('Warning!',
													'Server is unreachable!');
										}
									}
								});
							}
						}
					}]
				}]
			}, {
				xtype : 'RunScript',
				id : 'RunScriptPanel'
			}]
		});
		me.callParent(arguments);
	}
});
