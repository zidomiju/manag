from odoo import fields, models, api


class UnitConditionResult(models.Model):
    _name = "unit.condition.result2"
    _description = "Unit Condition Result 2"
    _order = "sort_order, id"

    unit_condition_id = fields.Many2one(
        "unit.condition.report",
        string="Unit Condition Report",
        required=True,
        ondelete="cascade",
    )

    general_visual_id = fields.Many2one(
        "general.visual.report",
        string="General Visual ",
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

            general_visual_id = vals.get("general_visual_id")

            if general_visual_id:

                general_visual = self.env[
                    "general.visual.report"
                ].browse(general_visual_id)

                if general_visual.exists():

                    vals.update({
                        "sequence": general_visual.sequence,
                        "item_detail": general_visual.item_detail,
                        "is_section":general_visual.is_section,
                        "sort_order": general_visual.sort_order,
                    })

        return super().create(vals_list)