from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Section 3: Payment & Tax Info
    npwp_number = fields.Char(string='No. NPWP')
    # npwp_file = fields.Binary(string='NPWP Document', attachment=True)
    # npwp_filename = fields.Char(string='NPWP File Name')

    sppkp_number = fields.Char(string='No. SPPKP')
    # sppkp_file = fields.Binary(string='SPPKP Document', attachment=True)
    # sppkp_filename = fields.Char(string='SPPKP File Name')

    bank_name = fields.Char(string='Nama Bank')
    bank_account_number = fields.Char(string='No. Rekening Bank')
    term_of_payment = fields.Char(string='Term of Payment (TOP)')

    # Section 4: Extra / Optional Documents (One2many -> dynamic list)
    extra_document_ids = fields.One2many(
        'vendor.extra.document', 
        'partner_id', 
        string='Extra Documents'
    )

    # Inverse relation pointing back to product.supplierinfo
    supplierinfo_ids = fields.One2many(
        'product.supplierinfo', 
        'partner_id', 
        string='Mapped Vendor Products'
    )

    is_customer = fields.Boolean(
        string='Is a Customer',
        compute='_compute_partner_type',
        store=True,
        readonly=False,
        default=lambda self: self.env.context.get('res_partner_search_mode') == 'customer' or self.env.context.get('default_customer_rank', 0) > 0
    )

    is_vendor = fields.Boolean(
        string='Is a Vendor',
        compute='_compute_partner_type',
        store=True,
        readonly=False,
        default=lambda self: self.env.context.get('res_partner_search_mode') == 'supplier' or self.env.context.get('default_supplier_rank', 0) > 0
    )

    @api.depends('customer_rank', 'supplier_rank')
    def _compute_partner_type(self):
        for partner in self:
            if partner.customer_rank > 0:
                partner.is_customer = True
            if partner.supplier_rank > 0:
                partner.is_vendor = True

    # @api.constrains('child_ids', 'company_type', 'parent_id')
    # def _check_company_pic_required(self):
    #     for partner in self:
    #         # RULE 1: If the user chose "Person", NEVER demand a child contact
    #         if partner.company_type == 'person':
    #             continue

    #         # RULE 2: If this is a child contact (PIC) linked to a parent, skip
    #         if partner.parent_id:
    #             continue

    #         # RULE 3: Only enforce for top-level Companies
    #         if partner.company_type == 'company' and not partner.child_ids:
    #             raise ValidationError(
    #                 f"Perusahaan '{partner.name or 'ini'}' wajib memiliki minimal 1 Contact Person (PIC)!"
    #             )


class VendorExtraDocument(models.Model):
    _name = 'vendor.extra.document'
    _description = 'Vendor Extra Documents'

    partner_id = fields.Many2one('res.partner', string='Vendor', ondelete='cascade')
    name = fields.Char(string='Document Description', required=True)
    upload_date = fields.Date(string='Uploaded On', default=fields.Date.context_today)
    file_name = fields.Char(string='File Name')
    file_data = fields.Binary(string='File', filename="file_name", required=True)

    def action_view_file(self):
        self.ensure_one()
        if not self.file_data:
            raise UserError("Belum ada file yang di unggah.")

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self._name}/{self.id}/file_data/{self.file_name}',
            'target': 'new',
        }