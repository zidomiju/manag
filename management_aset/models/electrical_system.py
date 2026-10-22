from odoo import fields, models


class ElectricalSystem(models.Model):
    _name = "electrical.system.report"
    _description = "Electrical System Master"
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