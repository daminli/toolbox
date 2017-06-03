Ext.define('itsm.store.Issue', {
    extend: 'Ext.data.Store',
    requires: [
        'itsm.model.IssueCategory'
    ],

    constructor: function(cfg) {
        var me = this;
        cfg = cfg || {};
        me.callParent([Ext.apply({
            model: 'itsm.model.IssueCategory',
            paramsAsHash:true,
            proxy: {
                type: 'direct',
                directFn: Remote.itsm.get_issue,
                reader: {
                    type: 'json'
                }
            }
        }, cfg)]);
    }
});