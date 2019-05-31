
# -*- coding: utf-8 -*-
import odoo
from odoo.addons.component.core import AbstractComponent
import logging

_logger = logging.getLogger(__name__)


class LeafLinkBaseExporter(AbstractComponent):

    _name = "leaflink.exporter"
    _inherit = ["base.exporter", "base.leaflink.connector"]
    _usage = "record.exporter"

    def __init__(self, working_context):
        super(LeafLinkBaseExporter, self).__init__(working_context)
        self.binding = None
        self.external_id = None

    def _export(self, binder, *args, **kwargs):
        if not self.external_id:
            return self._run_create(binder, *args, **kwargs)

        return self._run_patch(binder, *args, **kwargs)

    def run(self, binding, *args, **kwargs):
        self.binding = binding

        self.external_id = self.binder.to_external(self.binding)
        self._lock()

        result = self._export(binding, args, kwargs)

        self.binder.bind(self.external_id, self.binding)

        if not odoo.tools.config["test_enable"]:
            self.env.cr.commit() 
            
        self._after_export()
        return result

    def _run_create(self, binding=None, *args, **kwargs):
        _logger.warning("_run_create not implemented")
        return None

    def _run_patch(self, binding=None, *args, **kwargs):
        _logger.warning("_run_patch not implemented")
        return None

    def _after_export(self):
        _logger.warning("_after_export not implemented")

    def _lock(self):
        lock_name = "export({}, {}, {})".format(
            self.binding.odoo_id._name,
            self.binding.odoo_id.id,
            self.binding.name,
        )

        self.advisory_lock_or_retry(lock_name, retry_seconds=2)
