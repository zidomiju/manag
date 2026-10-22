from odoo import api, fields, models, _


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def action_new_quotation(self):
        action = super().action_new_quotation()
        action['context'].update({'default_is_verification_order': True})
        return action
    
    def action_view_sale_quotation(self):
        action = super().action_view_sale_quotation()
        action['context'].update({'default_is_verification_order': True})
        action['context'].pop('search_default_draft')
        action['name'] = 'Verification Order'
        action['display_name'] = 'Verification Order'
        return action


