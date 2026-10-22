from odoo import fields, models, _

class DocumentCraneRegist(models.Model):
    _name="document.crane.regist"
    _description="Document Crane Registratation"
    _rec_name="name"


    name=fields.Char(string="Name")
    file=fields.Binary(string="Upload")
    crane_id=fields.Many2one('crane.registration', string="Crane Registration", ondelete='cascade')

    def action_view_file(self):
        self.ensure_one()

        return {
                'type':'ir.actions.act_url',
                'url': '/web/content/document.crane.regist/%s/file/%s?download=false' % (
                    self.id,
                    self.name,
                ),
                'target':'new',
            }