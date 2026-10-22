from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit="purchase.order"

    delivery_address=fields.Char(string="Delivery Address")
    project_number=fields.Char(string="Internal Ref")