# -*- coding: utf-8 -*-
{
    'name': "Product Vendor Update Wizard",
    'description': "A wizard to assist in mass updating product vendors",
    'summary': 'Product Vendor wizard',
    'author': 'Yazan H',
    'version': '1.1',
    'depends': [
        'stock',
        'product'
    ],
    'data': [
        'views/product_update_wizard_view.xml',
    ],
    'installable': True,
    'application': True,
}
