{
    'name': "Lika Cranes - Verification Order Module",
    'summary': "Generates quotations based on verified product selections.",
    "author": "Arkana Solusi Digital extended by Megareka",
    "website": "https://github.com/ArkanaDigital/lika",
    'category': 'Uncategorized',
    "version": "19.0.1.0.0",
    'depends': [
        'base',
        'sale',
        'sale_crm',
        'sequence_reset_period'
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/verification_order_views.xml',
        # 'views/crm_lead_views.xml',
    ],
}
