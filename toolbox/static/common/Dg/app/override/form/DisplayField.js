Ext.define('Dg.override.form.DisplayField', {
			override : 'Ext.form.DisplayField',
			getValue : function() {
				return this.value;
			},
			setValue : function(v) {
				this.value = v;
				this.setRawValue(this.formatValue(v));
				return this;
			},
			formatValue : function(v) {
				if (this.dateFormat && Ext.isDate(v)) {
					//return v.dateFormat(this.dateFormat);
					return Ext.util.Format.date(v,this.dateFormat)
				}
				if (this.numberFormat && typeof v == 'number') {
					return Ext.util.Format.number(v, this.numberFormat);
				}
				return v;
			}
		});