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
from io import BytesIO
import base64
import functools
import babel.messages.pofile
import base64
import json
import io

from odoo.modules import get_resource_path
from odoo import http
from odoo.tools.misc import file_open
from odoo.addons.web.controllers.main import Binary
from datetime import datetime
 
 
class WebFavicon(http.Controller):
    
    @http.route('/web_favicon/ficn', type='http',  auth="public")
    def icon(self):
        request = http.request
        favicon_icon = request.env['ir.config_parameter'].sudo().get_param('cust.favicon_icon')
#         favicon_icon = favicon_obj.get_param('cust.favicon_icon')
        if not favicon_icon:
            favicon = file_open('web/static/src/img/favicon.ico')
            favicon_mimetype = 'image/x-icon'
        else:
            favicon = io.BytesIO(base64.b64decode(favicon_icon))
        return request.make_response(
            favicon.read(), [('Content-Type', 'image/x-icon')])
         
    @http.route('/web_brand/brand_name', type='json', auth="none")
    def footer_brand(self):
        request = http.request
        brand_name = request.env['ir.config_parameter'].get_param('cust.brand_name')
        return brand_name
     
    @http.route(['/get_brand_value/'], type='json', auth="public", website=True)
    def action_get_css_selected(self):
        value_obj = request.env['ir.config_parameter'].get_param('cust.brand_name')
        vals = {
            'brand_name': 'test'
        }
        return vals
     
    @http.route(['/get_brand_info_login/'], type='http', auth="public", website=True) 
    def get_brand_info_login(self):
        request = http.request
        vals = {}
        value_obj = request.env['ir.config_parameter']
        brand_name = value_obj.get_param('cust.brand_name')
        brand_website = value_obj.get_param('cust.brand_website')
        vals = ''
        if brand_name:
            vals += brand_name + ','
        else:
            return 'Odoo' + ','
        if brand_website:
            vals += brand_website
        else:
            vals += 'www.odoo.com'
        return vals
      
    @http.route(['/get_css_selected/'], type='json', auth="public")
    def action_get_css_selected(self):
        request = http.request
        vals = {}
        get_css = request.env['ir.config_parameter']
        leftfont_color = get_css.get_param('cust.leftfont_color')
        leftfont_color_parent = get_css.get_param('cust.leftfont_color_parent') 
        menu_font_color = get_css.get_param('cust.menu_font_color') 
        menu_background_color = get_css.get_param('cust.menu_background_color') 
        left_background_color = get_css.get_param('cust.left_background_color')
        font_common = get_css.get_param('cust.font_common')
        brand_name = get_css.get_param('cust.brand_name')
        brand_website = get_css.get_param('cust.brand_website')
        favicon = get_css.get_param('cust.favicon_icon')
         
        vals.update({'leftfont_color': leftfont_color, 
                     'leftfont_color_parent': leftfont_color_parent,
                     'leftfont_color_parent': leftfont_color_parent,
                     'menu_font_color': menu_font_color,
                     'menu_background_color': menu_background_color,
                     'left_background_color': left_background_color,
                     'leftfont_color': leftfont_color,
                     'font_common': font_common,
                     'brand_name' : brand_name or 'Odoo',
                     'brand_website': brand_website or 'www.odoo.com',
                     'favicon': favicon
        })
        return json.dumps(vals)
  
