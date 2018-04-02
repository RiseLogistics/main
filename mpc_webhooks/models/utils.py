from odoo import fields, models, api
import logging
import requests
import json
_logger = logging.getLogger(__name__)


def send_webhook(id,model,trigger):
	try:
		payload = {'model':model,'id':id,'trigger':trigger}
		_logger.info(payload)
		r = requests.post( "https://sean-local.ngrok.io/api/v3/webhooks/odoo",data=json.dumps(payload),headers={'Content-Type': 'application/json'})
	except Exception as error:
		_logger.info("error sending webhook: " + str(error))