# -*- coding: utf-8 -*-

import werkzeug
import logging
import base64

from odoo import http
from odoo.http import request, content_disposition
from odoo.exceptions import AccessError


_logger = logging.getLogger(__name__)


class COAFileServerConnector(http.Controller):
    @http.route("/coa_server/<req_id>", auth="public", method=["GET"], type="http", csrf=False, cors="*")
    def index(self, req_id, **kw):
        _logger.warning("Serving COA file for {}".format(req_id))
        try:
            return self._serve_coa(req_id)
        
        except Exception as e:
            _logger.exception("Exception while in /coa_server/ [%s]" % e)
            raise AccessError("unable to serve COA")

    def _serve_coa(self, req_id):
        file_server = request.env["coa.file.server"].sudo()
        move_line_coa = file_server.find_and_disable(req_id)
        if not move_line_coa:
            return request.not_found()

        _coa_file, _filename = move_line_coa

        return request.make_response(
            base64.b64decode(_coa_file),
            [("Content-Type", "application/octet-stream"),
             ("Content-Disposition", content_disposition(_filename))])
