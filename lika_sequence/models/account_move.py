from odoo import _, api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    # Replace to use specific sequence for customer invoice
    @api.depends("state", "journal_id", "date")
    def _compute_name_by_sequence(self):
        for move in self:
            name = move.name or "/"
            # I can't use posted_before in this IF because
            # posted_before is set to True in _post() at the same
            # time as state is set to "posted"
            if (
                move.state == "posted"
                and (not move.name or move.name == "/")
                and move.journal_id
                and move.journal_id.sequence_id
            ):
                if (
                    move.move_type in ("out_refund", "in_refund")
                    and move.journal_id.type in ("sale", "purchase")
                    and move.journal_id.refund_sequence
                    and move.journal_id.refund_sequence_id
                ):
                    seq = move.journal_id.refund_sequence_id
                else:
                    # Custom sequence for customer invoice
                    if move.move_type == 'out_invoice' and move.journal_id.type in ("sale", "purchase"):
                        seq = self.env.ref('lika_sequence.seq_account_move_invoice')
                    else:
                        seq = move.journal_id.sequence_id

                # next_by_id(date) only applies on ir.sequence.date_range selection
                # => we use with_context(ir_sequence_date=date).next_by_id()
                # which applies on ir.sequence.date_range selection AND prefix
                name = seq.with_context(ir_sequence_date=move.date).next_by_id()
            move.name = name
        # Force compute of sequence_prefix and sequence_number
        self._compute_split_sequence()
        # Force compute of fields depending on name
        self._inverse_name()

