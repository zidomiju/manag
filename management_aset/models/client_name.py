from odoo import fields, models, _ 

class ClientName(models.Model):
    _name="client.name"
    _description="Define Personnel Met During Visit"
    _rec_name="name"

    name=fields.Char(string="Name", required=True)
    job_title=fields.Char(string="Job Title", required=True)
    unit_condition_id=fields.Many2one('unit.condition.report',string="Client Personnel Met During Visit")
    