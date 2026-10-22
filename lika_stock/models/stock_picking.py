from odoo import models, fields, api

ROMAN_MONTH = ['', 'I', 'II', 'III', 'IV', 'V', 'VI',
               'VII', 'VIII', 'IX', 'X', 'XI', 'XII']


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    cipl_delivery_no = fields.Char(
        string='Delivery No.',
        compute='_compute_cipl_delivery_no',
        store=True,
    )

    @api.depends('name', 'scheduled_date', 'company_id')
    def _compute_cipl_delivery_no(self):
        for picking in self:
            # If the picking doesn't have a name or scheduled date yet, skip it
            if not picking.name or not picking.scheduled_date:
                picking.cipl_delivery_no = ''
                continue
            
            # Call helpers on the specific 'picking' record, not 'self'
            company_code = picking._get_company_code()
            seq = picking._get_sequence_number()
            month = ROMAN_MONTH[picking.scheduled_date.month]
            year = picking.scheduled_date.year
            
            picking.cipl_delivery_no = f"{seq}/{company_code}/OUT/{month}/{year}"

    def _get_company_code(self):
        """Ensure we are only processing one record"""
        self.ensure_one()
        # Customize per company, or extract from name
        # For PT. Buana Lintas Khatulistiwa → LIKA
        company = self.company_id
        code_map = {
            'PT. Buana Lintas Khatulistiwa': 'LIKA',
            'PT Kartika Samudra Adijaya': 'KSA',
        }
        for key, val in code_map.items():
            if key.lower() in company.name.lower():
                return val
        return ''.join(w[0] for w in company.name.split()[:4]).upper()

    def _get_sequence_number(self):
        """Ensure we are only processing one record"""
        self.ensure_one()
        # Extract numeric portion from picking name (WH/OUT/00002 → 00002)
        if self.name:
            parts = self.name.split('/')
            return parts[-1].zfill(5)
        return '00000'