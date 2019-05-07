# -*- coding: utf-8 -*-

import logging
from odoo import http, exceptions
import requests
import datetime
import base64

from .env import ODOO_TOKEN

log = logging.getLogger(__name__)


class ExpressPOController(http.Controller):
    @http.route("/po/new/", auth="public", method=["POST"], type="json", csrf=False, cors="*")
    def index(self, **kw):
        self._auth(http.request.params)

        payload = http.request.params["data"]

        log.debug("Creating PO order for {}".format(payload))
        po = http.request.env["purchase.order"].sudo()

        try:
            return self._handle_po_creation(po, payload)

        except Exception as e:
            log.exception("Exception while in /po/new [%s]" % e)
            raise exceptions.ValidationError("Unable to handle PO creation")

    def _handle_po_creation(self, po, payload):

        try:

            po_id = po.create({
                "name": "New",
                "partner_id": payload["source"]["id"],
                "date_order": payload["pickup_date"],
                "picking_type_id": payload["pick_type_id"],
                "state": "draft",
                "dyme_transfer_id": payload["transfer_id"],
                "location_dest_id": payload["location_dest_id"],
                "location_id": payload["location_id"],
            })

            po_line = http.request.env["purchase.order.line"].sudo()

            parsed_line_items = []
            for item in payload["line_items"]:
                product = item["product"]

                line_id = po_line.create({
                    "product_id": product["id"],
                    "name": product["name"],
                    "price_unit": item["price"],
                    "product_qty": item["quantity"],
                    "product_uom": item["unit"]["id"],
                    "coa_upload_filename": "{product} {batch} Certifcate of Analysis.pdf"
                                           .format(product=product["id"], batch=item["batch_number"]),

                    "coa_upload": self._coa_url_to_base64(item["coa"]),
                    "date_planned": payload["scheduled_date"],
                    "date_order": payload["pickup_date"],
                    "order_id": po_id.id,
                    "location_dest_id": payload["location_dest_id"],
                    "location_id": payload["location_id"],
                    "dyme_transfer_id": payload["transfer_id"],
                    "picking_type_id": payload["pick_type_id"],
                    "lot_id": self._create_batch(item)
                })

                parsed_line_items.append(line_id.id)

            po_id.write({"order_line": [(6, 0, parsed_line_items)]})
            po_id.button_confirm()

        except Exception as e:
            log.exception(e)
            raise exceptions.ValidationError("Error creating PO object {}".format(str(e)))

        return po_id.id

    def _create_batch(self, item):
        log.info("Creating batch for %s" % item["product"])

        lots = http.request.env["stock.production.lot"].sudo()

        lot_record = lots.create({
            "name": item["batch_number"],
            "product_id": item["product"]["id"],
            "product_uom_id": item["unit"]["id"]
        })

        return lot_record.id

    def _coa_url_to_base64(self, url):
        data = None

        try:
            data = base64.b64encode(requests.get(url.strip()).content).replace(b"\n", b"")

        except Exception as e:
            log.warn("There was a problem requesting the COA from URL %s" % url)
            log.exception(e)

        return data

    def _auth(self, body):
        try:
            log.info("Validating BCC access token")

            if ODOO_TOKEN != body["token"]:
                raise exceptions.AccessDenied("Invalid access token")

        except KeyError:
            raise exceptions.AccessDenied("Must set token in request body")
