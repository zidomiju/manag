{
    'name': "Invoice Custom for Lika Crane",
    'category': 'General',
    'author': 'Instep',
    "version": "1.0",
    'depends': ['account','lika_report'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move.xml',
        'report/lika_invoice_paperformat.xml',
        'report/lika_kwintansi_paperformat.xml',
        'report/lika_invoice_report.xml',
        'report/lika_kwintansi_report.xml',
        'report/lika_invoice_action.xml',
    ],
    'installable':True,
}
