from odoo import models, fields, api

class DeliveryPoint(models.Model):
    _name = 'delivery.point'
    _description = 'Delivery Point'

    name = fields.Char('Name')
