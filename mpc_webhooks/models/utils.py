from odoo import fields, models, api
import logging
import json

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

_logger = logging.getLogger(__name__)


def _post(url, payload):
    _logger.info("Calling Webhook [{0}]".format(url))
    try:
        requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
    except requests.exceptions.Timeout:
        _logger.info("Webhook Timeout[{0}]".format(url))


def send_webhook(id, model, trigger, dbname=None):
    try:
        env_type = None
        webhook_url = None
        leaflink_webhook_url = ("https://leaflink-{0}-riselogistics.herokuapp.com"
                                "/webhooks/odoo/1RL3137258415e5dee668438702cdd5b24ef158ce5575e")

        if "staging" in dbname:
            webhook_url = "https://rise-online.herokuapp.com/api/v3/webhooks/odoo"
            leaflink_webhook_url = leaflink_webhook_url.format("stage")
            env_type = "[STAGING]"

        else:
            webhook_url = "https://rise-logistics.herokuapp.com/api/v3/webhooks/odoo"
            leaflink_webhook_url = leaflink_webhook_url.format("prod")
            env_type = "[PRODUCTION]"

        payload = {'model': model, 'id': id, 'trigger': trigger}
        urls = [webhook_url, leaflink_webhook_url]

        _logger.info("Payload[{0}] - ENV{1}".format(payload, env_type))

        with ThreadPoolExecutor(max_workers=2) as executor:
            for url in urls:
                executor.submit(_post, url, payload)

    except Exception as error :
        _logger.info("error sending webhook: " + str(error))


