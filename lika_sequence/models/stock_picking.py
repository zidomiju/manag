from odoo import _, api, fields, models

class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for rec in res:
            # Set custom sequence for delivery orders
            if rec.code == 'outgoing' and rec.sequence_id:
                rec.sequence_id.write({
                    'code': f'sec.delivery.order.lika.{rec.id}',
                    'prefix': False,
                    'suffix': f'/LIKA/{rec.sequence_code}/%(range_rom_month)s/%(range_year)s',
                    'padding': 3,
                    'use_date_range': True,
                    'range_reset': 'yearly'
                })
        return res
    
    def write(self, vals):
        res = super().write(vals)
        # Update sequence if sequence_code is changed
        if 'sequence_code' in vals:
            for picking_type in self:
                if picking_type.code == 'outgoing':
                    if picking_type.warehouse_id:
                        picking_type.sequence_id.sudo().write({
                            'name': _('%(warehouse)s Sequence %(code)s', warehouse=picking_type.warehouse_id.name, code=vals['sequence_code']),
                            'prefix': False,
                            'suffix': f'/LIKA/{vals['sequence_code']}/%(range_rom_month)s/%(range_year)s',
                            'padding': 3,
                            'use_date_range': True,
                            'range_reset': 'yearly'
                        })
                    else:
                        picking_type.sequence_id.sudo().write({
                            'name': _('Sequence %(code)s', code=vals['sequence_code']),
                            'prefix': False,
                            'suffix': f'/LIKA/{vals['sequence_code']}/%(range_rom_month)s/%(range_year)s',
                            'padding': 3,
                            'use_date_range': True,
                            'range_reset': 'yearly'
                        })
        return res
