# -*- coding: utf-8 -*-

from odoo.addons.queue_job.job import job
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

STOCK_LOCATION_ID = 18
VENDOR_FIELD = "x_studio_field_jbJcD"
BRAND_FIELD = "x_studio_field_pHWCf"


PRODUCT_STATE_CHOICES = [
    ("Available",)   * 2,
    ("Archived",)    * 2,
    ("Sample",)      * 2,
    ("Backorder",)   * 2,
    ("Internal",)    * 2,
    ("Unavailable",) * 2
]


UOM_MAPPING = {
    "Case(s)"   : "Case",
    "Oz"        : "Ounce",
    "oz(s)"     : "Ounce",
    "Unit(s)"   : "Unit",
    "g"         : "Gram",
    "kg"        : "Kilogram",
    "lb(s)"     : "Pound"
}


STRAIN_TYPE_MAPPING = {
    "CBD": "High CBD",
    "HYBRID": "Hybrid",
    "SATIVA": "Sativa",
    "INDICA": "Indica",
    "N/A": "N/A",
    "STRAIN SPECIFIC": "N/A",
}


class ProductTemplate(models.Model):
    _inherit = "product.template"

    leaflink_bind_ids = fields.One2many(
        comodel_name="leaflink.product.template",
        inverse_name="odoo_id",
        string="LeafLink Bindings",
    )

    @job(default_channel="root.leaflink")
    @api.multi
    def export_record(self, backend_record=None, fields=None):
        _logger.warning("Proxy export record [%s - %s]" % (self._name, self.id))

        self.ensure_one()

        for bind_id in self.leaflink_bind_ids:
            with bind_id.backend_id.work_on(bind_id._name) as work:
                exporter = work.component(usage="record.exporter")
                return exporter.run(bind_id, fields)


class ProductLeafLinkMapping(models.Model):
    _inherit = "leaflink.product.template"

    is_medical_line_item = fields.Boolean(default=False, string="Medical Item")
    can_sample = fields.Boolean(default=False, string="Available for sample")
    featured = fields.Boolean(default=False, string="Featured on LeafLink")
    tagline = fields.Char(default=None, string="Tag line to display when featured")
    allow_fractional_quantities = fields.Boolean(default=False)
    listing_state = fields.Selection(
        PRODUCT_STATE_CHOICES,
        default="Internal"
    )

    @api.multi
    def map_product_export(self):
        self.ensure_one()

        product_info = dict(name=self.odoo_id.name)
        product_info["description"] = self.odoo_id.description or " - "
        product_info.update(self.map_sku)
        product_info.update(self.map_quantites)
        product_info.update(self.map_cost)
        product_info.update(self.map_leaflink_fields)
        product_info.update(self.map_unit_values)
        product_info.update(self.map_strain_data)

        return product_info

    @property
    @api.model
    def map_sku(self):
        return {"sku": self.odoo_id.default_code or None}

    @property
    @api.model
    def map_quantites(self):
        stock = self.odoo_id.product_variant_id.with_context(location_id=STOCK_LOCATION_ID)

        real_qty = stock.qty_available - stock.outgoing_qty
        is_empty_stock = real_qty <= 0

        return {
            "quantity": stock.qty_available,
            "reserved_qty": stock.outgoing_qty,
            "minimum_order": is_empty_stock and 0 or 1,
            "maximum_order": is_empty_stock and 0 or real_qty,
            "unit_multiplier": 1,
            "listing_state": is_empty_stock and "Unavailable" or self.listing_state
        }

    @property
    @api.model
    def map_cost(self):
        return {
            "wholesale_price": self.odoo_id.list_price,
            "list_price": self.odoo_id.list_price,
            "retail_price": self.odoo_id.list_price,
            "sale_price": self.odoo_id.list_price
        }

    @property
    @api.model
    def map_leaflink_fields(self):
        return {
            "is_medical_line_item": self.is_medical_line_item,
            "AVAILABLE_FOR_SAMPLES": self.can_sample,
            "featured": self.featured,
            "tagline": self.featured and self.tagline or None,
            "inventory_management": "Managed",
            "brand": self.this_brand.external_id,
            "manufacturer": self.this_brand.internal_vendor_id.id,
            "seller": self.this_brand.api_backend.external_id
        }

    @property
    @api.model
    def this_brand(self):
        my_brand = self.env["leaflink.manager.brand"].search([
            ("internal_brand_id", "=", self.odoo_id[BRAND_FIELD].id),
            ("internal_vendor_id", "=", self.odoo_id[VENDOR_FIELD].id)
        ], limit=1)

        return my_brand

    @property
    @api.model
    def map_unit_values(self):
        leaflink_uom_id = None
        unit_multiplier = 1

        if self.odoo_id.uom_id:
            leaflink_uom_id = UOM_MAPPING.get(self.odoo_id.uom_id.name)

        if leaflink_uom_id == "Case":
            unit_multiplier = self.odoo_id.x_quantity_per_case or 1

        return {
            "category": self.categ_id.leaflink_bind_ids.external_id,
            "sell_in_unit_of_measure": None,
            "unit_denomination": 1,
            "unit_of_measure": leaflink_uom_id,
            "uni_multiplier": unit_multiplier,
            "allow_fractional_quantities": False
        }

    @property
    @api.model
    def map_strain_data(self):
        return {"strain_classification":
            STRAIN_TYPE_MAPPING.get(
                self.odoo_id.x_studio_field_52vaT.display_name, "N/A")
        }
