# -*- coding: utf-8 -*-
{
    'version': "0.2",
    'name': "COA Printing",
    'summary': "DYME COA Printing",
    'category': 'Manufacturing',
    # 'live_test_url': "",
    'images': [],
    'application': True,

    'author': "DionyMed Brands Inc",
    'website': "https://dyme.com",
    'license': "Other proprietary",

    'depends': [
        'stock'
    ],
    'external_dependencies': {"python": [], "bin": []},

    'data': [
        'views/coa_wizard.xml',
        'security/ir.model.access.csv'
    ],
    'qweb': [
    ],
    'demo': [
    ],

    'post_load': None,
    'pre_init_hook': None,
    'post_init_hook': None,
    'uninstall_hook': None,

    'auto_install': False,
    'installable': True,

    'description': """
    Handle merging and printing COAs
"""
}
