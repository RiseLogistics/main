# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ExpressPOModel(models.Model):
    _name = 'express.po'
    _description = "Express PO Creator"


class POTopGun(models.Model):
    _inherit = "purchase.order"

    location_id = fields.Many2one("stock.location")
    location_dest_id = fields.Many2one("stock.location")
    dyme_transfer_id = fields.Char()


class POLineTopGun(models.Model):
    _inherit = "purchase.order.line"

    lot_id = fields.Many2one("stock.production.lot")
    location_id = fields.Many2one("stock.location")
    location_dest_id = fields.Many2one("stock.location")

    coa_upload = fields.Binary()
    coa_upload_filename = fields.Char()


class POStockMoveLine(models.Model):
    _inherit = "stock.move.line"

    dyme_transfer_id = fields.Char()

    @api.multi
    def create(self, vals):

        if vals["move_id"]:
            po_line = self.env["stock.move"].browse(vals["move_id"]).purchase_line_id

            if po_line:
                vals["x_lot_id"] = po_line["lot_id"].id
                vals["x_coa_upload"] = po_line["coa_upload"]
                vals["x_coa_upload_filename"] = po_line["coa_upload_filename"]
                vals["location_dest_id"] = po_line["location_dest_id"].id
                vals["location_id"] = po_line["location_id"].id

        return super(POStockMoveLine, self).create(vals)