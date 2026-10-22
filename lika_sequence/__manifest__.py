{
    'name': "Lika Cranes - Sequence Module Custom",
    'summary': "Custom sequence management for Odoo records.",
    "author": "Arkana Solusi Digital extended by Megareka",
    'category': 'Uncategorized',
    "version": "19.0.1.0.0",
    'depends': [
        'base',
        'sale',
        'account',
        'account_move_name_sequence',
        'lika_account',
        'lika_sale',
        'sequence_reset_period',
        'hr'
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/views.xml',
        'views/res_users_views.xml',
    ],
}

