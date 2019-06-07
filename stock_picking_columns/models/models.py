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


    so_modified_at = fields.Datetime("SO Modified On",
                                     related="sale_id.write_date",
                                     store=True,
                                     copy=True,
                                     readonly=True)
    #
    # so_modified_by = fields.Many2one("res.users",
    #                                  related="sale_id.write_uid",
    #                                  copy=True,
    #                                  store=True,
    #                                  readonly=True)
