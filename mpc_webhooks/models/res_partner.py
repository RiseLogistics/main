# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
import logging
import requests
import json
_logger = logging.getLogger(__name__)

class res_partner(models.Model):
	_inherit = 'res.partner'

	@api.model
	def create(self, vals):
		record = super(res_partner, self).create(vals)
		try:
			payload = {'model':'res.partner','id':record.id,'trigger':'create'}
			r = requests.post( "https://mpcrequestbin.herokuapp.com/15iix041",data=json.dumps(payload),headers={'Content-Type': 'application/json'})
		except Exception as error:
			_logger.info("error sending webhook: " + str(error))
		return record

	@api.multi
	def unlink(self):
		record = super(res_partner,self).unlink()
		try:
			payload = {'model':'res.partner','id':self.id,'trigger':'unlink'}
			r = requests.post( "https://mpcrequestbin.herokuapp.com/15iix041",data=json.dumps(payload),headers={'Content-Type': 'application/json'})
		except Exception as error:
			_logger.info("error sending webhook: " + str(error))
		return record		

	@api.multi
	def write(self, vals):
		record = super(res_partner, self).write(vals)
		try:
			payload = {'model':'res.partner','trigger':'write','id':self.id}
			r = requests.post( "https://mpcrequestbin.herokuapp.com/15iix041",data=json.dumps(payload),headers={'Content-Type': 'application/json'})
		except Exception as error:
			_logger.info("error sending webhook: " + str(error))
		return record