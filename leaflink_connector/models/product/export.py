from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if

import logging


_logger = logging.getLogger(__name__)


class ProductExportListener(Component):
    _name = "leaflink.product.template.listener.exporter"
    _inherit = "leaflink.listener.exporter"
    _apply_on = [
        "product.template",
        "leaflink.product.template"
    ]

    @skip_if(lambda self, record, *args, **kwargs:
             self.env.context.get('connector_no_export')
             or not self.valid_binding(record))
    def on_record_write(self, record, fields=None):
        _logger.warning("ON LL/product.template WRITE %s" % record)
        record.with_delay().export_record(record, fields=fields)

    @skip_if(lambda self, record, *args, **kwargs:
             self.env.context.get('connector_no_export')
             or not self.valid_binding(record))
    def on_record_create(self, record, fields=None):
        _logger.warning("ON LL/product.template CREATE %s" % record)
        record.with_delay().export_record(record, fields=fields)


class ProductExportHandler(Component):
    _name = "leaflink.product.template.exporter"
    _inherit = "leaflink.exporter"
    _apply_on = [
        "product.template",
        "leaflink.product.template"
    ]

    def _run_create(self, binding=None, *args, **kwargs):
        _logger.warning("Running record export [%s]" % self._name)

        adapter = self.backend_adapter
        backend_id = self.binding.backend_id

        api_client = adapter.config_api_client(backend_id)

        export_payload = self.binding.map_product_export()
        res = api_client.create(**export_payload).run()
        res_json = res.dump()
        _logger.warning(res_json)

        self.external_id = res_json["id"]

        return True

    def _run_patch(self, binding=None, *args, **kwargs):
        _logger.warning("Running record export [%s]" % self._name)

        adapter = self.backend_adapter
        backend_id = self.binding.backend_id

        api_client = adapter.config_api_client(backend_id)

        export_payload = self.binding.map_product_export()
        _logger.warning(export_payload)

        res = api_client.patch(self.external_id, **export_payload).run()
        res_json = res.dump()
        _logger.warning(res_json)

        self.external_id = res_json["id"]

        return True
