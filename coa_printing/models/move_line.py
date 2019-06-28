import logging
import random
import urllib.parse as SAFE_URL
import datetime

from odoo import models, fields, api
import jwt


_logger = logging.getLogger(__name__)


class COAFileServerModel(models.Model):
    _name = "coa.file.server"

    token = fields.Integer(index=True)
    move_line_id = fields.Many2one("stock.move.line")
    active = fields.Boolean(default=True)

    @api.model
    def generate_coa_request_token(self, seed, move_line, with_url=False):
        _token = seed * random.randint(345, 98765)
        self.create({
            "token": _token,
            "move_line_id": move_line.id
        })

        config_env = self.env["ir.config_parameter"].sudo()
        url = config_env.get_param("dyme.coa.server.api", "").strip()

        return with_url and "%s%s" % (url, _token) or _token

    @api.model
    def find_and_disable(self, request_token):
        _coa_serve_rec = self.search([("token", "=", request_token),
                                      ("active", "=", True)])

        if _coa_serve_rec:
            _move_line = _coa_serve_rec.move_line_id
            _coa_serve_rec.active = False
            return _move_line.x_coa_upload, _move_line.x_coa_upload_filename

        return None


class COAPrintWizard(models.TransientModel):
    _name = "coa.print.wizard"

    def _get_default_picks(self):
        active_pick_ids = self.env.context.get("active_ids")
        return self.env["stock.picking"].browse(active_pick_ids)

    state = fields.Selection(
        selection=[("draft", "Draft"),
                   ("confirm", "Confirm"),
                   ("print", "Print")],
        readonly=True,
        default="draft",
        string="Print State"
    )

    pick_ids = fields.Many2many("stock.picking",
                                string="Transfers",
                                default=_get_default_picks)

    move_line_coa_ids = fields.Many2many("stock.move.line",
                                         compute="_set_move_line_coa_ids",
                                         string="COAs To Print")

    move_line_dne_coa_ids = fields.Many2many("stock.move.line",
                                             compute="_set_move_line_dne_coa_ids",
                                             string="COAs Not Assigned")

    seed = fields.Integer(default=lambda _: random.randint(100, 999))

    def _sign_request(self, expires_in_seconds=60 * 10):
        payload = dict(exp=datetime.datetime.utcnow() +
                           datetime.timedelta(seconds=expires_in_seconds))

        _key = self.env["ir.config_parameter"].sudo().get_param("dyme.coa.print.key", "")

        return jwt.encode(payload, _key, algorithm="HS256")

    @api.model
    def _build_single_transfer_coa_request(self, pick, files_only=False):
        files = []
        coa_server_env = self.env["coa.file.server"]

        for move_line in pick.move_line_ids:
            if move_line.x_coa_upload:
                token = coa_server_env.generate_coa_request_token(self.seed, move_line, with_url=True)
                files.append(token)

        if files:
            return files_only and files or {"name": pick.name, "files": files}

        return files

    @api.multi
    def confirm_coa_print_action(self):
        self.ensure_one()
        record = self
        req_payload_parts = []
        record.state = "print"

        for pick in record.pick_ids:
            payload_part = self._build_single_transfer_coa_request(pick, files_only=True)
            if payload_part:
                req_payload_parts += payload_part

        payload = SAFE_URL.urlencode({"coa": [{"name": "COAs", "files": req_payload_parts}],
                                      "token": self._sign_request()})

        _logger.warning("Dispatching COA merger %s" % payload)

        config_env = self.env["ir.config_parameter"].sudo()
        redirect_to = "%s?%s" % (config_env.get_param("dyme.coa.merger.api", "").strip(), payload)

        return {"type": "ir.actions.act_url",
                "url": redirect_to,
                "nodestroy": False,
                "target": "new"}

    @api.multi
    def draft_coa_print_action(self):
        for record in self:
            record.state = "confirm"

        return {"type": "set_scrollTop"}

    @api.one
    @api.depends("pick_ids")
    def _set_move_line_coa_ids(self):
        valid_ids = []
        for pick in self.pick_ids:
            valid_ids += pick.move_line_ids.filtered(lambda rec: rec.x_coa_upload).ids

        self.move_line_coa_ids = [(6, 0, valid_ids)]

    @api.one
    @api.depends("pick_ids")
    def _set_move_line_dne_coa_ids(self):
        dne_ids = []
        for pick in self.pick_ids:
            dne_ids += pick.move_line_ids.filtered(lambda rec: not rec.x_coa_upload).ids

        self.move_line_dne_coa_ids = [(6, 0, dne_ids)]