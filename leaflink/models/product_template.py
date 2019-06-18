from odoo import models, fields, api
import logging

from ..api_client.client.exceptions import LeafLinkClientRequestError

_logger = logging.getLogger(__name__)

STOCK_LOCATION_ID = 15


class LeafLinkProductTemplate(models.Model):
    _inherit = ["product.template",
                "leaflink.base.adapter"]

    _name = "product.template"
    _external_model = "Products"

    @property
    @api.multi
    def map_quantites(self):
        self.ensure_one()

        stock = self.product_variant_id.with_context(location_id=STOCK_LOCATION_ID)
        real_qty = stock.qty_available - stock.outgoing_qty

        return {
            "quantity": real_qty > 0 and real_qty or 0,
            "minimum_order": 1,
            "maximum_order": real_qty > 0 and real_qty or 0,
        }

    @api.multi
    def patch_leaflink_product(self):
        for record in self:
            try:
                _logger.warning("Updating Product[%s] inventory using [%s]"
                                % (record.id, record.map_quantites))

                work_with_context = record.with_context(ll_api=True)
                work_with_context.leaflink_crud.patch(
                    record.leaflink_external_id,
                    **record.map_quantites
                ).run()
                work_with_context.set_leaflink_sync_ts()

            except LeafLinkClientRequestError as e:
                _logger.exception("CLIENT ERROR: (%s - %s)" % (e.msg, e.response))
                continue

            except Exception as e:
                _logger.exception("ERR: %s" % e)
                continue

        return True


class LeafLinkProduct(models.Model):
    _inherit = "stock.quant"
    _name = "stock.quant"

    @api.multi
    @api.constrains("quantity", "reserved_quantity", "location_id", "lot_id", "product_id")
    def update_product(self):
        for record in self:
            prod_tmpl = record.product_id.product_tmpl_id
            if prod_tmpl.leaflink_external_id and prod_tmpl.leaflink_sync_enabled:
                _logger.warning("Updating %s" % record.product_id.id)
                prod_with_context = record.with_context(ll_api=True).product_id
                prod_with_context.product_tmpl_id.patch_leaflink_product()
