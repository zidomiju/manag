from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_time = fields.Char(
        compute='_compute_delivery_time',
        string='Delivery Time',
        help="Duration between Order Date and Delivery Date, or Expected Date if                                                                                                              Delivery Date is missing."
    )
    delivery_point_id = fields.Many2one('delivery.point', string='Delivery Point                                                                                                             ')
    project_name = fields.Char('Project Name')
    contract_number = fields.Char('Contract Number')
    partner_bank_id = fields.Many2one('res.partner.bank', string='Recipient Bank                                                                                                             ')
    po_customer_number = fields.Char('PO Customer')
    no_proforma_invoice = fields.Char('No Proforma Invoice')

    @api.depends('date_order','commitment_date','expected_date')
    def _compute_delivery_time(self):
        for rec in self:
            rec.delivery_time = False
            target_date=rec.commitment_date or rec.expected_date

            if rec.date_order and target_date:
                days=(target_date.date() - rec.date_order.date()).days
                if days < 7:
                    rec.delivery_time=f'{days} Working Days'
                elif days%7==0:
                    rec.delivery_time=f'{int(days/7)} Weeks '
                elif days%30==0:
                    rec.delivery_time=f'{int(days/30)} Months'
                else:
                    rec.delivery_time=f'{days} Working Days'

class SaleOrderLine(models.Model):
    _inherit="sale.order.line"
    delivery=fields.Char(string="Delivery")
    