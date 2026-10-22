{
    'name': "Lika Cranes - Sale Module Custom",
    'summary': "Custom enhancements for Odoo Sale module.",
    "author": "Arkana Solusi Digital extended by Megareka",
    'category': 'Uncategorized',
    "version": "19.0.1.0.0",
    'depends': ['base', 'sale','sale_stock', 'delivery'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/delivery_point_views.xml',
        'views/menuitem.xml',
    ],
}
