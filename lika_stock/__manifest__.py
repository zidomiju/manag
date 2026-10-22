{
    'name': "Lika Cranes - CIPL Stock Print Out Custom ",
    'version': '19.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Custom Commercial Invoice & Packing List Report',
    'depends': ['stock', 'sale_stock', 'stock_account'],
    'data': [
        # 'data/ir_sequence_data.xml',
        'views/stock_move_views.xml',
        # 'reports/report_deliveryslip.xml',
        'reports/delivery_slip_report.xml',
    ],
    'installable': True,
    'application': False,
}

# {
#     'name': "lika_stock",

#     'summary': "Short (1 phrase/line) summary of the module's purpose",

#     'description': """
# Long description of module's purpose
#     """,

#     'author': "My Company",
#     'website': "https://www.yourcompany.com",

#     # Categories can be used to filter modules in modules listing
#     # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
#     # for the full list
#     'category': 'Uncategorized',
#     'version': '0.1',

#     # any module necessary for this one to work correctly
#     'depends': ['base'],

#     # always loaded
#     'data': [
#         # 'security/ir.model.access.csv',
#         'views/views.xml',
#         'views/templates.xml',
#     ],
#     # only loaded in demonstration mode
#     'demo': [
#         'demo/demo.xml',
#     ],
# }

