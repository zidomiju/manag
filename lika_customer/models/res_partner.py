from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    billing_addr = fields.Char(string='Alamat Penagihan (Jika berbeda dari Alamat Perusahaan)', help='Alamat penagihan untuk faktur dan dokumen terkait.')
    payment_method = fields.Char(string='Metode Pembayaran', help='Metode pembayaran yang disepakati dengan klien.')

    # Section 3: Billing & PKP Info
    pkp_type = fields.Selection([
        ('wapu', 'PKP WAPU'),
        ('pkp', 'PKP'),
        ('non_pkp', 'Non-PKP')
    ], string='Jenis Pengusaha Kena Pajak (PKP)', default='pkp')

    # Section 4: Dynamic Customer Document Table
    customer_document_ids = fields.One2many(
        'customer.document', 
        'partner_id', 
        string='Dokumen Klien'
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
    #             print("### DEBUG: Partner is a person, skipping PIC check.")
    #             continue

    #         # RULE 2: If this is a child contact (PIC) linked to a parent, skip
    #         if partner.parent_id:
    #             continue

    #         # RULE 3: Only enforce for top-level Companies
    #         if partner.company_type == 'company' and not partner.child_ids:
    #             print("### DEBUG: Partner is a company with no child contacts, raising ValidationError.")
    #             raise ValidationError(
    #                 f"Perusahaan '{partner.name or 'ini'}' wajib memiliki minimal 1 Contact Person (PIC)!"
    #             )

    def action_submit_customer(self):
        """Action for the bottom Submit button to trigger save and validation"""
        return True


class CustomerDocument(models.Model):
    _name = 'customer.document'
    _description = 'Customer Attachments'

    partner_id = fields.Many2one('res.partner', string='Customer', ondelete='cascade')
    name = fields.Char(string='Nama Dokumen', required=True)
    file_name = fields.Char(string='File Name')
    file_data = fields.Binary(string='Upload Dokumen', filename="file_name", required=True)

    def action_view_file(self):
            self.ensure_one()
            if not self.file_data:
                raise UserError("Belum ada file yang di unggah.")
    
            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{self._name}/{self.id}/file_data/{self.file_name}',
                'target': 'new',
            }