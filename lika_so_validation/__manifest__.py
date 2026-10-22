{
    'name': "Lika Cranes - Sales Order Validation Custom",

    'summary': "Prevent SO creation with specified validations",

    'description': """
        Sales Order can only be created / generated when conditions set by this module is met
    """,

    'author': "Megareka",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Validation',
    'version': '19.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        'views/sale_order_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install':False
}

