from odoo import fields, models, api
import logging
import requests
import json
from .utils import send_webhook

_logger = logging.getLogger(__name__)

class product_template(models.Model):
	_inherit = 'product.template'

	@api.model
	def create(self, vals):
		record = super(product_template,self).create(vals)
		send_webhook( record.id,self._inherit,'create')
		return record

	@api.one
	def unlink(self):
		record = super(product_template,self).unlink()
		send_webhook( self.id,self._inherit,'unlink')
		return record		

	@api.multi
	def write(self, vals):
		record = super(product_template, self).write(vals)
		send_webhook( self.id,self._inherit,'write')
		return record




class product_product(models.Model):
	_inherit = 'product.product'

	@api.model
	def create(self, vals):
		record = super(product_product,self).create(vals)
		send_webhook( record.id,self._inherit,'create')
		return record

	@api.one
	def unlink(self):
		record = super(product_product,self).unlink()
		send_webhook( self.id,self._inherit,'unlink')
		return record		

	@api.multi
	def write(self, vals):
		record = super(product_product, self).write(vals)
		send_webhook( self.id,self._inherit,'write')
		return record

if False:
	class x_varietal(models.Model):
		_inherit = 'x_varietal'

		@api.model
		def create(self, vals):
			record = super(x_varietal,self).create(vals)
			send_webhook( record.id,self._inherit,'create')
			return record

		@api.one
		def unlink(self):
			record = super(x_varietal,self).unlink()
			send_webhook( self.id,self._inherit,'unlink')
			return record		

		@api.multi
		def write(self, vals):
			record = super(x_varietal, self).write(vals)
			send_webhook( self.id,self._inherit,'write')
			return record


	class x_cannabis_type(models.Model):
		_inherit = 'x_cannabis_type'

		@api.model
		def create(self, vals):
			record = super(x_cannabis_type,self).create(vals)
			send_webhook( record.id,self._inherit,'create')
			return record

		@api.one
		def unlink(self):
			record = super(x_cannabis_type,self).unlink()
			send_webhook( self.id,self._inherit,'unlink')
			return record		

		@api.multi
		def write(self, vals):
			record = super(x_cannabis_type, self).write(vals)
			send_webhook( self.id,self._inherit,'write')
			return record



	class x_brand(models.Model):
		_inherit = 'x_brand'

		@api.model
		def create(self, vals):
			record = super(x_brand,self).create(vals)
			send_webhook( record.id,self._inherit,'create')
			return record

		@api.one
		def unlink(self):
			record = super(x_brand,self).unlink()
			send_webhook( self.id,self._inherit,'unlink')
			return record		

		@api.multi
		def write(self, vals):
			record = super(x_brand, self).write(vals)
			send_webhook( self.id,self._inherit,'write')
			return record


class product_uom(models.Model):
	_inherit = 'product.uom'

	@api.model
	def create(self, vals):
		record = super(product_uom,self).create(vals)
		send_webhook( record.id,self._inherit,'create')
		return record

	@api.one
	def unlink(self):
		record = super(product_uom,self).unlink()
		send_webhook( self.id,self._inherit,'unlink')
		return record		

	@api.multi
	def write(self, vals):
		record = super(product_uom, self).write(vals)
		send_webhook( self.id,self._inherit,'write')
		return record



class product_category(models.Model):
	_inherit = 'product.category'

	@api.model
	def create(self, vals):
		record = super(product_category,self).create(vals)
		send_webhook( record.id,self._inherit,'create')
		return record

	@api.one
	def unlink(self):
		record = super(product_category,self).unlink()
		send_webhook( self.id,self._inherit,'unlink')
		return record		

	@api.multi
	def write(self, vals):
		record = super(product_category, self).write(vals)
		send_webhook( self.id,self._inherit,'write')
		return record
# x_varietal , x_cannabis_type , # x_brand, # product.uom, # product.category


