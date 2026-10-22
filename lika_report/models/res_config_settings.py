from odoo import _, api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoice_report_sign_id = fields.Many2one(
        'res.users', string='Invoice Report Sign', related='company_id.invoice_report_sign_id', readonly=False)
