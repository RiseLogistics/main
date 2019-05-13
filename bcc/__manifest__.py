# -*- coding: utf-8 -*-
{
    'version': "0.1",
    'name': "License Scrapper Adapter",
    'summary': "BCC, CDFA & MCSB license scrapper",
    'category': "Manufacturing",
    'images': [],
    'application': True,
    'sequence': 1,
    'author': "DionyMed Brands Inc",
    'website': "http://dyme.com",
    'license': "Other proprietary",
    'depends': [
        "stock",
        "sale"
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

    'post_load': None,
    'pre_init_hook': None,
    'post_init_hook': None,
    'uninstall_hook': None,

    'auto_install': False,
    'installable': True,

    'description': """
    This tool allows the res.partner record to be extended, allowing us to store license status and information twice per day.
    Please see https://cannabis.ca.gov/check_a_license/ for more information.
"""
}
