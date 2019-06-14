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


    so_modified_at = fields.Datetime(string="SO Modified On",
                                     related="sale_id.write_date",
                                     store=True,
                                     copy=True,
                                     readonly=True,
                                     default=None)

    so_modified_by = fields.Many2one("res.users",
                                     related="sale_id.write_uid",
                                     copy=True,
                                     store=True,
                                     readonly=True)


    so_delivery_date = fields.Datetime(string="Scheduled Delivery",
                                       related="sale_id.so_delivery_task.x_scheduled_at",
                                       store=True,
                                       readonly=True,
                                       default=None)


class SODeliveryTask(models.Model):
    _inherit = "sale.order"

    so_delivery_task = fields.One2many(comodel_name="x_dispatch_task",
                                       inverse_name="x_order_id",
                                       domain=[("x_task_type", "=", "PRODUCT_DELIVERY")],
                                       readonly=True,
                                       default=None)
