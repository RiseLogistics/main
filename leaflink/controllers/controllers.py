# -*- coding: utf-8 -*-

from odoo import http, exceptions
import logging

_logger = logging.getLogger(__name__)

STATE_IDS = {
    "California": 13,
    "Oregon": 40,
    "Washington": 56
}

PAYMENT_TERMS_MAPPING = {
    "COD":      1,
    "Net 14":   2,
    "Net 7":    4,
    "Net 15":   6,
    "Net 30":   7
}


SO_OWNER = 2501
STOCK_LOCATION = 1


class LeaflinkConnector(http.Controller):
    @http.route("/leaflink_so/", auth="public", method=["POST"], type="json", csrf=False, cors="*")
    def index(self, **kw):
        self._auth(http.request.params)

        payload = http.request.params["data"]
        _logger.warning("Creating LeafLink SO for {}".format(payload))

        try:
            so = self._handle_so(payload)
            if not so:
                return {"error": "Active SO Odoo <> LeafLink Sync"}

            _logger.warning("Create/Update SO [%s]" % so.id)
            return {"so_id": so.id, "so_name": so.name}

        except Exception as e:
            _logger.exception("Exception while in /leaflink_so/ [%s]" % e)
            raise exceptions.ValidationError("Unable to handle leaflink_so creation")

    def _handle_so(self, payload):
        _logger.warning("Handling SO for [%s]" % payload["number"])
        so_env = http.request.env["sale.order"].sudo()
        so_record = so_env.search([("leaflink_order_id", "=", payload["number"])])

        # first check if we are updating the SO using the LeafLink client
        if so_record.env.context.get("ll_api", False):
            _logger.warning("SO[%s] being updated by Odoo." % so_record.id)
            return False

        if so_record:
            return self._update_so(so_record, payload)

        return self._create_so(payload, so_env)

    def _update_so(self, so_record, payload):
        partner_rec = self._fetch_partner(payload)
        _logger.warning("Handling SO update for partner[%s]" % partner_rec.id)

        status_handlers = {
            "Accepted": lambda: self._so_confirm(so_record),
            "Completed": lambda: self._so_done(so_record),
            "Rejected": lambda: self._so_cancel(so_record)
        }

        status = payload["status"]
        _logger.warning("[%s] Fetching handler for status %s"
                        % (so_record.id, status))

        handler = status_handlers.get(status)
        res = handler and handler() or "HANDLER_DNE"

        _logger.warning("[%s - %s] handler results --> [%s]"
                        % (so_record.id, status, res))

        default_write = {
            "x_paid": payload["paid"],
            'x_scheduled_delivery_date': payload["ship_date"],
            "x_studio_field_QSmM6": payload["internal_notes"] or None
        }

        payment_term_id = PAYMENT_TERMS_MAPPING.get(payload["payment_term"])
        if payment_term_id:
            default_write["payment_term_id"] = payment_term_id

        so_record.with_context(ll_api=True).write(default_write)
        return so_record

    def _create_so(self, payload, env):
        partner_rec = self._fetch_partner(payload)
        _logger.warning("Handling SO creation for partner[%s]" % partner_rec.id)

        new_so = {
            "x_studio_field_kVKl0": SO_OWNER,  # created by
            "x_invoiced": False,
            "warehouse_id": STOCK_LOCATION,
            "partner_shipping_id": partner_rec.id,
            "partner_invoice_id": partner_rec.id,
            "partner_id": partner_rec.id,
            "validity_date": False,
            "x_cashcollected": False,
            "invoice_status": "no",
            "leaflink_order_id": payload["number"]
        }

        so_rec = env.with_context(ll_api=True).create(new_so)
        self._so_draft(so_rec, payload)
        self._update_so(so_rec, payload)

        return so_rec

    def _so_draft(self, so_rec, payload):
        rec_id = so_rec.id
        _logger.warning("SO[%s] Setting draft order line..." % rec_id)
        if not self._can_update_so(so_rec):
            return False

        order_line_ids = self._build_order_line(payload, so_rec.id)
        work_with_context = so_rec.with_context(ll_api=True)
        work_with_context.action_draft()

        return work_with_context.write({"order_line": [(6, 0, order_line_ids)]})

    def _so_confirm(self, so_rec):
        rec_id = so_rec.id
        _logger.warning("SO[%s] Confirming..." % rec_id)
        if not self._can_update_so(so_rec):
            return False

        return so_rec.with_context(ll_api=True).action_confirm()

    def _so_done(self, so_rec):
        rec_id = so_rec.id
        _logger.warning("SO[%s] Confirming..." % rec_id)

        if so_rec.state in ["done", "cancel"]:
            _logger.warning("SO[%s] Can not cancel order in state [%s]"
                            % (rec_id, so_rec.state))
            return False

        return so_rec.with_context(ll_api=True).action_done()

    def _so_cancel(self, so_rec):
        rec_id = so_rec.id
        _logger.warning("SO[%s] cancelling..." % rec_id)

        if so_rec.state in ["done", "cancel"]:
            _logger.warning("SO[%s] Can not cancel order in state [%s]"
                            % (rec_id, so_rec.state))
            return False

        return so_rec.action_cancel()

    def _build_order_line(self, payload, internal_order_id):
        order_line_env = http.request.env["sale.order.line"].sudo()
        product_env = http.request.env["product.template"].sudo()
        leaflink_order_line = payload["orderedproduct_set"]
        order_line_ids = []

        for line_item in leaflink_order_line:
            _logger.warning("Building Line[%s] for order [%s]"
                            % (line_item, payload["number"]))

            _rec = order_line_env.create({
                "product_id": product_env.search([
                    ("leaflink_external_id", "=", line_item["id"]),
                    ("leaflink_sync_enabled", "=", True)]).product_variant_id.id,

                "order_id": internal_order_id,
                "product_uom_qty": line_item["quantity"],
                "price_unit": float(line_item["ordered_unit_price"]),
                "state": "draft"
            })

            order_line_ids.append(_rec.id)

        return order_line_ids

    def _can_update_so(self, so_rec):
        if so_rec.state in ["done", "cancel", "sale"]:
            _logger.warning("[SO - %s] Can not update SO in [%s]" % (so_rec.id, so_rec.state))
            return False

        return True

    def _fetch_partner(self, payload):
        res_partner_env = http.request.env["res.partner"].sudo()
        external_id = payload["customer"]["id"]
        license_number = payload["customer"]["license_number"]

        partner_rec = res_partner_env.search([("leaflink_external_id", "=", external_id)])

        # fetch partner if external id was previously assigned
        if partner_rec:
            return partner_rec

        # search on license number if no partner with external id exists
        partner_rec = res_partner_env.search([("filter_on", "ilike", license_number)])

        if len(partner_rec) == 1:
            partner_rec.with_context(ll_api=True).write({"leaflink_external_id": external_id})
            return partner_rec

        # create a new partner with the external id if we can't find a valid partner
        customer = payload["customer"]
        _logger.warning("Creating new LeafLink customer %s" % customer)

        partner_rec = res_partner_env.with_context(ll_api=True).create({
            "company_type": "company",
            "name": customer["nickname"] or customer["business_license_name"],
            "x_studio_field_YcCId": customer["business_license_name"],
            "x_studio_field_K2J26": license_number,
            "leaflink_external_id": external_id,
            "email": customer["email"],
            "phone": customer["phone"],
            "street": customer["address"],
            "state_id": STATE_IDS.get(customer["state"], None),
            "city": customer["city"],
            "zip": customer["zipcode"],
            "vat": customer["ein"],
            "website": customer["website"],
            "x_delivery_fee_view": customer["shipping_charge"],
            "x_studio_field_nmITT": customer["delivery_preferences"],
            "x_invoice_notes": customer["description"]
        })

        return partner_rec

    @property
    def _token(self):
        env_params = http.request.env["ir.config_parameter"].sudo()
        return env_params.get_param("leaflink.api.token", False)

    def _auth(self, body):
        try:
            _logger.info("Validating access token")

            if not self._token or (self._token != body["token"]):
                raise exceptions.AccessDenied()

        except KeyError:
            raise exceptions.AccessDenied()

