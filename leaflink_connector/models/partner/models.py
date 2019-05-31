# -*- coding: utf-8 -*-

from odoo.addons.queue_job.job import job
from odoo import models, fields, api, _
import logging

from .common import get_license_type, PHONE


_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    leaflink_bind_ids = fields.One2many(
        comodel_name="leaflink.res.partner",
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


class PartnerLeafLinkMapping(models.Model):
    _inherit = "leaflink.res.partner"

    @api.multi
    def map_customer_export(self):
        self.ensure_one()

        customer_info = {}

        customer_info["external_id"] = self.odoo_id.id
        customer_info["website"] = self.map_website
        customer_info["name"] = self.odoo_id.name
        customer_info["business_license_name"] = self.odoo_id.name
        customer_info["dba"] = self.map_legal_name
        customer_info["address"] = self.street
        customer_info["city"] = self.city or None
        customer_info["zipcode"] = self.zip or None
        customer_info["state"] = self.state_id and self.state_id.name or None
        customer_info["email"] = self.map_email
        customer_info["phone"] = self.map_phone

        customer_info.update(self.map_license_type)
        customer_info.update(self.map_ein)
        customer_info.update(self.map_delivery_fees)
        customer_info.update(self.map_notes_and_preferences)
        # customer_info.update(self.map_service_zone)

        return customer_info

    @property
    @api.model
    def map_website(self):
        if self.website:
            return self.website.replace(" ", "")
        return None

    @property
    @api.model
    def map_email(self):
        if self.odoo_id.email:
            emails = self.odoo_id.email.split(";")
            if len(emails) > 1:
                return emails.pop()

            return None

    @property
    @api.model
    def map_license_type(self):
        tmp_license = self.x_studio_field_K2J26

        license_type = get_license_type(tmp_license)
        if license_type and license_type["type"]:
            return {
                "license": {
                    "license_number": license_type["number"],
                    "license_type": {"id": license_type["type"]["id"]}
                }
            }

        return {}

    @property
    @api.model
    def map_legal_name(self):
        return self.odoo_id.x_studio_field_YcCId

    @property
    @api.model
    def map_delivery_fees(self):
        return {
            "shipping_charge": self.x_studio_field_Pb8Oc or None
        }

    @property
    @api.model
    def map_phone(self):
        return self.phone and PHONE(self.phone) or None

    @property
    @api.model
    def map_notes_and_preferences(self):
        delivery_contact = ""
        if self.x_studio_field_4z3lM:
            delivery_contact += "Deliver To: %s -- " % self.x_studio_field_4z3lM

        if self.x_studio_field_m82Hm:
            delivery_contact += " Phone: %s" % self.x_studio_field_m82Hm

        if self.x_studio_field_nmlTT:
            delivery_contact += " Notes: %s" % self.x_studio_field_nmlTT

        return {
            "delivery_preferences": self.x_studio_field_4z3lM or "",
            "notes": None,
            "nickname": self.odoo_id.name
        }

    @property
    @api.model
    def map_ein(self):
        return {
           "EIN": self.vat or None
        }
