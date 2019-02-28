from odoo import models, fields, api, _
from odoo.exceptions import UserError


import logging
_logger = logging.getLogger(__name__)


class ProductVendorUpdateWizard(models.TransientModel):
    _name = "product.vendor.update.wizard"

    product_tmp_ids = fields.Many2many("product.template", string="Products")

    VENDOR = "x_studio_field_jbJcD"
    new_vendor = fields.Many2one("res.partner", string="New Vendor")

    BRAND = "x_studio_field_pHWCf"
    new_brand = fields.Many2one("x_brand", string="New Brand")

    PIN = "7700"
    pin = fields.Char("PIN")

    @api.model
    def default_get(self, field_names):
        defaults = super(ProductVendorUpdateWizard,
                         self).default_get(field_names)

        defaults["product_tmp_ids"] = self.env.context["active_ids"]
        return defaults

    @api.multi
    def process_update(self):
        self.ensure_one()

        if self.pin != self.PIN:
            self._error("Invalid PIN")

        update_vals = {}
        if not len(self.new_vendor):
            self._error("Invalid update, must select a new vendor.")

        update_vals[self.VENDOR] = self.new_vendor.id

        if self.new_brand:
            update_vals[self.BRAND] = self.new_brand.id

        self.product_tmp_ids.write(update_vals)

        return True

    def _error(self, msg):
        """A method wrapper for returning warning and error messages"""
        raise UserError(_(msg))
