Ext.define('itsm.store.RootCause', {
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
                directFn: Remote.itsm.get_root_cause,
                reader: {
                    type: 'json'
                }
            }
        }, cfg)]);
    }
});