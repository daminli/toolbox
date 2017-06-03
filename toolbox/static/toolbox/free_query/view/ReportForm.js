Ext.define('free_query.view.ReportForm', {
			extend : 'Ext.form.Panel',
			alias : 'widget.reportform',
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

				Ext.applyIf(me, {
							dockedItems : [{
										dock : 'top',
										xtype : 'toolbar',
										items : [{
													glyph : 61717,
													xtype : 'button',
													text : 'Open'
												},'-',{
													glyph : 61508,
													xtype : 'button',
													text : 'Edit'
												}, '-', {
													glyph : 61527,
													xtype : 'button',
													text : 'Delete'
												}, '->', {
													glyph : 61446,
													xtype : 'button',
													text : 'Add Favorit',
													enableToggle: true
												}, {
													glyph : 61445,
													xtype : 'button',
													text : 'Remove Favorit',
													enableToggle: true
												}, {
													xtype : 'displayfield',
													width:100
												}]
									}],
							items : [{
										xtype : 'fieldcontainer',
										layout : 'hbox',
										items : [{
													xtype : 'textfield',
													fieldLabel : 'Id',
													name : 'id',
													hidden : true,
													hideLabel : true
												}, {
													xtype : 'displayfield',
													fieldLabel : 'Unique Name',
													width : 400,
													name : 'name'
												}, {
													xtype : 'displayfield',
													fieldLabel : 'Data Source',
													width : 300,
													name : 'datasource'
												}]
									}, {
										xtype : 'fieldcontainer',
										layout : 'hbox',
										items : [{
													xtype : 'displayfield',
													fieldLabel : 'Display Name',
													width : 400,
													name : 'display_name'
												}, {
													xtype : 'treepicker',
													fieldLabel : 'Folder',
													width : 300,
													id : 'folder_id',
													name : 'folder_id',
													displayField : 'text',
													rootVisible : false,
													store : me.folderStore
												}]
									}, {
										xtype : 'textareafield',
										fieldLabel : 'Report Desc',
										name : 'rpt_desc'
									}, {
										xtype : 'textareafield',
										fieldLabel : 'Sql Query',
										name : 'sql_query'
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