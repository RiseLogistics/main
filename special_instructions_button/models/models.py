# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProductTemplateHandlingInstructions(models.Model):
    _inherit = "product.template"

    @api.multi
    def show_handling_instructions(self):
        res = {
            "warning": {
                "title": _("Handling Instructions"),
                "message": _("N/A")
            }
        }

        if self.x_handling_instructions:
            res["warning"]["message"] = _(self.x_handling_instructions)


        return res



