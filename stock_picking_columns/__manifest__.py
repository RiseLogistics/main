# -*- coding: utf-8 -*-
{
    'version': "0.1",
    'name': "Stock Pick DYME Columns",
    'summary': "Extend stock picking view",
    'category': "Manufacturing",
    'images': [],
    'application': True,
    'sequence': 1,
    'author': "DionyMed Brands Inc",
    'website': "http://dyme.com",
    'license': "Other proprietary",
    'depends': [
        "stock",
    ],

    'external_dependencies': {"python": [], "bin": []},

    'data': [
        'views/stock_picking_filters.xml',
    ],

    'post_load': None,
    'pre_init_hook': None,
    'post_init_hook': None,
    'uninstall_hook': None,

    'auto_install': False,
    'installable': True,

    'description': """
    Extend stock picking view to display route schedule, region, SO edits.
"""

}
