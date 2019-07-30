from odoo import fields, models, api
import logging
import json
import pika
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

_logger = logging.getLogger(__name__)


def _post(url, payload):
    _logger.info("Calling Webhook [{0}]".format(url))
    try:
        requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
    except requests.exceptions.Timeout:
        _logger.info("Webhook Timeout[{0}]".format(url))


def publish_change(id,model,trigger,dbname=None):
    try:
        env_type = None
        exchange = ""
        env_type = os.environ['ODOO_STAGE']

        topic_name = "odoo_{model}_{env}".format(model=model,env=env_type)
        _logger.info("topic={topic}".format(topic=topic_name))
        payload = {
            'id': id,
            'trigger': trigger
        }

        _logger.info("connecting to rabbit")
        params = pika.URLParameters('amqp://uaoqejpl:vrjdmxg7QDzqcPyS7qAIW5HSme4OEa1s@skunk.rmq.cloudamqp.com/uaoqejpl')
        conn = pika.BlockingConnection(params)
        channel = conn.channel()
        channel.exchange_declare(exchange=topic_name,exchange_type="fanout",durable=True,auto_delete=False)
        channel.basic_publish(body=json.dumps(payload),exchange=topic_name,routing_key="")
        _logger.info("message sent")

        conn.close()

    except Exception as error :
        _logger.info("error publishing change to queue: " + str(error))


def send_webhook(id, model, trigger, dbname=None):

    #publish_change(id,model,trigger,dbname=dbname)

    try:
        env_type = None
        webhook_url = None
        

        if "staging" in dbname:
            webhook_url = "https://rise-online.herokuapp.com/api/v3/webhooks/odoo"
            env_type = "[STAGING]"

        else:
            webhook_url = "https://rise-logistics.herokuapp.com/api/v3/webhooks/odoo"
            env_type = "[PRODUCTION]"

        payload = {'model': model, 'id': id, 'trigger': trigger}
        urls = [webhook_url]

        _logger.info("Payload[{0}] - ENV{1}".format(payload, env_type))

        with ThreadPoolExecutor(max_workers=2) as executor:
            for url in urls:
                executor.submit(_post, url, payload)

    except Exception as error :
        _logger.info("error sending webhook: " + str(error))


