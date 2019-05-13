# -*- coding: utf-8 -*-

import logging
from odoo import http, exceptions
import requests
import datetime

from .. import env

log = logging.getLogger(__name__)


class Bcc(http.Controller):
    @http.route('/bcc/manage/', auth='public', method=["POST"], type="json", csrf=False, cors="*")
    def index(self, **kw):
        log.info("Handling BCC license status")
        self._auth(http.request.params)

        payload = http.request.params["data"]

        log.debug("Storing BCC data for {}".format(payload))
        bcc = http.request.env["bcc.license"].sudo()

        try:
            if isinstance(payload, list):
                return self._load_list(bcc, payload)

            else:
                return self._load_single(bcc, payload)

        except Exception as e:
            log.exception("Exception while in /bcc/manage [%s]" % e)
            raise exceptions.ValidationError("Unable to handle BCC updates")

    @http.route("/bcc/meta/<int:partner_id>", auth='public', method=["POST"],
                type="json", csrf=False, cors="*")
    def partner_metadata(self, partner_id, token=None):
        log.info("Handling BCC license status")
        self._auth(http.request.params)

        partner_model = http.request.env["res.partner"].sudo()
        partner = partner_model.browse(partner_id)

        _res = {
            "can_purchase_so": partner.is_bcc_valid(),
            "licenses": []
        }

        for lic_rec in partner.bcc_license_data:
            _res["licenses"].append({
                "license_number": lic_rec.license_number,
                "license_status": lic_rec.status,
                "license_valid": lic_rec.validate_license_status(alert=False),
                "license_issue_date": lic_rec.issue_date,
                "license_expiration_date": lic_rec.expiration_date,
                "type": lic_rec.license_type,
                "allowed_use_type": lic_rec.allowed_use_type
            })

        return _res

    def _load_list(self, bcc, payload):
        modified_records = []

        for lic in payload:
            modified_records.append(self._load_single(bcc, lic))

        return modified_records

    def _load_single(self, bcc, payload):
        parent = bcc.search([("license_number", "=", payload["license_number"])])
        partner = http.request.env["res.partner"].sudo()

        try:
            parsed_payload = {
                "business_owner": payload["business_owner"],
                "business_contact_information": payload["business_contact_information"],
                "business_structure": payload["business_structure"],
                "premise_address": payload["premise_address"],
                "issue_date": payload["issue_date"],
                "expiration_date": payload["expiration_date"],
                "activities": payload["activities"],
                "license_number": payload["license_number"],
                "license_type": payload["license_type"],
                "allowed_use_type": payload["allowed_use_type"],
                "status": payload["status"],
                "partner_id": [(6, 0, self._check_partners_for_license(partner, payload))]
            }

        except KeyError as e:
            raise exceptions.MissingError("Missing update params [{}]".format(e))

        try:
            if parent:
                parent.write(parsed_payload)
                rec = parent

            else:
                rec = bcc.create(parsed_payload)

        except Exception as e:
            raise exceptions.ValidationError("Error creating object {}".format(e))

        return rec.id

    def _check_partners_for_license(self, partner, pl):
        recs = partner.search([("filter_on", "ilike", pl["license_number"])])

        today_date = datetime.datetime.today()
        expiration_date = datetime.datetime.strptime(pl["expiration_date"], "%m/%d/%Y")
        expires_in = (expiration_date - today_date).days

        if pl["status"] and pl["status"].upper() != "ACTIVE" or expires_in <= 0:
            for rec in recs:
                log.warn("Found expired License %s for %s"
                         % (pl["license_number"], partner.id))

                self._trigger_exp_license_alert(rec, pl)

        if 14 >= expires_in > 0 and pl["status"] and pl["status"].upper() == "ACTIVE":
            for rec in recs:
                log.warn("Found 2-week License expiration %s for %s"
                         % (pl["license_number"], partner.id))

                self._trigger_exp_license_alert(rec, pl, warn=True)

        return recs.ids

    def _trigger_exp_license_alert(self, partner, payload, warn=False):
        log.warn("Alerting[%s] - %s - %s"
                 % (payload["license_type"], partner.name, partner.id))

        res = requests.post(env.ALERT_ENDPOINT, json={
            "license_number": payload["license_number"],
            "status": payload["status"],
            "issue_date": payload["issue_date"],
            "license_type": payload["license_type"],
            "activity": payload["activities"],
            "expiration_date": payload["expiration_date"],
            "partner": "%s - %s" % (partner.name, partner.id),
            "warning_2weeks": warn
        })

        log.warn("Alerting[%s] - RESPONSE_STATUS[%s]" % (payload["license_type"], res.status_code))

    def _auth(self, body):
        try:
            log.info("Validating BCC access token")

            if env.TOKEN != body["token"]:
                raise exceptions.AccessDenied("Invalid access token")

        except KeyError:
            raise exceptions.AccessDenied("Must set token in request body")
