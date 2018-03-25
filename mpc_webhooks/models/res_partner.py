# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class res_partner(models.Model):
	_inherit = 'res.partner'
	mpc_test_field = fields.Boolean('MPC Test Field', default=True)

	@api.model
	def create(self, vals):
		vals['name'] = vals['name'] + "__edited by module"
		_logger.info("DEBUG: CREATE 1")
		new_product = super(res_partner, self).create(vals)
		_logger.info("new_product: " + str(new_product))
		_logger.info("DEBUG: CREATE 2")
		return new_product