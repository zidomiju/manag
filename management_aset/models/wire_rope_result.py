from odoo import fields, models, api

class WireRopeResult(models.Model):
    _name="wire.rope.result"
    _description="Wire Rope Result"
    _order="sort_order, id"

    unit_condition_id=fields.Many2one(
        "unit.condition.report",
        string="Unit Condition Report",
        required=True,
        readonly=True,
        ondelete="cascade"
    )

    wire_rope_id=fields.Many2one(
        "wire.rope.specification",
        string="Wire Rope Specification",
        required=True,
        ondelete="restrict"
    )

    location=fields.Char(
        string="Location",
        readonly=True
    )
    sort_order=fields.Integer(
        string="Sort Order",
        readonly=True
    )

    nominal_diameter=fields.Char(
        string="Nominal Diameter"
    )
    rope_description=fields.Char(
        string="Rope Description"
    )
    date_install=fields.Date(
        string="Date Installed"
    )
    certificate_no=fields.Char(
        string="Certificate No"
    )

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:

            wire_rope_id = vals.get("wire_rope_id")

            if wire_rope_id:

                wire_rope = self.env[
                    "wire.rope.specification"
                ].browse(wire_rope_id)

                if wire_rope.exists():

                    vals.update({
                        "location": wire_rope.location,
                        "sort_order":wire_rope.sort_order
                    })

        return super().create(vals_list)