from odoo import fields,models
class WireRope(models.Model):
    _name="wire.rope.specification"
    _description="List of detail in Part 1.1.2 : WIRE ROPE SPECIFICATION "
    _order="sort_order, id"

    location=fields.Char(
        string="Location",
        required=True
    )
    sort_order=fields.Integer(
        string="Sort Order",
        default=10,
    )
    active = fields.Boolean(
            string="Active",
            default=True,
    )
    