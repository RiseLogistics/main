from odoo.addons.component.core import AbstractComponent, Component
from odoo.addons.component_event import skip_if

import logging

_logger = logging.getLogger(__name__)


class LeafLinkExportListener(AbstractComponent):
    _name = "leaflink.listener.exporter"
    _inherit = "base.event.listener"
    _external_field = "external_id"

    _apply_on = [
        "leaflink.product.template",
        "leaflink.sale.order",
        "leaflink.res.partner",
        "leaflink.product.category",
        "leaflink.manager.api",

        "product.template",
        "sale.order",
        "res.partner"
    ]

    def on_record_create(self, record, fields=None):
        raise NotImplementedError

    def on_record_write(self, record, fields=None):
        raise NotImplementedError

    def valid_binding(self, record):
        return bool(
            (hasattr(record, "leaflink_bind_ids")
                and record.leaflink_bind_ids)

            or (hasattr(record, "odoo_id") and record.enabled)
        )


class LeafLinkBindedExportListener(Component):
    _name = "leaflink.global.listener.exporter"
    _inherit = "leaflink.listener.exporter"
    _apply_on = [
        "product.template",
        "res.partner"
    ]

    @skip_if(lambda self, record, *args, **kwargs:
             self.env.context.get("skip_binding")
             or record.leaflink_bind_ids)
    def on_record_write(self, record, fields=None):
        _logger.warning("ON LL/%s WRITE" % record._name)
        rec_handler = self.env["leaflink.%s" % record._name]

        record.with_context(skip_binding=True)
        work_with_context = rec_handler.with_context(skip_binding=True)
        work_with_context.with_delay().bind_domain_records()

    @skip_if(lambda self, record, *args, **kwargs:
             self.env.context.get("skip_binding")
             or record.leaflink_bind_ids)
    def on_record_create(self, record, fields=None):
        _logger.warning("ON LL/%s CREATE" % record._name)
        rec_handler = self.env["leaflink.%s" % record._name]

        record.with_context(skip_binding=True)
        work_with_context = rec_handler.with_context(skip_binding=True)
        work_with_context.with_delay().bind_domain_records()

