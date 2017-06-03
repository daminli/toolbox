Ext.define('itsm.store.TicketAnalyze', {
    extend: 'Ext.data.Store',
    requires: [
        'itsm.model.TicketAnalyze'
    ],

    constructor: function(cfg) {
        var me = this;
        cfg = cfg || {};
        me.callParent([Ext.apply({
            model: 'itsm.model.TicketAnalyze',
            paramsAsHash:true,
            proxy: {
                type: 'direct',
                directFn: Remote.itsm.get_ticket_analyze,
                reader: {
                    type: 'json'
                }
            }
        }, cfg)]);
    }
});