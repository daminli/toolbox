
Ext.define('free_query.model.Reports', {
    extend: 'Ext.data.Model',

    fields: [
        {
            name: 'id'
        },
        {
            name: 'file_name'
        },
        {
            name: 'start_time'
        },
        {
            name: 'end_time'
        },
        {
            name: 'total count'
        },
        {
            name: 'export_by'
        }
    ]
});