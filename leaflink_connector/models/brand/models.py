# -*- coding: utf-8 -*-

from odoo.addons.queue_job.job import job
from odoo import models, api
import logging


_logger = logging.getLogger(__name__)

VENDOR_FIELD = "x_studio_field_jbJcD"
BRAND_FIELD = "x_studio_field_pHWCf"


class LeafLinkBrand(models.Model):
    _inherit = "leaflink.manager.brand"

    @job(default_channel="root.leaflink")
    @api.model
    def bind_brand_products(self):
        _logger.warning("Exporting internal brand products")

        rec_model = self.env["leaflink.product.template"]
        return rec_model.bind_domain_records()
