from odoo import fields, models

class StockMove(models.Model):
    _inherit = 'stock.move'

    dimension = fields.Integer(string="Dimension", tracking=True, default=0)