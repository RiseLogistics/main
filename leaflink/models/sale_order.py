from odoo import models, fields, api
import logging
from ..api_client.client.exceptions import LeafLinkClientRequestError

_logger = logging.getLogger(__name__)


STATE_MAPPING = {
    "done":     ("completed", "complete"),
    "cancel":   ("rejected", "reject"),
    "sale":     ("accepted", "accept")
}

PAYMENT_TERMS_MAPPING = {
    1: "COD",
    2: "Net 14",
    4: "Net 7",
    6: "Net 15",
    7: "Net 30"
}


class LeafLinkSO(models.Model):
    _inherit = ["sale.order",
                "leaflink.base.adapter"]

    _name = "sale.order"
    _external_model = "Orders"

    leaflink_order_id = fields.Char(index=True)

    @property
    @api.multi
    def map_leaflink_so_fields(self):
        ship_date = self.x_scheduled_delivery_date
        default_mapping = {
            "ship_date": ship_date and "%sT12:00:00" % ship_date or None,
            "paid": self.x_paid,
            "internal_notes": self.x_studio_field_QSmM6
        }

        if PAYMENT_TERMS_MAPPING.get(self.payment_term_id.id):
            default_mapping["payment_term"] = PAYMENT_TERMS_MAPPING[self.payment_term_id.id]

        return {k: v for k, v in default_mapping.items() if v}

    @api.multi
    def patch_leaflink_so(self):
        if self.env.context.get("ll_api", False):
            _logger.warning("SO[%s] being updated by SO endpoint." % self.id)
            return False

        try:
            _logger.warning("PATCHING SO[%s] with PARAMS[%s]"
                            % (self.id, self.map_leaflink_so_fields))

            work_with_context = self.with_context(ll_api=True)
            res = work_with_context.leaflink_crud.patch(
                self.leaflink_order_id,
                **self.map_leaflink_so_fields
            ).run().dump_all()

            _state_mapping = STATE_MAPPING.get(self.state)
            if _state_mapping and _state_mapping[0] in res["available_transitions"]:
                self.rpc_leaflink_state(_state_mapping[1])

            work_with_context.set_leaflink_sync_ts()

        except LeafLinkClientRequestError as e:
            _logger.exception("CLIENT ERROR: (%s - %s)" % (e.msg, e.response))
            return False

        except Exception as e:
            _logger.exception("SO ERROR: %s" % e)
            return False

        return True

    @api.multi
    def rpc_leaflink_state(self, set_state):
        try:
            _logger.warning("[%s] Updating order status on LeafLink"
                            " -> %s" % (self.id, set_state))

            self.with_context(ll_api=True).leaflink_crud.rpc_status(
                self.leaflink_order_id,
                status=set_state
            ).run()

        except LeafLinkClientRequestError as e:
            _logger.exception("CLIENT ERROR: (%s - %s)" % (e.msg, e.response))
            return False
