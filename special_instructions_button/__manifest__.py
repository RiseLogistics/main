# -*- coding: utf-8 -*-
{
    'version': "0.1",
    'name': "Product Special Instructions Button",
    'summary': "Stock Picking Product Special Instructions",
    'category': "Manufacturing",
    'images': [],
    'application': True,
    'sequence': 1,
    'author': "DionyMed Brands Inc",
    'website': "http://dyme.com",
    'license': "Other proprietary",
    'depends': [
        "stock"
    ],

    'external_dependencies': {"python": [], "bin": []},

    'data': [
        'views/stock_picking_special_instructions.xml',
    ],

    'post_load': None,
    'pre_init_hook': None,
    'post_init_hook': None,
    'uninstall_hook': None,

    'auto_install': False,
    'installable': True,

    'description': """
    Extend stock picking view to display special instructions button if instructions exist..
"""

}
