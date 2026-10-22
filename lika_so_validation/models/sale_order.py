from odoo import models, fields, api, _
from odoo.exceptions import UserError
import re


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model_create_multi
    def create(self, vals_list):
        """
        Quotation dibuat langsung menggunakan workflow
        standard Odoo.

        Tidak membutuhkan Verification Order terlebih dahulu.
        """
        return super().create(vals_list)

    def action_confirm(self):
        today = fields.Date.today()

        for order in self:

            # =========================================================
            # 1. CHECK CANCELLED
            # =========================================================
            if order.state == 'cancel':
                raise UserError(_(
                    "Cannot confirm a cancelled quotation. "
                    "Please reactivate or reset it to draft first."
                ))

            # =========================================================
            # 2. CHECK EXPIRATION
            # =========================================================
            if (
                order.validity_date
                and order.validity_date < today
            ):
                raise UserError(_(
                    "Cannot confirm quotation %s because it expired "
                    "on %s. Please update the expiration date or "
                    "create a revision first."
                ) % (
                    order.name,
                    order.validity_date,
                ))

            # =========================================================
            # 3. CHECK CUSTOMER PO
            # =========================================================
            attachments = self.env['ir.attachment'].search([
                ('res_model', '=', 'sale.order'),
                ('res_id', '=', order.id),
            ])

            has_valid_po = any(
                re.search(
                    r'(?i)(^|[\s\_.-])po([\s\_.-]|$)',
                    attachment.name or ''
                )
                for attachment in attachments
            )

            if not has_valid_po:
                raise UserError(_(
                    'Cannot create Sales Order from Quotation.\n\n'
                    'A Customer Purchase Order (PO) must be uploaded '
                    'first.\n\n'
                    'Please follow these steps:\n'
                    '1. Go to the chatter section below or on the side\n'
                    '2. Click the attachment icon (paperclip)\n'
                    '3. Upload your Customer PO document\n'
                    '4. Ensure the filename contains "PO" or "po"\n'
                    '5. Then confirm the quotation to create a '
                    'Sales Order'
                ))

        return super().action_confirm()

