# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo import exceptions

import pandas
import requests
import logging
import datetime

from .. import env

log = logging.getLogger(__name__)

STATES = [
    ("Pending", "Pending BCC Status Update"),
    ("About to Expire", "About to Expire"),
    ("Active",)         * 2,
    ("Inactive",)       * 2,
    ("Expired",)        * 2,
    ("Revoked",)        * 2,
    ("Canceled",)       * 2,
    ("Suspended",)      * 2,
    ("Surrendered",)    * 2,
    ("Delinquent",)     * 2,
    ("FTB Suspension",) * 2,
    ("Error",)          * 2,
    ("Other",)          * 2,

    ("Family Support Suspension",) * 2,
    ("Military License Inactive", "Military - License Inactive"),
]

LICENSE_USE_TYPES = [
    # BCC
    ("Pending", "Pending License Status Update"),
    ("Adult-Use",) * 2,
    ("Medicinal",) * 2,
    ("BOTH", "Adult/Medicinal"),

    # CDFA
    ("Temporary Cannabis Cultivation License",) * 2,

    # other
    ("N/A", "N/A")
]

BUSINESS_STRUCTURES = [
    ("Pending", "Pending License Status Update"),
    ("Limited Liability Company",)  * 2,
    ("Sole Proprietorship",)        * 2,
    ("General Partnership",)        * 2,
    ("Corporation",)                * 2,
    ("DNE", "N/A")
]


def to_py_date(bcc_date):
    return pandas.to_datetime(bcc_date, infer_datetime_format=True)


class BCCLicenseModel(models.Model):
    _name = 'bcc.license'
    _description = "CA License Status"

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

    business_name = fields.Char(
        ondelete="restrict",
        index=True
    )

    email = fields.Char(
        ondelete="restrict",
        index=True
    )

    phone = fields.Char(ondelete="restrict")
    city = fields.Char(ondelete="restrict")
    county = fields.Char(ondelete="restrict")
    data_source = fields.Char(index=True, ondelete="restrict")

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
    def validate_license_status(self, alert=True):
        today_date = datetime.datetime.today()
        expires_soon = 14 >= (to_py_date(self.expiration_date) - today_date).days > 0
        expired = (to_py_date(self.expiration_date) - today_date).days <= 0

        if alert and (expired or self.status.upper() != "ACTIVE" or expires_soon):
            log.warn("Alerting Expired/Soon to expire License [%s]" % self.license_type)

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

        return bool(not expired and self.status.upper() == "ACTIVE")

    @api.multi
    @api.depends()
    def _compute_filter_field(self): pass

    def _search_filter_field(self, operator, value):
        records = self.search([])
        ids = []
        if operator == "ilike":
            ids = records.filtered(
                lambda r: r.license_number.upper() in value.upper()).mapped("id")

        return [("id", "in", ids)]


class ResPartner(models.Model):
    _inherit = "res.partner"

    bcc_license_data = fields.Many2many("bcc.license")
    force_so_creation = fields.Boolean(default=False, string="Force SO creation")

    filter_on = fields.Char(
        string="Filter on license",
        compute="_compute_filter_field",
        search="_search_filter_field"
    )

    is_bcc_compliant = fields.Boolean(
        string="Filter on complaint partners",
        compute="_compute_bcc_compliant_filter_field",
        search="_search_bcc_compliant_filter_field"
    )

    @api.multi
    def write(self, vals):
        # x_studio_field_K2J26 == temp license number
        lic_recs = self.onchange_license_number(
            vals.get("x_studio_field_K2J26", self.x_studio_field_K2J26))

        lic_ids = lic_recs and lic_recs.ids or False
        if lic_recs:
            vals["bcc_license_data"] = [(6, 0, lic_ids)]

        else:
            vals["bcc_license_data"] = [(5,)]

        res = super(ResPartner, self).write(vals)

        if lic_ids:
            for rec in lic_recs:
                log.warn("LIC %s" % rec.validate_license_status())

        return res

    @api.multi
    def onchange_license_number(self, license_number):
        if not license_number:
            log.warn("License number not set for %s - %s" % (self.name, self.id))
            return False

        lic_rec = self.env["bcc.license"].search(
            [("filter_on", "ilike", "%{}%".format(license_number))])
        log.warn(lic_rec)
        self._unlink_licenses()

        return lic_rec

    @api.multi
    def is_bcc_valid(self):
        is_valid = False
        today = datetime.datetime.today()

        if self.force_so_creation:
            log.warn("Forcing SO creation for partner %s" % self.id)
            is_valid = True

        for bcc in self.bcc_license_data:
            expired = (to_py_date(bcc.expiration_date) - today).days <= 0

            if (bcc.status == "Active" and not expired) and bcc.data_source == "BCC":
                is_valid = True

        return is_valid

    @api.multi
    def _unlink_licenses(self):
        log.info("Unlinking licenses for %s" % self.name)

        # remove current licenses
        linked_licenses = self.env["bcc.license"].search([("partner_id", "in", self.id)])
        for _license in linked_licenses:
            _license.write(dict(partner_id=[(3, self.id)]))

    @api.multi
    @api.depends()
    def _compute_filter_field(self): pass

    def _search_filter_field(self, operator, value):
        all_partners = self.search([])
        ids = []
        if operator == "ilike":
            ids = all_partners.filtered(
                lambda r: r.x_studio_field_K2J26 and (value.upper() in r.x_studio_field_K2J26.upper())
            ).mapped("id")

        return [("id", "in", ids)]

    @api.multi
    @api.depends()
    def _compute_bcc_compliant_filter_field(self): pass

    def _search_bcc_compliant_filter_field(self, operator, value):
        all_partners = self.search([])

        ids = []
        if operator == "=":
            ids = all_partners.filtered(
                lambda r: r.is_bcc_valid() == value
            ).mapped("id")

        if operator == "!=":
            ids = all_partners.filtered(
                lambda r: r.is_bcc_valid() != value
            ).mapped("id")

        return [("id", "in", ids)]


class SaleOrderBCCValidator(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        skip_validation = False
        config_env = self.env["ir.config_parameter"].sudo()

        if config_env.get_param("license_validation.force_all_sale_orders", False):
            log.warn("Forcing SO for *ALL PARTNERS* %s" % self.id)
            skip_validation = True

        # x_studio_field_kVKl0 == created_by[vendor[ on Odoo
        # if not skip_validation and not self.x_studio_field_kVKl0.is_bcc_valid():
        #     raise exceptions.Warning("Partner license [Vendor] NOT compliant. "
        #                              "Must have at least one active license to place an SO.")

        if not skip_validation and not self.partner_id.is_bcc_valid():
            raise exceptions.Warning("Partner license [Retailer] NOT compliant. "
                                     "Must have at least one active license to place an SO.")

        return super(SaleOrderBCCValidator, self).action_confirm()
