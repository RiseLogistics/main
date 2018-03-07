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

import time
import datetime
from dateutil.relativedelta import relativedelta

import odoo
from odoo import SUPERUSER_ID
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import unicodedata

import os
import base64

class RebrandingConfigSettings(models.TransientModel):
    _name = 'rebranding.config.settings'
    _inherit = 'res.config.settings'

    brand_logo = fields.Binary(string='Brand Logo')
    brand_name = fields.Char(string="Brand Name")
    brand_website = fields.Char(string='Brand Website')
    favicon_icon = fields.Binary(string='Favicon Icon')
    
#     Theme's Fields
    top_image = fields.Binary('Top BackGround Image')
    sidebar_image = fields.Binary('Sidebar BackGround Image', help='You can set image at the left bar behind'
                                                                   ' the font such as your company logo.''keep this field empty '
                                                                   'if you need background colour.')
    menu_font_color = fields.Char('Font Color', default='#FFFFFF')
    menu_background_color = fields.Char('BackGround Color', default='#B71E17')
    
    leftfont_color_parent = fields.Char('Parent Font Color', default='#FFDC63')
    left_background_color = fields.Char('BackGround Color', default='#464746')
    leftfont_color = fields.Char('Font Colour of Child', default='#FFFFFF')
    
    font_common = fields.Selection([('sans-serif', 'Sans-Serif'),
                                   ('serif', 'Serif'),
				                   ('verdana', 'Verdana'), 
                                   ('monospace', 'Monospace'), ], default='monospace')
    

   
    @api.model
    def set_values(self):
       config = self.env['ir.config_parameter']
       config.set_param('cust.brand_logo', self.brand_logo or False)
       self.env.user.company_id.logo = self.brand_logo
       config.set_param('cust.brand_name', self.brand_name or False)
       config.set_param('cust.favicon_icon', self.favicon_icon or False)
       config.set_param('cust.brand_website', self.brand_website or False)
       config.set_param('cust.leftfont_color', self.leftfont_color or False)
       config.set_param('cust.leftfont_color_parent', self.leftfont_color_parent or False)
       config.set_param('cust.menu_font_color', self.menu_font_color or False)
       config.set_param('cust.menu_background_color', self.menu_background_color or False)
       config.set_param('cust.left_background_color', self.left_background_color or False)
       config.set_param('cust.font_common', self.font_common or False)
       
    def get_values(self):
#      
       res = super(RebrandingConfigSettings, self).get_values()
       get_param = self.env['ir.config_parameter'].sudo().get_param
       res.update(
        brand_logo = get_param('cust.brand_logo'),
        brand_name = get_param('cust.brand_name'),
        favicon_icon = get_param('cust.favicon_icon'),
        brand_website = get_param('cust.brand_website'),
        leftfont_color = get_param('cust.leftfont_color'),
        leftfont_color_parent = get_param('cust.leftfont_color_parent'),
        menu_font_color =  get_param('cust.menu_font_color'),
        menu_background_color = get_param('cust.menu_background_color'),
        left_background_color = get_param('cust.left_background_color'),
        font_common = get_param('cust.font_common'),
        )
       return res
        
        