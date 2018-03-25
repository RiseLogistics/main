# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
	_inherit = 'res.partner'

	@api.model
	def create(self, vals):
		print("DEBUG: CREATE 1")
		new_product = super(ResPartner, self).create(vals)
		print("new_product: " + str(new_product))
		print("DEBUG: CREATE 2")
		return new_product