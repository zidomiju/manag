from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit="purchase.order"

    delivery_address=fields.Char(string="Delivery Address")
    project_number=fields.Char(string="Internal Ref")

    def action_print_custom_purchase_order(self):
        self.ensure_one()

        report = self.env.ref(
            'lika_purchase.action_purchase_order_report'
        )

        return report.report_action(self)
