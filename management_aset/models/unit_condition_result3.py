from odoo import fields, models, api


class UnitConditionResult(models.Model):
    _name = "unit.condition.result3"
    _description = "Unit Condition Result 3"
    _order = "sort_order, id"

    unit_condition_id = fields.Many2one(
        "unit.condition.report",
        string="Unit Condition Report",
        required=True,
        ondelete="cascade",
    )

    instrumentation_control_id = fields.Many2one(
        "instrumentation.control.report",
        string="Instrumentation Control ",
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

            instrumentation_control_id = vals.get("instrumentation_control_id")

            if instrumentation_control_id:

                instrumentation_control = self.env[
                    "instrumentation.control.report"
                ].browse(instrumentation_control_id)

                if instrumentation_control.exists():

                    vals.update({
                        "sequence": instrumentation_control.sequence,
                        "item_detail": instrumentation_control.item_detail,
                        "is_section":instrumentation_control.is_section,
                        "sort_order": instrumentation_control.sort_order,
                    })

        return super().create(vals_list)