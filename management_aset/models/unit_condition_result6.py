from odoo import fields, models, api


class UnitConditionResult(models.Model):
    _name = "unit.condition.result6"
    _description = "Unit Condition Result 6"
    _order = "sort_order, id"

    unit_condition_id = fields.Many2one(
        "unit.condition.report",
        string="Unit Condition Report",
        required=True,
        ondelete="cascade",
    )

    hoist_slew_id = fields.Many2one(
        "hoist.slew.report",
        string="Wire Ropes/Chains and Hooks",
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

            hoist_slew_id = vals.get("hoist_slew_id")

            if hoist_slew_id:

                hoist_slew = self.env[
                    "hoist.slew.report"
                ].browse(hoist_slew_id)

                if hoist_slew.exists():

                    vals.update({
                        "sequence": hoist_slew.sequence,
                        "item_detail": hoist_slew.item_detail,
                        "is_section":hoist_slew.is_section,
                        "sort_order": hoist_slew.sort_order,
                    })

        return super().create(vals_list)