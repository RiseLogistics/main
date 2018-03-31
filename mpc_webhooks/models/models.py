# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
import logging
import requests
import json
_logger = logging.getLogger(__name__)
from .utils import send_webhook



class res_partner(models.Model):
	_inherit = 'res.partner'

	@api.model
	def create(self, vals):
		record = super(res_partner,self).create(vals)
		send_webhook( record.id,self._inherit,'create')
		return record

	@api.multi
	def unlink(self):
		record = super(res_partner,self).unlink()
		send_webhook( record.id,self._inherit,'unlink')
		return record		

	@api.multi
	def write(self, vals):
		record = super(res_partner, self).write(vals)
		send_webhook( self.id,self._inherit,'write')
		return record



class sale_order(models.Model):
	_inherit = 'sale.order'

	@api.model
	def create(self, vals):
		record = super(sale_order,self).create(vals)
		send_webhook( record.id,self._inherit,'create')
		return record

	@api.multi
	def unlink(self):
		record = super(sale_order,self).unlink()
		send_webhook( self.id,self._inherit,'unlink')
		return record		

	@api.multi
	def write(self, vals):
		record = super(sale_order, self).write(vals)
		send_webhook( self.id,self._inherit,'write')
		return record





class stock_picking(models.Model):
	_inherit = 'stock.picking'

	@api.model
	def create(self, vals):
		record = super(stock_picking,self).create(vals)
		send_webhook( record.id,self._inherit,'create')
		return record

	@api.multi
	def unlink(self):
		record = super(stock_picking,self).unlink()
		send_webhook( self.id,self._inherit,'unlink')
		return record		

	@api.multi
	def write(self, vals):
		record = super(stock_picking, self).write(vals)
		send_webhook( self.id,self._inherit,'write')
		return record




class stock_quant(models.Model):
	_inherit = 'stock.quant'

	@api.model
	def create(self, vals):
		record = super(stock_quant,self).create(vals)
		send_webhook( record.id,self._inherit,'create')
		return record

	@api.multi
	def unlink(self):
		record = super(stock_quant,self).unlink()
		send_webhook( self.id,self._inherit,'unlink')
		return record		

	@api.multi
	def write(self, vals):
		record = super(stock_quant, self).write(vals)
		send_webhook( self.id,self._inherit,'write')
		return record