{
    'name': "Purchase Order Custom for Lika Crane",
    'category': 'General',
    'author': 'Instep',
    "version": "1.0",
    'depends': ['purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order.xml',
        'report/report_purchase_paperformat.xml',
        'report/report_purchase_order.xml',
        'report/report_purchase_action.xml',
    ],
    'installable':True,
}
