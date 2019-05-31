from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if

import logging


_logger = logging.getLogger(__name__)


class LeafLinkBrandExportListener(Component):
    _name = "leaflink.manager.brand.listener.exporter"
    _inherit = "leaflink.listener.exporter"
    _apply_on = [
        "leaflink.manager.brand"
    ]

    @skip_if(lambda self, record, *args, **kwargs:
             self.env.context.get("connector_no_export"))
    def on_record_write(self, record, fields=None):
        _logger.warning("ON LL.brand WRITE %s" % record)
        work_context = record.with_context(skip_binding=True)
        work_context.with_delay().bind_brand_products()

    @skip_if(lambda self, record, *args, **kwargs:
             self.env.context.get("connector_no_export"))
    def on_record_create(self, record, fields=None):
        _logger.warning("ON LL.brand CREATE %s" % record)

        work_context = record.with_context(skip_binding=True)
        work_context.with_delay().bind_brand_products()


class LeafLinkBrandExportHandler(Component):
    _name = "leaflink.brand.exporter"
    _inherit = "leaflink.exporter"
    _apply_on = [
        "leaflink.manager.brand"
    ]

    def _run(self, args, **kwargs):
        _logger.warning("a %s" % args)
        _logger.warning("kw %s" % kwargs)
