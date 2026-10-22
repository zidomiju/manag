from odoo import _, api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    invoice_report_sign_id = fields.Many2one('res.users', string='Invoice Report Sign')
