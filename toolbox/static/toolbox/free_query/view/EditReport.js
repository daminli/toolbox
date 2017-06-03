/**
 * @author lidm1
 */

Ext.define('free_query.view.EditReport', {
			extend : 'Ext.container.Viewport',
			id : 'EditReportView',
			report_id : null,
			controllers:['CreateReport'],
			initComponent : function() {
				var me = this;
				me.application.getController(me.controllers);
				me.report_id = Ext.getUrlParam('report_id');
				Ext.applyIf(me, {
							items : [{
										xtype : 'tabpanel',
										activeTab : 0,
										items : [{
													xtype : 'ReportInfoPanel',
													id : 'createReportInfo',
													report_id : me.report_id,
													title : 'Basic Info'
												}, {
													xtype : 'ReportPropPanel',
													id : 'createReportPropPanel',
													title : 'Report Props'
												}]
									}]
						});

				me.callParent(arguments);
			}
		});
