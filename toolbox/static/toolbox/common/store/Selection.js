Ext.define('common.store.Selection', {
    extend: 'Ext.data.Store',
    requires: [
        'common.model.Selection'
    ],

    constructor: function(cfg) {
        var me = this;
        cfg = cfg || {};
        me.callParent([Ext.apply({
            model: 'common.model.Selection',
            paramsAsHash:true,
            proxy: {
                type: 'direct',
                directFn: Remote.selection.get_selections,
                reader: {
                    type: 'json'
                }
            }
        }, cfg)]);
    }
});