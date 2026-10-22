from odoo import fields, models


class HydraulicPneumatic(models.Model):
    _name = "hydraulic.pneumatic.report"
    _description = "Hydraulic and Pneumatic Systems"
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