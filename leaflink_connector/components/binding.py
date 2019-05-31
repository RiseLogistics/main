# -*- coding: utf-8 -*-

from odoo.addons.queue_job.job import job
from odoo import api, models, fields
import logging


_logger = logging.getLogger(__name__)

STATES = [("pending", "Pending Sync"),
          ("started", "Started Sync"),
          ("synced", "Synced"),
          ("fail", "Sync Failed")]


class LeafLinkExportBinding(models.AbstractModel):
    _name = "leaflink.binding.exporter"
    _inherit = "external.binding"
    _description = "LeafLink Binding (abstract)"
    _rec_name = "backend_id"

    backend_id = fields.Many2one(
        comodel_name="leaflink.manager.api",
        string="LeafLink API backend",
        required=True,
        ondelete="restrict"
    )

    status = fields.Selection(
        STATES,
        readonly=True,
        required=True,
        index=True,
        default="pending",
        string="Sync State"
    )

    external_id = fields.Char(string="ID on LeafLink")
    sync_date = fields.Datetime(string="Last Sync TS")
    created_at = fields.Date("LeafLink Creation Date")
    updated_at = fields.Date("LeafLink Update Date")
    enabled = fields.Boolean(required=True, default=True)

    _sql_constraints = [
        ("leaflink_uniq", "unique(backend_id, external_id)",
         "A binding already exists with the same LeafLink ID."),
    ]

    @job(default_channel="root.leaflink")
    @api.multi
    def export_record(self, backend_record=None, fields=None):
        _logger.warning("Exporting record [%s - %s]" % (self._name, self.id))

        self.ensure_one()
        with self.backend_id.work_on(self._name) as work:
            exporter = work.component(usage="record.exporter")
            return exporter.run(self, fields)

    @job(default_channel="root.leaflink")
    def export_delete_record(self, backend, external_id):
        with backend.work_on(self._name) as work:
            deleter = work.component(usage="record.exporter.deleter")
            return deleter.run(external_id)

    @job(default_channel="root.leaflink")
    @api.multi
    def bind_domain_records(self):
        _logger.warning("Binding records based on leaflink.manager.brand")

        brands = self.env["leaflink.manager.brand"].search([])
        ids = []

        for brand in brands:
            ids += self._bind_leaflink_record(
                brand.api_backend,
                brand.internal_brand_id,
                brand.internal_vendor_id
            )

    @api.multi
    def _bind_leaflink_record(self, backend, brand_id, vendor_id):
        target_model = self._name.replace("leaflink.", "")
        _domain = self._binding_domain(brand_id, vendor_id)
        ids = []

        for record in self.env[target_model].search(_domain):

            if self.skip_record_binding(record):
                continue

            _id = self.with_context(skip_binding=True).create({
                "status": "pending",
                "name": "[%s] LeafLink Binding" % record.id,
                "odoo_id": record.id,
                "backend_id": backend.id
            })

            ids.append(_id)

        return ids

    def skip_record_binding(self, record):
        return False

    def _binding_domain(self, brand_id, vendor_id):
        raise NotImplementedError
