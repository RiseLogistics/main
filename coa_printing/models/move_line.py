import logging
import random
import urllib.parse as SAFE_URL
import datetime

from odoo import models, fields, api
import jwt


_logger = logging.getLogger(__name__)


def soft_seed():
    upper, lower = 9999, 199
    return random.randint(lower, upper)


class COAFileServerModel(models.Model):
    _name = "coa.file.server"

    token = fields.Integer(index=True)
    move_line_id = fields.Many2one("stock.move.line")
    active = fields.Boolean(default=True)

    lot_id = fields.Integer(index=True)
    product_id = fields.Integer(index=True)
    wizard_id = fields.Integer(index=True)
    coa_filename = fields.Char(index=True)

    @api.model
    def generate_coa_request_token(self, seed, move_line, wizard_id, with_url=False):
        _token = seed * soft_seed()
        self.create({
            "token": _token,
            "move_line_id": move_line.id,
            "lot_id": move_line.lot_id.id,
            "product_id": move_line.product_id.id,
            "wizard_id": wizard_id,
            "coa_filename": move_line.x_coa_upload_filename
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

    @api.model
    def active_token_exists(self, coa_filename, lot_id, wizard_id):
        _coa_serve_rec = self.search([("coa_filename", "=", coa_filename),
                                      ("active", "=", True),
                                      ("wizard_id", "=", wizard_id),
                                      ("lot_id", "=", lot_id)])

        if _coa_serve_rec: return True

        return False


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

    seed = fields.Integer(default=lambda _: soft_seed())
    wizard_session_id = fields.Integer(default=lambda _: soft_seed())

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
            if not move_line.x_coa_upload:
                continue

            coa_in_download_list = coa_server_env.active_token_exists(
                coa_filename=move_line.x_coa_upload_filename,
                lot_id=move_line.lot_id.id,
                wizard_id=self.wizard_session_id)

            if not coa_in_download_list:
                token = coa_server_env.generate_coa_request_token(
                    seed=self.seed,
                    wizard_id=self.wizard_session_id,
                    move_line=move_line,
                    with_url=True)

                files.append(token)

        if files:
            return files_only and files or {"name": pick.name, "files": files}

        return files

    @api.multi
    def confirm_coa_print_action(self):
        self.ensure_one()
        record = self
        req_payload_parts = []
        config_env = self.env["ir.config_parameter"].sudo()

        files_only = config_env.get_param("dyme.coa.merger.no_page_header", "FALSE").strip()
        files_only = files_only == "TRUE"

        for pick in record.pick_ids:
            payload_part = self._build_single_transfer_coa_request(pick, files_only)

            if payload_part:
                req_payload_parts += files_only and payload_part or [payload_part]

        payload = SAFE_URL.urlencode({"coa": files_only and [{"name": "COAs", "files": req_payload_parts}] or req_payload_parts,
                                      "token": self._sign_request()})

        _logger.warning("Dispatching COA merger %s" % payload)

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
