from odoo import fields, models, api


class UnitConditionResult(models.Model):
    _name = "unit.condition.result5"
    _description = "Unit Condition Result 5"
    _order = "sort_order, id"

    unit_condition_id = fields.Many2one(
        "unit.condition.report",
        string="Unit Condition Report",
        required=True,
        ondelete="cascade",
    )

    wire_hook_id = fields.Many2one(
        "wire.hooks.report",
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

            wire_hook_id = vals.get("wire_hook_id")

            if wire_hook_id:

                wire_hook = self.env[
                    "wire.hooks.report"
                ].browse(wire_hook_id)

                if wire_hook.exists():

                    vals.update({
                        "sequence": wire_hook.sequence,
                        "item_detail": wire_hook.item_detail,
                        "is_section":wire_hook.is_section,
                        "sort_order": wire_hook.sort_order,
                    })

        return super().create(vals_list)