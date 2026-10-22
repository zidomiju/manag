from odoo import models, fields
from odoo.exceptions import UserError

class ProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    warranty_note = fields.Char(string='Catatan / Garansi')
    warranty_file = fields.Binary(string='Dokumen Garansi', filename="warranty_filename", attachment=True)
    warranty_filename = fields.Char(string='File Name Garansi')

    # view manual document action
    def action_view_warranty_file(self):
            self.ensure_one()
            if not self.warranty_file:
                raise UserError("Belum ada file warranty yang di unggah.")
    
            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{self._name}/{self.id}/warranty_file/{self.warranty_filename}',
                'target': 'new',
            }