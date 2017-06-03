Ext.setGlyphFontFamily("FontAwesome");
SERVER_INVALID = 'server';
CONNECT_FAILURE = 'connect';
CLIENT_INVALID = 'client';
LOAD_FAILURE = 'load';
STATIC_ROOT = 'http://' + window.location.host + '/static';
// CF_ROOT = 'cf:http://' + window.location.host;
CF_ROOT = '';

Ext.Loader.setPath('Ext.ux', STATIC_ROOT + '/ux');
Ext.Ajax.timeout = 1800000;
//Ext.Loader.setPath('common', STATIC_ROOT + '/toolbox/common/app');

if(!Array.indexOf){
            Array.prototype.indexOf = function(obj){
                for(var i=0; i<this.length; i++){
                    if(this[i]==obj){
                        return i;
                    }
                }
                return -1;
            }
        }

Ext.Date.patterns = {
	ISO8601Long : "Y/m/d H:i:s",
	ISO8601Short : "Y/m/d",
	ShortDate : "n/j/Y",
	LongDate : "l, F d, Y",
	FullDateTime : "l, F d, Y g:i:s A",
	MonthDay : "F d",
	ShortTime : "g:i A",
	LongTime : "g:i:s A",
	SortableDateTime : "Y/m/d\\TH:i:s",
	UniversalSortableDateTime : "Y/m/d H:i:sO",
	YearMonth : "F, Y"
};

if (Ext.form.field.Time) {
	Ext.apply(Ext.form.field.Time.prototype, {
		minText : "The time in this field must be equal to or after {0}",
		maxText : "The time in this field must be equal to or before {0}",
		invalidText : "{0} is not a valid time",
		format : "H:i",
		altFormats : "g:ia|g:iA|g:i a|g:i A|h:i|g:i|H:i|ga|ha|gA|h a|g a|g A|gi|hi|gia|hia|g|H"
	});
}

if (Ext.form.field.Date) {
	Ext.apply(Ext.form.field.Date.prototype, {
				disabledDaysText : "Disabled",
				disabledDatesText : "Disabled",
				minText : "The date in this field must be after {0}",
				maxText : "The date in this field must be before {0}",
				invalidText : "{0} is not a valid date - it must be in the format {1}",
				format : Ext.Date.patterns.ISO8601Short,
				altFormats : "m/d/Y|m-d-y|m-d-Y|m/d|m-d|md|mdy|mdY|d|Y-m-d"
			});
}

if (Ext.form.field.Date) {
	Ext.apply(Ext.form.field.Date.prototype, {
				disabledDaysText : "Disabled",
				disabledDatesText : "Disabled",
				minText : "The date in this field must be after {0}",
				maxText : "The date in this field must be before {0}",
				invalidText : "{0} is not a valid date - it must be in the format {1}",
				format : Ext.Date.patterns.ISO8601Short,
				altFormats : "m/d/Y|m-d-y|m-d-Y|m/d|m-d|md|mdy|mdY|d|Y-m-d"
			});
}
if (Ext.grid.column.Date) {
	Ext.apply(Ext.grid.column.Date.prototype, {
				format : Ext.Date.patterns.ISO8601Long
			})
}
if (Ext.data.Field) {
	Ext.apply(Ext.data.Field.prototype, {
				dateFormat : Ext.Date.patterns.ISO8601Long,
				dateWriteFormat : Ext.Date.patterns.ISO8601Long
			});
}

if (Ext.form.DisplayField) {
	Ext.apply(Ext.form.DisplayField.prototype, {
				dateFormat : Ext.Date.patterns.ISO8601Long
			});
}

Ext.getUrlParam = function(param) {

	var params = Ext.urlDecode(location.search.substring(1));

	return param ? params[param] : params;

};

/*
 * alert(navigator.appCodeName); alert(navigator.appName);
 * alert(navigator.appVersion);
 */

Ext.ns('Dg');

Dg.common = function(){
    var msgCt;

    function createBox(t, s){
       // return ['<div class="msg">',
       //         '<div class="x-box-tl"><div class="x-box-tr"><div class="x-box-tc"></div></div></div>',
       //         '<div class="x-box-ml"><div class="x-box-mr"><div class="x-box-mc"><h3>', t, '</h3>', s, '</div></div></div>',
       //         '<div class="x-box-bl"><div class="x-box-br"><div class="x-box-bc"></div></div></div>',
       //         '</div>'].join('');
       return '<div class="msg"><h3>' + t + '</h3><p>' + s + '</p></div>';
    }
    return {
        msg : function(title, format){
            if(!msgCt){
                msgCt = Ext.DomHelper.insertFirst(document.body, {id:'msg-div'}, true);
            }
            var s = Ext.String.format.apply(String, Array.prototype.slice.call(arguments, 1));
            var m = Ext.DomHelper.append(msgCt, createBox(title, s), true);
            m.hide();
            m.slideIn('t').ghost("t", { delay: 5000, remove: true});
        },

        init : function(){
            if(!msgCt){
                // It's better to create the msg-div here in order to avoid re-layouts 
                // later that could interfere with the HtmlEditor and reset its iFrame.
                msgCt = Ext.DomHelper.insertFirst(document.body, {id:'msg-div'}, true);
            }
//            var t = Ext.get('exttheme');
//            if(!t){ // run locally?
//                return;
//            }
//            var theme = Cookies.get('exttheme') || 'aero';
//            if(theme){
//                t.dom.value = theme;
//                Ext.getBody().addClass('x-'+theme);
//            }
//            t.on('change', function(){
//                Cookies.set('exttheme', t.getValue());
//                setTimeout(function(){
//                    window.location.reload();
//                }, 250);
//            });
//
//            var lb = Ext.get('lib-bar');
//            if(lb){
//                lb.show();
//            }
        }
    };
}();

 //鑾峰彇鍓垏鏉挎暟鎹� 鍑芥暟
    function getClipboard() {
        if (window.clipboardData) {
            return (window.clipboardData.getData('Text'));
        }
        else if (window.netscape) {
            netscape.security.PrivilegeManager.enablePrivilege('UniversalXPConnect');
            var clip = Components.classes['@mozilla.org/widget/clipboard;1'].createInstance(Components.interfaces.nsIClipboard);
            if (!clip) return;
            var trans = Components.classes['@mozilla.org/widget/transferable;1'].createInstance(Components.interfaces.nsITransferable);
            if (!trans) return;
            trans.addDataFlavor('text/unicode');
            clip.getData(trans, clip.kGlobalClipboard);
            var str = new Object();
            var len = new Object();
            try {
                trans.getTransferData('text/unicode', str, len);
            }
            catch (error) {
                return null;
            }
            if (str) {
                if (Components.interfaces.nsISupportsWString) str = str.value.QueryInterface(Components.interfaces.nsISupportsWString);
                else if (Components.interfaces.nsISupportsString) str = str.value.QueryInterface(Components.interfaces.nsISupportsString);
                else str = null;
            }
            if (str) {
                return (str.data.substring(0, len.value / 2));
            }
        }
        return null;
    }