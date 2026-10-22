{
    'name': "Lika Cranes - Spare Parts Management Custom",
    'summary': "Manage Spare Parts, Sub-Assemblies, Vendor Suppliers, and Specifications.",
    "author": "Megareka",
    'category': 'Inventory/Inventory',
    "version": "19.0.1.0.0",
    'depends': [
        'base',
        'stock',
        'sale',
        'purchase',
        'uom',
        'product',
        'lika_master_crane',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/product_template_views.xml',
        # 'views/spare_part_views.xml',
        # 'views/spare_part_menus.xml',
        # 'views/sparepart_category_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'lika_spareparts/static/src/js/image_fullscreen.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
