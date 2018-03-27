from odoo import fields, models, api
import logging
import requests
import json
import sys
_logger = logging.getLogger(__name__)

class sales_order(models.Model):
	_inherit = 'sale.order'

	@api.multi
	def action_create_quickbooks(self):
		_logger.info("Create a copy of this sales order in quickbooks")
		_logger.info(str(self))
		_logger.info( str(sys.version) )
		return {
			'type': 'ir.actions.act_url',
			'url': 'https://mpcrequestbin.herokuapp.com/15iix041?id=%s&q=test' % (self.id),
			'target': 'self'
		}