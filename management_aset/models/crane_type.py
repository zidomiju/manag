from odoo import fields,models,_ 

class TypeCrane(models.Model):
    _name="type.crane"
    _description="Type Crane"
    _rec_name="name"

    name=fields.Char(string="Type")