from odoo import models, fields


STATES = [("pending", "Pending Sync"),
          ("started", "Started Sync"),
          ("synced", "Synced"),
          ("fail", "Sync Failed")]


class LeafLinkManager(models.Model):
    _name = "leaflink.manager"

    name = fields.Char()
    brand_setting_id = fields.Many2one(
        comodel_name="leaflink.manager.settings",
        string="LeafLink Brand Settings",
        required=True,
        ondelete="restrict"
    )


class LeafLinkBrand(models.Model):
    _name = "leaflink.manager.brand"

    internal_brand_id = fields.Many2one(
        comodel_name="x_brand",
        string="Internal DYME Brand",
        required=True,
        ondelete="restrict"
    )

    internal_vendor_id = fields.Many2one(
        comodel_name="res.partner",
        string="Internal Vendor",
        required=True,
        ondelete="restrict"
    )

    api_backend = fields.Many2one(
        comodel_name="leaflink.manager.api",
        string="LeafLink API Connection",
        required=True,
        ondelete="restrict"
    )

    status = fields.Selection(
        STATES,
        readonly=True,
        required=True,
        index=True,
        default="pending",
        string="Sync State"
    )

    external_id = fields.Char(string="LeafLink Brand ID", required=True)
    external_slug = fields.Char(string="LeafLink Brand Slug", required=True)


class LeafLinkSettings(models.Model):
    _name = "leaflink.manager.settings"

    managed_brand_id = fields.Many2one(
        comodel_name="leaflink.manager.brand",
        string="LeafLink Brand",
        required=True,
        ondelete="restrict"
    )

    api_id = fields.Many2one(
        comodel_name="leaflink.manager.api",
        string="LeafLink API",
        required=True,
        ondelete="restrict"
    )

    orders_sync_freq = fields.Integer(string="Orders Sync Frequency", required=True)
    products_sync_freq = fields.Integer(string="Products Sync Frequency", required=True)
    partners_sync_freq = fields.Integer(string="Partners Sync Frequency", required=True)

    orders_sync_ts = fields.Datetime(string="Orders Last Update")
    products_sync_ts = fields.Datetime(string="Products Last Update")
    partners_sync_ts = fields.Datetime(string="Partners Last Update")
    
    active = fields.Boolean(default=False, string="Sync Brand")


class LeafLinkAPI(models.Model):
    _name = "leaflink.manager.api"
    _inherit = "connector.backend"
    
    name = fields.Char(required=True)
    
    token = fields.Char(string="API Token", required=True, ondelete="restrict")    
    base_uri = fields.Char(string="API Base", required=True, ondelete="restrict")
    external_id = fields.Char(string="LeafLink API ID", required=True, ondelete="restrict")
    external_slug = fields.Char(string="LeafLink API Slug", required=True, ondelete="restrict")

    enabled = fields.Boolean(default=False, string="Enable API")
