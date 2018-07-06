from odoo import fields, models, api
import logging
import grequests
import json

_logger = logging.getLogger(__name__)


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

        async_list = []
        for url in urls:
            _logger.info("sending webhook notification [{0}] ENV{1}"
                         .format(url, env_type))
            _logger.info(payload)

            async_task = grequests.post(webhook_url,
                                    data=json.dumps(payload),
                                    headers={'Content-Type': 'application/json'})
            # queue async calls
            async_list.append(async_task)

        # fire async tasks
        grequests.map(async_list)

    except Exception as error :
        _logger.info("error sending webhook: " + str(error))
