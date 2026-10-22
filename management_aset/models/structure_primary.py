from odoo import fields, models


class StructureionReport(models.Model):
    _name = "structure.primary.report"
    _description = "Structure and Primary Load Path Elements"
    _order = "sort_order asc"

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