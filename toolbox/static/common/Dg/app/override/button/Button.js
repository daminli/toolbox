Ext.define('Dg.override.button.Button', {
    override: 'Ext.button.Button',
    margin: '1px',
    initComponent : function() {
				var me = this;

				me.callParent(arguments);
				me.checkActivity(this);
			},
			checkActivity : function(button) {
				if (button.activity != null) {

					switch (button.activity) {
						case 'view' :
							(userAcl.view == 'true') ? button.show() : button
									.hide();
							break;
						case 'create' :
							(userAcl.create == 'true') ? button.show() : button
									.hide();
							break;
						case 'edit' :
							(userAcl.edit == 'true') ? button.show() : button
									.hide();
							break;
						case 'delete' :
							(userAcl.remove == 'true') ? button.show() : button
									.hide();
							break;
						case 'upload' :
							(userAcl.upload == 'true') ? button.show() : button
									.hide();
							break;
						default :
							button.hide();
							break;
					}
				} else {
					button.show();
				}
			}
    
});