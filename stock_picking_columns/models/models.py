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
                                     compute="_compute_so_modified_at",
                                     store=True,
                                     copy=True,
                                     readonly=True,
                                     default=None)
    #
    # so_modified_by = fields.Many2one("sale.order",
    #                                  related="sale_id.write_uid",
    #                                  copy=True,
    #                                  store=True,
    #                                  readonly=True)

    #
    @api.depends("origin")
    def _compute_so_modified_at(self):
        if self.sale_id and self.sale_id.write_date:
            return self.sale_id.write_date

        return None
