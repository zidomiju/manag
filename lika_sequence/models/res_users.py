from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResUsers(models.Model):
    _inherit = 'res.users'

    initials = fields.Char(
        string='Initials', 
        size=2, 
        required=True,
        help="Used for document sequence numbering (e.g., LK for Lika Crane)."
    )

    @api.onchange('initials')
    def _onchange_initials_uppercase(self):
        """Capitalizes the input in real time within the UI."""
        if self.initials:
            self.initials = self.initials.upper()

    @api.constrains('initials')
    def _check_unique_initials(self):
        """Ensures case-insensitive uniqueness across all records."""
        for user in self:
            if user.initials:
                # '=ilike' handles case-insensitive SQL matching ('zd' == 'ZD')
                duplicate = self.search([
                    ('initials', '=ilike', user.initials),
                    ('id', '!=', user.id)
                ], limit=1)
                if duplicate:
                    raise ValidationError(
                        _("The initials '%s' are already assigned to %s, please choose another initilas.") % (user.initials.upper(), duplicate.name)
                    )

    @api.model_create_multi
    def create(self, vals_list):
        """Forces uppercase conversion on record creation (API, imports, forms)."""
        for vals in vals_list:
            if vals.get('initials'):
                vals['initials'] = vals['initials'].upper()
        return super().create(vals_list)

    def write(self, vals):
        """Forces uppercase conversion on record updates."""
        if vals.get('initials'):
            vals['initials'] = vals['initials'].upper()
        return super().write(vals)



# class HrEmployee(models.Model):
#     _inherit = 'hr.employee'

#     initials = fields.Char(
#         related='user_id.initials', 
#         readonly=False, 
#         string="Initials",
#         help="Used for document sequence numbering (e.g., LK for Lika Crane)."
#     )