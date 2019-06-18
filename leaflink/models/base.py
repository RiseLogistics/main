# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api
import logging

from ..api_client import resources


_logger = logging.getLogger(__name__)


class GenericLeafLinkAdapter(models.AbstractModel):
    _name = "leaflink.base.adapter"
    _external_model = None

    leaflink_external_id = fields.Integer()
    leaflink_sync_enabled = fields.Boolean()
    leaflink_last_sync_ts = fields.Datetime()

    @property
    @api.multi
    def leaflink_crud(self):
        self.ensure_one()

        api_base = self._leaflink_config_param("api.base")
        api_token = self._leaflink_config_param("api.token")
        api_slug = self._leaflink_config_param("api.slug")
        client_resource = getattr(resources, self._external_model)

        return client_resource(
            company=api_slug,
            api_key=api_token,
            base_url=api_base
        )

    @api.multi
    def set_leaflink_sync_ts(self):
        self.ensure_one()

        ts = datetime.now()
        _logger.warning("[%s]Updating LeafLink sync TS[%s]" % (self.id, ts))
        self.leaflink_last_sync_ts = ts

    @api.model
    def _leaflink_config_param(self, param_key):
        config_ns = "leaflink.%s.PROD"
        config_env = self.env["ir.config_parameter"].sudo()

        if "STAGING" in self._cr.dbname.upper():
            config_ns = "leaflink.%s.STAGING"

        return config_env.get_param(config_ns % param_key, "").strip()
