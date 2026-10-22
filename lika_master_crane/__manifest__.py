{
    'name': 'Master Crane Model',
    'version': '1.0',
    'category': 'Inventory/Products',
    'summary': 'Add Crane Model management and link it to Products',
    'depends': ['product', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        
        'views/crane_model_views.xml',
        'views/crane_make_views.xml',
        'views/crane_type_views.xml',
        'views/crane_document_views.xml',
    ],
    'installable': True,
    'application': False,
}
# {
#     'name': "lika_master_crane",

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
