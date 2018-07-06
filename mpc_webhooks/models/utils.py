from odoo import fields, models, api
import logging
import requests
import json
_logger = logging.getLogger(__name__)


def send_webhook(id,model,trigger,dbname=None):
	try:
		webhook_url = None
		leaflink_webhook_url = ("https://leaflink-{0}-riselogistics.herokuapp.com"
                                "/webhooks/odoo/1RL3137258415e5dee668438702cdd5b24ef158ce5575e")

		if "staging" in dbname:
			webhook_url = "https://rise-online.herokuapp.com/api/v3/webhooks/odoo"
			leaflink_webhook_url = leaflink_webhook_url.format("stage")

		else:
			webhook_url = "https://rise-logistics.herokuapp.com/api/v3/webhooks/odoo"
			leaflink_webhook_url = leaflink_webhook_url.format("prod")

		payload = {'model':model,'id':id,'trigger':trigger}

		_logger.info("sending webhook notification to: " + webhook_url)
		_logger.info(payload)

		r = requests.post( webhook_url ,data=json.dumps(payload),headers={'Content-Type': 'application/json'})

		_logger.info("sending LeafLink webhook notification to: " + leaflink_webhook_url)
		requests.post(leaflink_webhook_url,
                      json=payload,
                      headers={'Content-Type': 'application/json'})

	except Exception as error:
		_logger.info("error sending webhook: " + str(error))