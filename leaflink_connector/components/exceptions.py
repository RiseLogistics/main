# -*- coding: utf-8 -*-

from odoo.addons.connector.exception import RetryableJobError


class OrderImportRetry(RetryableJobError):
    pass


class OrderExportRetry(RetryableJobError):
    pass


class ProductExportRetry(RetryableJobError):
    pass


class PartnerExportRetry(RetryableJobError):
    pass
