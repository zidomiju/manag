from odoo import fields, models, api


class UnitConditionResult(models.Model):
    _name = "unit.condition.result7"
    _description = "Unit Condition Result 7"
    _order = "sort_order, id"

    unit_condition_id = fields.Many2one(
        "unit.condition.report",
        string="Unit Condition Report",
        required=True,
        ondelete="cascade",
    )

    power_mover_id = fields.Many2one(
        "prime.mover.report",
        string="Prime Mover And Drive Train",
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

            power_mover_id = vals.get("power_mover_id")

            if power_mover_id:

                power_mover = self.env[
                    "prime.mover.report"
                ].browse(power_mover_id)

                if power_mover.exists():

                    vals.update({
                        "sequence": power_mover.sequence,
                        "item_detail": power_mover.item_detail,
                        "is_section":power_mover.is_section,
                        "sort_order": power_mover.sort_order,
                    })

        return super().create(vals_list)