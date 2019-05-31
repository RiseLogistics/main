# -*- coding: utf-8 -*-
{
    'version': "0.2",
    'name': "leaflink_connector",
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
        'connector',
        'queue_job'
    ],
    'external_dependencies': {"python": [], "bin": []},

    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'qweb': [
        # 'static/src/xml/*.xml',
    ],
    'demo': [
        'demo/demo.xml'
    ],

    'post_load': None,
    'pre_init_hook': None,
    'post_init_hook': None,
    'uninstall_hook': None,

    'auto_install': False,
    'installable': True,

    'description': """
Enable products and customers export to LeafLink with order import only
"""
}
