from odoo import models, fields


class ResBank(models.Model):
    _inherit = "res.bank"

    branch = fields.Char('Branch')
