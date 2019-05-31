# -*- coding: utf-8 -*-

from odoo.addons.component.core import Component


class LeafLinkProductAdapter(Component):
    _name = 'leaflink.product.template.adapter'
    _inherit = "leaflink.adapter"
    _usage = 'backend.adapter'
    _apply_on = "leaflink.product.template"
    _leaflink_model = "product"
    _external_model = "Products"
