# -*- coding: utf-8 -*-
{
    'version': "0.1",
    'name': "Express PO handler",
    'summary': "Create POs via a controller endpoint",
    'category': "Manufacturing",
    'images': [],
    'application': True,
    'sequence': 1,
    'author': "DionyMed Brands Inc",
    'website': "http://dyme.com",
    'license': "Other proprietary",
    'depends': [
        "stock",
        "purchase"
    ],

    'external_dependencies': {"python": [], "bin": []},

    'data': [
        'security/ir.model.access.csv',
    ],

    'post_load': None,
    'pre_init_hook': None,
    'post_init_hook': None,
    'uninstall_hook': None,

    'auto_install': False,
    'installable': True,

    'description': """
    PO order creation wrapper
"""
}
