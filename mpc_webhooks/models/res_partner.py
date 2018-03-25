# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
import logging
import requests
_logger = logging.getLogger(__name__)

class res_partner(models.Model):
	_inherit = 'res.partner'

	@api.model
	def create(self, vals):
		new_product = super(res_partner, self).create(vals)

		try:
			_logger.info("sending test webhook")
			r = requests.post( "https://mpcrequestbin.herokuapp.com/15iix041",data=json.dumps(new_product),headers={'Content-Type': 'application/json'})
		except Exception as error:
			_logger.info("error sending webhook: " + str(error))

		return new_product