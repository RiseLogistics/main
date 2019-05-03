# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import requests
import logging
import datetime

from .. import env

log = logging.getLogger(__name__)


STATES = [
    ("Pending", "Pending BCC Status Update"),
    ("Active", "Active"),
    ("Expired", "Expired"),
    ("Revoked", "Revoked"),
    ("Canceled", "Canceled"),
    ("Suspended", "Suspended"),
    ("Surrendered", "Surrendered"),
    ("Military License Inactive", "Military - License Inactive"),
    ("Delinquent", "Delinquent"),
    ("Family Support Suspension", "Family Support Suspension"),
    ("FTB Suspension", "FTB Suspension"),
    ("Error", "Error"),
    ("Other", "Other")
]


LICENSE_USE_TYPES = [
    ("Pending", "Pending BCC Status Update"),
    ("Adult-Use", "Adult-Use"),
    ("Medicinal", "Medicinal"),
    ("BOTH", "Adult/Medicinal"),
    ("N/A", "N/A")
]


BUSINESS_STRUCTURES = [
    ("Pending", "Pending BCC Status Update"),
    ("Corporation", "Corporation"),
    ("Limited Liability Company", "Limited Liability Company"),
    ("Sole Proprietorship", "Sole Proprietorship"),
    ("General Partnership", "General Partnership")
]


class BCCLicenseModel(models.Model):
    _name = 'bcc.license'
    _description = "BCC License Status"

    _sql_constraints = [
        ("license_number", "unique (license_number)", "Duplicate License Number!")]
    
    business_owner = fields.Char(default="TBD", ondelete="restrict")
    business_contact_information = fields.Char(
        default="TBD",
        ondelete="restrict",
        string="Business Contact Information"
    )

    business_structure = fields.Char(default="Pending")
    premise_address = fields.Char(ondelete="restrict")

    issue_date = fields.Date(index=True, ondelete="restrict")
    expiration_date = fields.Date(index=True, ondelete="restrict")

    activities = fields.Char(ondelete="restrict")
    license_number = fields.Char(index=True, ondelete="restrict", unique=True)
    license_type = fields.Char(ondelete="restrict", index=True)

    allowed_use_type = fields.Selection(
        LICENSE_USE_TYPES,
        default="Pending",
        ondelete="restrict",
        index=True,
        string="Adult-Use/Medicinal"
    )

    status = fields.Selection(
        STATES,
        index=True,
        default="Pending",
        ondelete="restrict"
    )

    filter_on = fields.Char(
        string="Filter on license",
        compute='_compute_filter_field',
        search='_search_filter_field'
    )

    partner_id = fields.Many2many("res.partner")

    @api.depends('expiration_date')
    def _expiration_date_format(self):
        for record in self:
            record.name = fields.Date.from_string(
                record.expiration_date).strftime("%m/%d/%Y")

    @api.depends('issue_date')
    def _issue_date_format(self):
        for record in self:
            record.name = fields.Date.from_string(
                record.issue_date).strftime("%m/%d/%Y")

    def name_get(self):
        return {"name": "{0} - {1} - EXP: {2}".format(
            self.license_number,
            self.license_type,
            self.expiration_date)}

    @api.multi
    def validate_license_status(self):
        log.warn("Alerting Expired License [%s]" % self.license_type)

        today_date = datetime.datetime.today()
        expires_soon = 14 >= (self.expiration_date - today_date).days > 0

        if self.status.upper() != "ACTIVE" or expires_soon:
            for partner in self.partner_id:
                res = requests.post(env.ALERT_ENDPOINT, json={
                    "license_number": self.license_number,
                    "status": self.status,
                    "issue_date": self.issue_date,
                    "license_type": self.license_type,
                    "activity": self.activities,
                    "expiration_date": self.expiration_date,
                    "partner": "%s - %s" % (partner.name, partner.id),
                    "warning_2weeks": self.status.upper() == "ACTIVE" and expires_soon
            })

                log.warn("Alerting Expired License[%s] - RESPONSE_STATUS[%s]"
                         % (self.license_type, res.status_code))

    @api.multi
    @api.depends()
    def _compute_filter_field(self):
        pass

    def _search_filter_field(self, operator, value):
        records = self.search([])
        ids = []
        if operator == 'ilike':
            ids = records.filtered(
                lambda r: r.license_number in value).mapped('id')

        return [('id', 'in', ids)]


class ResPartner(models.Model):
    _inherit = "res.partner"

    bcc_license_data = fields.Many2many("bcc.license")
    can_place_so = fields.Boolean(default=False)

    filter_on = fields.Char(
        string="Filter on license",
        compute='_compute_filter_field',
        search='_search_filter_field'
    )

    @api.multi
    def write(self, vals):
        # x_studio_field_K2J26 == temp license number
        lic_recs = self.onchange_license_number(
            vals.get("x_studio_field_K2J26", self.x_studio_field_K2J26))

        if lic_recs:
            vals["bcc_license_data"] = [(6, 0, lic_recs)]

        else:
            vals["bcc_license_data"] = [(5,)]

        return super(ResPartner, self).write(vals)

    @api.multi
    def onchange_license_number(self, license_number):
        if not license_number:
            log.warn("License number not set for %s - %s" % (self.name, self.id))
            return False

        lic_rec = self.env["bcc.license"].search(
            [("filter_on", "ilike", "%{}%".format(license_number))])

        self._unlink_licenses()

        # for rec in lic_rec:
        #     rec.validate_license_status()

        return lic_rec.ids

    @api.multi
    def is_bcc_valid(self):
        is_valid = False

        for bcc in self.bcc_license_data:
            if bcc.status == "Active":
                is_valid = True

        return is_valid

    @api.multi
    def _unlink_licenses(self):
        log.info("Assigning license for %s" % self.name)

        # remove current licenses
        linked_licenses = self.env["bcc.license"].search([("partner_id", "in", self.id)])
        for _license in linked_licenses:
            _license.write(dict(partner_id=[(3, self.id)]))

    @api.multi
    @api.depends()
    def _compute_filter_field(self):
        pass

    def _search_filter_field(self, operator, value):
        all_partners = self.search([])
        ids = []
        if operator == 'ilike':
            ids = all_partners.filtered(
                lambda r: r.x_studio_field_K2J26 and (value in r.x_studio_field_K2J26)
            ).mapped('id')

        return [('id', 'in', ids)]


class SaleOrderBCCValidator(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_button_confirm(self):
        if not self.partner_id.is_bcc_valid():
            raise Exception("Partner not BCC compliant!")

        return super(SaleOrderBCCValidator, self).action_button_confirm()
