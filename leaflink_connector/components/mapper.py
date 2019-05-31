from odoo.addons.component.core import AbstractComponent


class LeafLinkImportMapper(AbstractComponent):
    _name = "base.leaflink.import.mapper"
    _inherit = ["base.leaflink.connector", "base.import.mapper"]
    _usage = "import.mapper"


class LeafLinkExportMapper(AbstractComponent):
    _name = "base.leaflink.export.mapper"
    _inherit = ["base.leaflink.connector", "base.export.mapper"]
    _usage = "export.mapper"
