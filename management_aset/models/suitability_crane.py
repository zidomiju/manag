from odoo import fields, models


class SuitabilityCrane(models.Model):
    _name = "suitability.crane.report"
    _description = "SUITABILITY OF CRANE FOR MANRIDING DUTIES"
    _order = "sort_order, id"

    sequence = fields.Char(
        string="Sequence",
        required=True,
    )

    item_detail = fields.Text(
        string="Item Detail",
        required=True,
    )

    is_section = fields.Boolean(
        string="Section",
        default=False,
    )

    sort_order = fields.Integer(
        string="Sort Order",
        default=10,
    )

    active = fields.Boolean(
        string="Active",
        default=True,
    )