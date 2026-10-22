from odoo import fields, models, api


class UnitConditionResult(models.Model):
    _name = "unit.condition.result8"
    _description = "Unit Condition Result 8"
    _order = "sort_order, id"

    unit_condition_id = fields.Many2one(
        "unit.condition.report",
        string="Unit Condition Report",
        required=True,
        ondelete="cascade",
    )

    hydraulic_pneumatic_id = fields.Many2one(
        "hydraulic.pneumatic.report",
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

            hydraulic_pneumatic_id = vals.get("hydraulic_pneumatic_id")

            if hydraulic_pneumatic_id:

                hydraulic_pneumatic = self.env[
                    "hydraulic.pneumatic.report"
                ].browse(hydraulic_pneumatic_id)

                if hydraulic_pneumatic.exists():

                    vals.update({
                        "sequence": hydraulic_pneumatic.sequence,
                        "item_detail": hydraulic_pneumatic.item_detail,
                        "is_section":hydraulic_pneumatic.is_section,
                        "sort_order": hydraulic_pneumatic.sort_order,
                    })

        return super().create(vals_list)