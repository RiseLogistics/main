# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
	_inherit = 'res.partner'
	def create(self, cr, uid, vals, context=None):
		_logger.info("mpc - test - create - mpc -test - create - mpc - test - create")
		return super(self).create(cr, uid, vals, context=context)