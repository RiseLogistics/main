# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Rice Brand',
    'version': '1.0',
    'summary': 'Delivery Slip Customization',
    'description': """
Customization report for delivery slip and receipts also having reports for proof of pick up and proof of delivery.
    """,
    'depends': ['stock', 'delivery'],
    'data': [
        'report/report_delivery_slip.xml',
        'report/report_proof_of_pickup.xml',
        'report/report_proof_of_delivery.xml',
    ],
    'installable': True,
    'application': False,
}
