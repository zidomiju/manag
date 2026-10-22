from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _prepare_report_packing_list(self):
        for rec in self:
            packages = rec.move_ids.mapped('package_ids')
            packing_list = []
            for packing in packages:
                filter = rec.move_line_ids.filtered(lambda x: x.result_package_id == packing)
                packing_list.append({
                    'name': packing.name,
                    'package_type': packing.package_type_id,
                    'line': filter
                })
            return packing_list



