Ext.define('itsm.store.RCCategory', {
    extend: 'Ext.data.Store',
    requires: [
        'itsm.model.TicketRootCause'
    ],

    constructor: function(cfg) {
        var me = this;
        cfg = cfg || {};
        me.callParent([Ext.apply({
            model: 'itsm.model.TicketRootCause',
            paramsAsHash:true,
            proxy: {
                type: 'direct',
                directFn: Remote.itsm.get_rc_category,
                reader: {
                    type: 'json'
                }
            }
        }, cfg)]);
    }
});