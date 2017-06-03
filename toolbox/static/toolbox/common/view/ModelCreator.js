Ext.define('common.view.ModelCreator', {
	extend : 'Ext.container.Viewport',
	// controllers : ['ModelCreator'],
	padding : 5,
	initComponent : function() {
		var me = this;
		// me.application.getController(me.controllers);

		var type = Ext.create('Ext.data.Store', {
					fields : ['text'],
					data : [{
								text : 'db_table'
							}, {
								text : 'db_sql'
							}, {
								text : 'cls_name'
							}, {
								text : 'table'
							}]
				});

		Ext.applyIf(me, {
					items : [{
								xtype : 'form',
								bodyPadding : 10,
								height:600,
								layout : 'anchor',
								title : 'Model Creator',
								defaults : {
									anchor : '100%'
								},
								frame : true,
								dockedItems : [{
											dock : 'top',
											xtype : 'toolbar',
											items : [{
														xtype : 'combo',
														labelAlign : 'left',
														name : 'type',
														store : type,
														queryMode : 'local'
													}, {
														xtype : 'textfield',
														labelAlign : 'left',
														name : 'value'
													}, {
														text : 'Search',
														listeners : {
															click : {
																fn : me.onSearch,
																scope : me
															}
														}
													}]
										}],
								items : [{
											xtype : 'textarea',
											name : 'model_script',
											labelAlign : 'top',
											fieldLabel : 'Model Script',
											anchor : '60% 40%'
										}]
							}]
				});
		me.callParent(arguments);
	},
	onSearch : function(button, e, eOpts) {
		console.log(button.text);
		console.log(button.up().up().getValues());
		Remote.dict.get_model(button.up().up().getValues(), function(result,
						event) {
					str = Ext.JSON.encode(result);
					str = str.replace(/"(\w+)"(\s*:\s*)/g, "$1$2");
					Ext.ComponentQuery.query("form[title='Model Creator']")[0].form
							.setValues({
										model_script : str
									});
				})
	}
});
