from odoo import models, fields


class AccountMove(models.Model):
    _inherit="account.move"

    no_po_so=fields.Char(string="No. PO/SO")
    no_contract=fields.Char(string="No. Contract")
    payment_for=fields.Char(string="Payment For")