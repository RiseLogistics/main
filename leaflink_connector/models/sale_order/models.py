# -*- coding: utf-8 -*-

from odoo.addons.queue_job.job import job
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    leaflink_bind_ids = fields.One2many(
        comodel_name="leaflink.sale.order",
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
