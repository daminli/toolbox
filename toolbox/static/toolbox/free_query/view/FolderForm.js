Ext.define('free_query.view.FolderForm', {
			extend : 'Ext.form.Panel',
			alias : 'widget.folderform',
			layout : {
				align : 'stretch',
				type : 'vbox'
			},
			initComponent : function() {
				var me = this;

				me.folderStore = Ext.create('free_query.store.FolderTree', {
							proxy : {
								type : 'ajax',
								url : '/free_query/report_folder?root_id=1',
								reader : {
									type : 'json'
								}
							}
						});
				// folderStore.load()
				Ext.applyIf(me, {
							dockedItems : [{
										dock : 'top',
										xtype : 'toolbar',
										items : [{
													glyph : 61639,
													xtype : 'button',
													text : 'Save'
												}, '-', {
													glyph : 61462,
													xtype : 'button',
													text : 'Create'
												}, '-', {
													glyph : 61527,
													xtype : 'button',
													text : 'Delete'
												}]
									}],
							items : [{
										xtype : 'textfield',
										fieldLabel : 'Id',
										name : 'id',
										hidden : true,
										hideLabel : true
									}, {
										xtype : 'textfield',
										fieldLabel : 'Folder Name',
										activity : 'edit',
										name : 'name'
									}, {
										xtype : 'treepicker',
										fieldLabel : 'Parant Folder',
										id : 'parent_id',
										name : 'parent_id',
										displayField : 'text',
										store : me.folderStore
									}, {
										xtype : 'displayfield',
										fieldLabel : 'Create By',
										name : 'create_by'
									}, {
										xtype : 'displayfield',
										fieldLabel : 'Creation Date',
										name : 'creation_date'
									}]
						});

				me.callParent(arguments);
			}
		});