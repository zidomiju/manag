from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    kwitansi_number = fields.Char(compute='_compute_kwitansi_number', string='Kwitansi Number', store=True)
    kwitansi_note = fields.Char('Notes')

    @api.depends('name')
    def _compute_kwitansi_number(self):
        for rec in self:
            if rec.move_type == 'out_invoice' and rec.name and rec.name != '/':
                rec.kwitansi_number = rec.name.replace('INV', 'KWT')
            else:
                rec.kwitansi_number = False
