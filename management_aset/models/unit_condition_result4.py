from odoo import fields, models, api


class UnitConditionResult(models.Model):
    _name = "unit.condition.result4"
    _description = "Unit Condition Result 4"
    _order = "sort_order, id"

    unit_condition_id = fields.Many2one(
        "unit.condition.report",
        string="Unit Condition Report",
        required=True,
        ondelete="cascade",
    )

    structure_primary_id = fields.Many2one(
        "structure.primary.report",
        string="Structure and Primary Load Path Elements",
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

            structure_primary_id = vals.get("structure_primary_id")

            if structure_primary_id:

                structure_primary = self.env[
                    "structure.primary.report"
                ].browse(structure_primary_id)

                if structure_primary.exists():

                    vals.update({
                        "sequence": structure_primary.sequence,
                        "item_detail": structure_primary.item_detail,
                        "is_section":structure_primary.is_section,
                        "sort_order": structure_primary.sort_order,
                    })

        return super().create(vals_list)