# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResPartner(models.Model):
	_inherit = 'res.partner'
	def create(self, cr, uid, vals, context=None):
		print("mpc - test - create - mpc -test - create - mpc - test - create")
		return super(pos_order, self).create(cr, uid, vals, context=context)