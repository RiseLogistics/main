# -*- coding: utf-8 -*-

from odoo.addons.component.core import AbstractComponent

from ..api_client import resources


class GenericAdapter(AbstractComponent):
    _name = "leaflink.adapter"
    _inherit = ["base.backend.adapter", "base.leaflink.connector"]
    _usage = "backend.adapter"

    _leaflink_model = None
    _external_model = None

    def config_api_client(self, api_backend):
        client_resource = getattr(resources, self._external_model)

        res = client_resource(
            company=api_backend.external_slug,
            api_key=api_backend.token,
            base_url=api_backend.base_uri
        )

        return res
