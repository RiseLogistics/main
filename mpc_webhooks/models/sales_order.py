from odoo import fields, models, api
import logging
import requests
import json
_logger = logging.getLogger(__name__)

class sales_order(models.Model):
	_inherit = 'sale.order'

	@api.multi
	def action_create_quickbooks(self):
		_logger.info("Create a copy of this sales order in quickbooks")
		_logger.info(str(self))