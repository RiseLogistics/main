# -*- coding: utf-8 -*-
{
    'version': "0.1",
    'name': "leaflink",
    'summary': "LeafLink Connector",
    'category': 'Connector',
    # 'live_test_url': "",
    'images': [],
    'application': True,

    'author': "DYME",
    'website': "https://dyme.com",
    'license': "Other proprietary",

    'depends': [
        'sale',
        'product',
        'stock',
        'contacts',
    ],
    'external_dependencies': {"python": [], "bin": []},

    'data': [
    ],
    'qweb': [
        # 'static/src/xml/*.xml',
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
    Handle order creation and inventory sync to LeafLink.
"""
}
