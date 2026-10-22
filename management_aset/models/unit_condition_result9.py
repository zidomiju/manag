from odoo import fields, models, api


class UnitConditionResult(models.Model):
    _name = "unit.condition.result9"
    _description = "Unit Condition Result 9"
    _order = "sort_order, id"

    unit_condition_id = fields.Many2one(
        "unit.condition.report",
        string="Unit Condition Report",
        required=True,
        ondelete="cascade",
    )

    electrical_system_id = fields.Many2one(
        "electrical.system.report",
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

            electrical_system_id = vals.get("electrical_system_id")

            if electrical_system_id:

                electrical_system = self.env[
                    "electrical.system.report"
                ].browse(electrical_system_id)

                if electrical_system.exists():

                    vals.update({
                        "sequence": electrical_system.sequence,
                        "item_detail": electrical_system.item_detail,
                        "is_section":electrical_system.is_section,
                        "sort_order": electrical_system.sort_order,
                    })

        return super().create(vals_list)