from odoo import fields, models, api

class UnitConditionResult(models.Model):
    _name = "unit.condition.result"
    _description = "Unit Condition Result"
    _order = "sort_order, id"

    unit_condition_id = fields.Many2one(
        "unit.condition.report",
        string="Unit Condition Report",
        required=True,
        ondelete="cascade",
    )

    # OPTIONAL, bukan required
    specification_id = fields.Many2one(
        "specification.report",
        string="Specification",
        required=True,
        readonly=True,
        ondelete="restrict",
    )

    sequence = fields.Char(
        string="No",
        readonly=True,
    )

    item_detail = fields.Text(
        string="Item Detail",
        readonly=True,
    )

    is_section = fields.Boolean(
        string="Section",
        readonly=True,
    )

    sort_order = fields.Integer(
        string="Sort Order",
        readonly=True,
    )

    condition = fields.Selection(
        [
            ("green", "Green"),
            ("amber", "Amber"),
            ("red", "Red"),
            ("na", "N/A"),
        ],
        string="Condition",
    )

    observation = fields.Text(
        string="Observations / Recommendations",
    )

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:

            specification_id = vals.get("specification_id")

            if specification_id:

                specification = self.env[
                    "specification.report"
                ].browse(specification_id)

                if specification.exists():

                    vals.update({
                        "sequence": specification.sequence,
                        "item_detail": specification.item_detail,
                        "is_section": specification.is_section,
                        "sort_order": specification.sort_order,
                    })

        return super().create(vals_list)