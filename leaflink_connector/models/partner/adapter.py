# -*- coding: utf-8 -*-

from odoo.addons.component.core import Component


class LeafLinkPartnerAdapter(Component):
    _name = 'leaflink.res.partner.adapter'
    _inherit = "leaflink.adapter"
    _usage = 'backend.adapter'
    _apply_on = "leaflink.res.partner"
    _leaflink_model = "customer"
    _external_model = "Customers"
