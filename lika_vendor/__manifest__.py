{
    'name': "Lika Cranes - Vendor Profile Extension for Purchase",
    'version': '1.0',
    'category': 'Inventory/Purchase',
    'summary': 'Extend res.partner with Indonesian Tax Info and Custom Documents',
    'depends': ['base', 'product', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/product_supplierinfo_views.xml'
    ],
    'installable': True,
    'application': False,
}
# {
#     'name': "Vendor Data Management",

#     'summary': "Manage vendor data and related information",

#     'description': """
# Manage vendor data, including contact information, addresses, and related documents. This module provides a comprehensive solution for maintaining accurate and up-to-date vendor records within the system.
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

