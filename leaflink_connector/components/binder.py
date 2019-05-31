# -*- coding: utf-8 -*-


from odoo.addons.component.core import Component


class LeafLinkModelBinder(Component):
    _name = "leaflink.binder"
    _inherit = ["base.binder", "base.leaflink.connector"]
    _apply_on = [
        "leaflink.res.partner",
        "leaflink.product.category",
        "leaflink.product.template",
        "leaflink.sale.order"
    ]
