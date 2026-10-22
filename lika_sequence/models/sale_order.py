from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:

            # =========================================================
            # PROFORMA INVOICE SEQUENCE
            # =========================================================
            if not vals.get('no_proforma_invoice'):
                vals['no_proforma_invoice'] = self.env[
                    'ir.sequence'
                ].next_by_code(
                    'lika.proforma.invoice'
                )

            # =========================================================
            # QUOTATION / SALES ORDER SEQUENCE
            # =========================================================
            if vals.get('name', _('New')) == _('New'):

                seq_date = (
                    fields.Datetime.to_datetime(
                        vals.get('date_order')
                    )
                    or fields.Datetime.now()
                )

                user_id = (
                    vals.get('user_id')
                    or self.env.uid
                )

                partner_id = vals.get('partner_id')

                vals['name'] = self.env[
                    'ir.sequence'
                ].with_context(
                    ir_sequence_date=seq_date,
                    user_id=user_id,
                    partner_id=partner_id,
                ).next_by_code(
                    'sale.order'
                ) or _('New')

        return super().create(vals_list)
