Ext.define('tools.view.IconsGlyph', {
	extend: 'Ext.container.Viewport',
	autoScroll : true,
	height : 700,
	width : '100%',
	title : 'Icon Glyph',

	initComponent : function() {
		var me = this;

		//alert(parseInt("F000", 16));

		Ext.Ajax.request({
			url : STATIC_ROOT+"/toolbox/tools/store/data/icons_map.json",
			success : function(response, config) {
				json = Ext.JSON.decode(response.responseText);
				me.icons = json;

				icon_panel = Ext.create('Ext.panel.Panel', {
					layout : {
						type : 'table',
						columns : 10,
						tdAttrs : {
							style : 'padding: 5px 3px;'
						}
					}
				});

				for (var i = 0; i < me.icons.length; i++) {
					temp_icon = me.icons[i];

					var temp = Ext.create('Ext.button.Button', {
						glyph : parseInt(me.icons[i].font_code, 16),
						text : temp_icon.icon_class,
						maxWidth:150,
						font_code : temp_icon.font_code,
						icon_class : temp_icon.icon_class,
						tooltip : 'icon_class : ' + temp_icon.icon_class + '\nfont_code : ' + temp_icon.font_code + '\nfont_code(10) : ' + parseInt(temp_icon.font_code, 16),
						tooltipType:  'title'
					});
					icon_panel.add(temp);
				}
				me.add(icon_panel);
				Ext.QuickTips.init();
			}
		});
		Ext.applyIf(me);
		me.callParent(arguments);

		//Ext.applyIf(me);

	},

	show_code : function(btn, e, eOpts) {

		Ext.Msg.alert('Icon Info', 'icon_class : ' + btn.icon_class + '<br/> font_code :' + btn.font_code + '<br/> font_code(10) : ' + parseInt(btn.font_code, 16));
	}
});
