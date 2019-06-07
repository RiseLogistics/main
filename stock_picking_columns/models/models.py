# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockPickingColumns(models.Model):
    _inherit = "stock.picking"

    dyme_route_schedule = fields.Many2one("x_route_schedule",
                                          related="partner_id.x_route_schedule",
                                          store=True,
                                          copy=True,
                                          readonly=True)

    dyme_partner_region = fields.Selection("Region",
                                           related="partner_id.x_studio_field_P4UbZ",
                                           store=True,
                                           copy=True,
                                           readonly=True)


