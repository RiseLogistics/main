from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class LeafLinkPartner(models.Model):
    _inherit = ["res.partner",
                "leaflink.base.adapter"]

    _name = "res.partner"
    _external_model = "Customer"

    leaflink_slug = fields.Char()

    @property
    @api.multi
    def leaflink_fields(self):
        self.ensure_one()

        return {
            "id": self.leaflink_external_id,
            "slug": self.leaflink_slug
        }
