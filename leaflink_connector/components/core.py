# -*- coding: utf-8 -*-

from odoo.addons.component.core import AbstractComponent


class BaseLeafLinkConnectorComponent(AbstractComponent):
    _name = "base.leaflink.connector"
    _inherit = "base.connector"
    _collection = "leaflink.manager.api"
