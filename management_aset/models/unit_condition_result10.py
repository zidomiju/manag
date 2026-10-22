from odoo import fields, models, api


class UnitConditionResult(models.Model):
    _name = "unit.condition.result10"
    _description = "Unit Condition Result 10"
    _order = "sort_order, id"

    unit_condition_id = fields.Many2one(
        "unit.condition.report",
        string="Unit Condition Report",
        required=True,
        ondelete="cascade",
    )

    suitability_crane_id = fields.Many2one(
        "suitability.crane.report",
        string="Electrical System",
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

            suitability_crane_id = vals.get("suitability_crane_id")

            if suitability_crane_id:

                suitability_crane = self.env[
                    "suitability.crane.report"
                ].browse(suitability_crane_id)

                if suitability_crane.exists():

                    vals.update({
                        "sequence": suitability_crane.sequence,
                        "item_detail": suitability_crane.item_detail,
                        "is_section":suitability_crane.is_section,
                        "sort_order": suitability_crane.sort_order,
                    })

        return super().create(vals_list)