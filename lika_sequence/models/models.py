import roman
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    def _get_prefix_suffix(self, date=None, date_range=None):
        def _interpolate(s, d):
            return (s % d) if s else ''

        def _interpolation_dict():
            now = range_date = effective_date = datetime.now(self.env.tz)
            if date or self.env.context.get('ir_sequence_date'):
                effective_date = fields.Datetime.from_string(
                    date or self.env.context.get('ir_sequence_date'))
            if date_range or self.env.context.get('ir_sequence_date_range'):
                range_date = fields.Datetime.from_string(
                    date_range or self.env.context.get('ir_sequence_date_range'))

            sequences = {
                'year': '%Y', 'month': '%m', 'day': '%d', 'y': '%y', 'doy': '%j', 'woy': '%W',
                'weekday': '%w', 'h24': '%H', 'h12': '%I', 'min': '%M', 'sec': '%S',
                'isoyear': '%G', 'isoy': '%g', 'isoweek': '%V',
                'rom_year': '%Y', 'rom_month': '%m', 'rom_y': '%y', 'rom_day': '%d'
            }
            res = {}
            for key, format in sequences.items():
                if "rom_" in key:
                    res[key] = roman.toRoman(int(effective_date.strftime(format)))
                    res['range_' + key] = roman.toRoman(int(range_date.strftime(format)))
                    res['current_' + key] = roman.toRoman(int(now.strftime(format)))
                else:
                    res[key] = effective_date.strftime(format)
                    res['range_' + key] = range_date.strftime(format)
                    res['current_' + key] = now.strftime(format)

            # --- Read User Initials ---
            user_id = self.env.context.get('user_id') or self.env.uid
            user = self.env['res.users'].browse(user_id)
            
            # Direct user initials check
            if user and not user.initials:
                raise UserError(_('User "%s" does not have initials set. Please define initials in the user profile.', user.name))

            res['user_initials'] = user.initials or ''
            return res

        self.ensure_one()
        d = _interpolation_dict()
        try:
            interpolated_prefix = _interpolate(self.prefix, d)
            interpolated_suffix = _interpolate(self.suffix, d)
        except (ValueError, TypeError, KeyError):
            raise UserError(_('Invalid prefix or suffix for sequence “%s”', self.name))

        return interpolated_prefix, interpolated_suffix


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                seq_date = fields.Datetime.to_datetime(vals.get('date_order'))
                user_id = vals.get('user_id') or self.env.uid
                vals['name'] = self.env['ir.sequence'].with_context(
                    ir_sequence_date=seq_date,
                    user_id=user_id
                ).next_by_code('sale.order') or _('New')
        return super().create(vals_list)

# import roman
# from datetime import datetime
# from odoo import models, fields, api, _
# from odoo.exceptions import UserError


# class IrSequence(models.Model):
#     _inherit = 'ir.sequence'

#     # Replace to add roman numeral support
#     def _get_prefix_suffix(self, date=None, date_range=None):
#         def _interpolate(s, d):
#             return (s % d) if s else ''

#         def _interpolation_dict():
#             now = range_date = effective_date = datetime.now(self.env.tz)
#             if date or self.env.context.get('ir_sequence_date'):
#                 effective_date = fields.Datetime.from_string(
#                     date or self.env.context.get('ir_sequence_date'))
#             if date_range or self.env.context.get('ir_sequence_date_range'):
#                 range_date = fields.Datetime.from_string(
#                     date_range or self.env.context.get('ir_sequence_date_range'))

#             sequences = {
#                 'year': '%Y', 'month': '%m', 'day': '%d', 'y': '%y', 'doy': '%j', 'woy': '%W',
#                 'weekday': '%w', 'h24': '%H', 'h12': '%I', 'min': '%M', 'sec': '%S',
#                 'isoyear': '%G', 'isoy': '%g', 'isoweek': '%V',

#                 # Additional dict for roman
#                 'rom_year': '%Y', 'rom_month': '%m',
#                 'rom_y': '%y', 'rom_day': '%d'
#             }
#             res = {}
#             for key, format in sequences.items():
#                 if "rom_" in key:
#                     # Convert to Roman
#                     res[key] = roman.toRoman(int(
#                         effective_date.strftime(format)))
#                     res['range_' + key] = roman.toRoman(
#                         int(range_date.strftime(format)))
#                     res['current_' + key] = roman.toRoman(int(now.strftime(format)))
#                 else:
#                     res[key] = effective_date.strftime(format)
#                     res['range_' + key] = range_date.strftime(format)
#                     res['current_' + key] = now.strftime(format)
#             return res
        
#         self.ensure_one()
#         d = _interpolation_dict()
#         try:
#             interpolated_prefix = _interpolate(self.prefix, d)
#             interpolated_suffix = _interpolate(self.suffix, d)
#         except (ValueError, TypeError, KeyError):
#             raise UserError(_('Invalid prefix or suffix for sequence “%s”', self.name))

#         return interpolated_prefix, interpolated_suffix

