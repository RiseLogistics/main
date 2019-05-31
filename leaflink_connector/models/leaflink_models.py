# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

VENDOR_FIELD = "x_studio_field_jbJcD"
BRAND_FIELD = "x_studio_field_pHWCf"
PRODUCTS_STOCK_LOCATION_ID = 18


class LeafLinkPartner(models.Model):
    _name = "leaflink.res.partner"
    _inherits = {"res.partner": "odoo_id"}
    _inherit = "leaflink.binding.exporter"

    name = fields.Char()

    odoo_id = fields.Many2one(comodel_name="res.partner",
                              string="Partner",
                              required=True,
                              ondelete="restrict")

    def _binding_domain(self, brand, vendor):
        return [
            ("active", "=", True),
            ("is_company", "=", 1),
            ("parent_id", "=", False),  # import parent, then contacts
            ("x_studio_field_K2J26", "!=", False),  # license num
            ("leaflink_bind_ids", "=", False),
            ("zip", "!=", False),
            ("name", "!=", False),
            ("employee", "=", False),
            ("customer", "=", True),
            ("id", ">", 2),  # skip first two admins
            ("x_studio_field_P4UbZ", "!=", False)  # make sure region is set
        ]

    def skip_record_binding(self, record):
        if record.leaflink_bind_ids:
            return True


class LeafLinkSaleOrder(models.Model):
    _name = "leaflink.sale.order"
    _inherits = {"sale.order": "odoo_id"}
    _inherit = "leaflink.binding.exporter"

    name = fields.Char()

    odoo_id = fields.Many2one(comodel_name="sale.order",
                              string="Sale Order",
                              required=True,
                              ondelete="restrict")

    @api.multi
    def handle_so(self, so_object):
        _logger.warning("pass to adapter")


class LeafLinkProduct(models.Model):
    _name = "leaflink.product.template"
    _inherits = {"product.template": "odoo_id"}
    _inherit = "leaflink.binding.exporter"

    name = fields.Char()

    odoo_id = fields.Many2one(comodel_name="product.template",
                              string="Product",
                              required=True,
                              ondelete="restrict")

    def _binding_domain(self, brand, vendor):
        return [
            (BRAND_FIELD, "=", brand.id),
            (VENDOR_FIELD, "=", vendor.id),
            ("leaflink_bind_ids", "=", False),
            ("type", "in", ["product"]),
            ("sale_ok", "=", 1),
            ("categ_id.leaflink_bind_ids", "!=", False),
            ("active", "=", True),
            ("tracking", "=", "lot"),
            ("x_retail_ready", "=", True),
            ("x_studio_field_52vaT", "!=", False)
        ]

    def skip_record_binding(self, record):
        if (record.is_product_variant or
                not record.product_variant_id):
            return True

        variant_id = record.product_variant_id
        stock_locations = self.env["stock.quant"].search([
            ("product_id", "=", variant_id.id),
            ("location_id", "=", PRODUCTS_STOCK_LOCATION_ID)
        ])

        if not stock_locations:
            return True

        stock = variant_id.with_context(
            location_id=PRODUCTS_STOCK_LOCATION_ID
        )

        if (stock.qty_available - stock.outgoing_qty) <= 0:
            return True

        return False

    image_1_id = fields.Binary(string="1/5", store=True, attachment=True, readonly=False)
    image_2_id = fields.Binary(string="2/5", store=True, attachment=True, readonly=False)
    image_3_id = fields.Binary(string="3/5", store=True, attachment=True, readonly=False)
    image_4_id = fields.Binary(string="4/5", store=True, attachment=True, readonly=False)
    image_5_id = fields.Binary(string="5/5", store=True, attachment=True, readonly=False)


class LeafLinkCategory(models.Model):
    _name = "leaflink.product.category"
    _inherit = "leaflink.binding.exporter"

    name = fields.Char()
    slug = fields.Char()
    description = fields.Char()

    odoo_id = fields.Many2one("product.category",
                              string="Product Category",
                              required=True)

    _sql_constraints = [
        ("leaflink_uniq", "unique(backend_id, external_id, name)",
         "A binding already exists with the same LeafLink ID."),
    ]


class StockCategory(models.Model):
    _inherit = "product.category"

    leaflink_bind_ids = fields.One2many(
        comodel_name="leaflink.product.category",
        inverse_name="odoo_id",
        string="LeafLink Bindings",
    )


class LeafLinkSalesRep(models.Model):
    _name = "leaflink.sales.rep"
    _inherit = "leaflink.binding.exporter"

    odoo_sales_rep = fields.Many2one(
        "res.users",
        string="Sales Rep",
        required=True
    )

