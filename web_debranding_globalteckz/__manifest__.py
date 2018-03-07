# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
#    Globalteckz Software Solutions and Services                             #
#    Copyright (C) 2013-Today(www.globalteckz.com).                          #
#                                                                            #
#    This program is free software: you can redistribute it and/or modify    #
#    it under the terms of the GNU Affero General Public License as          #
#    published by the Free Software Foundation, either version 3 of the      #
#    License, or (at your option) any later version.                         #
#                                                                            #
#    This program is distributed in the hope that it will be useful,         #  
#    but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#    GNU Affero General Public License for more details.                     #
#                                                                            #
#                                                                            #
##############################################################################
{
    "name" : "Odoo 11 Debranding Look and feel",
    "version" : "11.0.1.0",
    "depends" : ["base","web"],
    "author" : "Globalteckz",
    "description": """Odoo 11 change your backend theme and Branding based on your company name """,
    "website" : "www.globalteckz.com",
    "category" : "Extra Tools",
    'images': ['static/description/Banner.png'],
    "license" : "Other proprietary",
    "price": "30.00",
    "currency": "EUR",
    'summary': 'Change your Odoo Theme/colors and Branding based on your company name',
    'qweb': [],
    "data" : [
            'views/res_config_view.xml',
            'views/brand_template.xml',
            'views/template.xml',
    ],
    "installable": True,
}
