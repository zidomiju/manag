from odoo import models, fields, api, _
from odoo.exceptions import UserError


class VerificationOrder(models.Model):
    _inherit = 'sale.order'

    # =============================================================
    # VERIFICATION ORDER
    # =============================================================

    is_verification_order = fields.Boolean(
        string='Verification Order',
        default=False,
        copy=False,
    )

    vo_state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled'),
    ],
        string='VO Status',
        default='draft',
        tracking=True,
        copy=False,
    )

    # =============================================================
    # LEGACY / OLD DATA
    # Tetap dipertahankan agar data lama tidak rusak.
    # =============================================================

    vo_id = fields.Many2one(
        'sale.order',
        string='VO Reference',
        copy=False,
    )

    is_all_quotation_created = fields.Boolean(
        compute='_compute_is_all_quotation_created',
        string='All Quotation Created',
    )

    @api.depends('order_line.vo_quotation_id')
    def _compute_is_all_quotation_created(self):
        for rec in self:
            if rec.is_verification_order:
                rec.is_all_quotation_created = all(
                    line.vo_quotation_id
                    for line in rec.order_line
                    if not line.display_type
                )
            else:
                rec.is_all_quotation_created = False

    # =============================================================
    # CREATE
    # =============================================================

    @api.model_create_multi
    def create(self, vals_list):

        orders = super().create(vals_list)

        for order in orders:

            # -----------------------------------------------------
            # DATA LAMA / SYSTEM CREATE
            # Jangan mengubah VO yang memang sudah dibuat
            # dengan workflow lama.
            # -----------------------------------------------------
            if order.is_verification_order:
                continue

            # -----------------------------------------------------
            # DATA BARU
            #
            # Quotation standard Odoo otomatis menjadi
            # Verification Order.
            #
            # TIDAK membuat record baru.
            # -----------------------------------------------------
            order.write({
                'is_verification_order': True,
                'vo_state': 'confirm',
            })

        return orders

    # =============================================================
    # OLD VERIFICATION ORDER WORKFLOW
    # Dipertahankan untuk data lama.
    # =============================================================

    def action_draft_vo(self):
        for rec in self:
            rec.vo_state = 'draft'

    def action_confirm_vo(self):
        for rec in self:
            rec.vo_state = 'confirm'

    def action_cancel_vo(self):
        for rec in self:
            rec.vo_state = 'cancel'

    # =============================================================
    # OLD CREATE QUOTATION
    #
    # Dipertahankan agar VO lama yang belum melakukan
    # Create Sales Order tidak kehilangan workflow.
    # =============================================================

    def action_create_quotation(self):

        for rec in self:

            # -----------------------------------------------------
            # Validation
            # -----------------------------------------------------

            if not rec.order_line:
                raise UserError(
                    _("Order lines cannot be empty.")
                )

            # =====================================================
            # PARTIAL
            # =====================================================

            partial_lines = rec.order_line.filtered(
                lambda line:
                    line.is_partial
                    and not line.vo_quotation_id
            )

            if partial_lines:

                vals = {
                    'vo_id': rec.id,
                    'partner_id': rec.partner_id.id,
                    'date_order': rec.date_order,
                    'validity_date': rec.validity_date,
                    'pricelist_id': rec.pricelist_id.id,
                    'payment_term_id': rec.payment_term_id.id,
                    'delivery_point_id': rec.delivery_point_id.id,
                    'commitment_date': rec.commitment_date,
                }

                order_line = []

                for line in partial_lines:

                    if line.display_type:

                        order_line.append((
                            0,
                            0,
                            {
                                'display_type': line.display_type,
                                'name': line.name,
                            }
                        ))

                    else:

                        order_line.append((
                            0,
                            0,
                            {
                                'product_id': line.product_id.id,
                                'name': line.product_id.display_name,
                                'product_uom_qty': line.product_uom_qty,
                                'price_unit': line.price_unit,
                                'tax_ids': [(6, 0, line.tax_ids.ids)],
                            }
                        ))

                vals['order_line'] = order_line

                quotation = self.env[
                    'sale.order'
                ].with_context(
                    skip_auto_verification_order=True
                ).create(vals)

                partial_lines.write({
                    'vo_quotation_id': quotation.id
                })

                continue

            # =====================================================
            # NON-PARTIAL
            # =====================================================

            normal_lines = rec.order_line.filtered(
                lambda line:
                    not line.is_partial
                    and not line.vo_quotation_id
            )

            if normal_lines:

                vals = {
                    'vo_id': rec.id,
                    'partner_id': rec.partner_id.id,
                    'date_order': rec.date_order,
                    'validity_date': rec.validity_date,
                    'pricelist_id': rec.pricelist_id.id,
                    'payment_term_id': rec.payment_term_id.id,
                    'delivery_point_id': rec.delivery_point_id.id,
                    'commitment_date': rec.commitment_date,
                }

                order_line = []

                for line in normal_lines:

                    if line.display_type:

                        order_line.append((
                            0,
                            0,
                            {
                                'display_type': line.display_type,
                                'name': line.name,
                            }
                        ))

                    else:

                        order_line.append((
                            0,
                            0,
                            {
                                'product_id': line.product_id.id,
                                'name': line.product_id.display_name,
                                'product_uom_qty': line.product_uom_qty,
                                'price_unit': line.price_unit,
                                'tax_ids': [(6, 0, line.tax_ids.ids)],
                            }
                        ))

                vals['order_line'] = order_line

                quotation = self.env[
                    'sale.order'
                ].with_context(
                    skip_auto_verification_order=True
                ).create(vals)

                normal_lines.write({
                    'vo_quotation_id': quotation.id
                })

        return True


# =============================================================
# SALE ORDER LINE
# =============================================================

class VerificationOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Legacy fields.
    # Tetap ada agar data Verification Order lama aman.

    is_partial = fields.Boolean(
        string='Partial',
        copy=False,
    )

    vo_quotation_id = fields.Many2one(
        'sale.order',
        string='Quotation',
        copy=False,
    )