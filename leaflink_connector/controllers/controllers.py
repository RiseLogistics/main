# -*- coding: utf-8 -*-


from odoo import http


class LeaflinkConnector(http.Controller):
    @http.route('/leaflink_connector/trigger_so/', auth='public')
    def index(self, **kw):
        return http.request.env["leaflink.sale.order"].sudo().handle_so(http.request.param)
