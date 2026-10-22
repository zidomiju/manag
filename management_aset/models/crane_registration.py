from odoo import fields, models, api, _

class CraneRegistration(models.Model):
    _name='crane.registration'
    _description="Crane Registration for Management Crane PT Buana Lintas Khatulistiwa"
    _inherit=['mail.thread','mail.activity.mixin']
    _rec_name="serial_number"

    crane_name=fields.Char(string="Crane Unit Name", tracking=True, required=True)
    image_crane=fields.Binary()
    status=fields.Selection([
            ('0','Inactive'),
            ('1','Active')
        ],string="Status",required=True)
    serial_number=fields.Char(string="Serial Number", 
                              tracking=True, 
                              required=True)
    model_id=fields.Many2one('crane.model', 
                             string='Crane Model', 
                             required=True)
    make=fields.Char(string='Manufacturer/Make', 
                     related="model_id.make_id.name", 
                     store=True,
                     readonly=True)
    type_crane=fields.Char(string="Type",
                           related="model_id.type_id.type", 
                           store=True, 
                           readonly=True)
    
    make_code=fields.Char(string="Model Code",
                          related="model_id.make_code",
                          store=True, 
                          readonly=True)
    notes=fields.Char(string='Description', size=250)
    
    customer_id=fields.Many2one(
        'res.partner',
        string="Customer / Owner",
    )
    vessel_platform_id=fields.Many2one('platform.vessel',
                                        string="Vessel / Platform", 
                                        required=True)
    type_asset=fields.Selection(string="Type",
                                related="vessel_platform_id.type_asset",
                                store=True,
                                readonly=True)
    year_built=fields.Char(string="Year Built", 
                           size=4, 
                           tracking=True)
    installation_year=fields.Char(string="Installation Year",
                                  size=4,
                                  tracking=True)

    document_ids=fields.One2many('document.crane.regist',
                                 'crane_id', 
                                 string="Documents")

    document_model_ids=fields.One2many(
        string="Crane Model Documents",
        related="model_id.document_ids",
        readonly=True 
    )
    service_history_ids=fields.One2many(
        "service.transaction.history",
        "crane_id",
        string="Service & Transaction History"
    )

    unit_condition_ids=fields.One2many(
        'unit.condition.report',
        'crane_registration_id',
        string='Unit Condition Report'
    )

    @api.onchange('customer_id')
    def _onchange_customer_id(self):
        self.vessel_platform_id=False
    @api.model
    def create(self, vals):
        record=super().create(vals)
        self.env['service.transaction.history'].create({
            'crane_id':record.id,
        })

        return record
