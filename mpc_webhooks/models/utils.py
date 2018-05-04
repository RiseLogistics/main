from odoo import fields, models, api
import logging
import requests
import json
_logger = logging.getLogger(__name__)


def send_webhook(id,model,trigger,dbname=None):
	try:
		webhook_url = None

		if "staging" in dbname:
			webhook_url = "https://rise-online.herokuapp.com/api/v3/webhooks/odoo"	
		else:
			webhook_url = "https://rise-logistics.herokuapp.com/api/v3/webhooks/odoo"

		payload = {'model':model,'id':id,'trigger':trigger}

		_logger.info("send webhook notification to: " + webhook_url)
		_logger.info(payload)

		r = requests.post( webhook_url ,data=json.dumps(payload),headers={'Content-Type': 'application/json'})
	except Exception as error:
		_logger.info("error sending webhook: " + str(error))