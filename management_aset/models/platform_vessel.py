from odoo import models, fields, api
from odoo.exceptions import UserError


class SalesOrder(models.Model):
    _inherit="sale.order"

    platform_vessel_id=fields.Many2one('platform.vessel', string='Vessel / Platform')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.platform_vessel_id=False

class PlatformVessel(models.Model):
    _name = 'platform.vessel'
    _description = 'This is for registering platform or vessel assets'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    type_asset = fields.Selection([
        ('1', 'Vessel'),
        ('2', 'Platform')
    ], string='Type Asset', required=True)

    status_asset=fields.Selection([
        ('1','Active'),
        ('2','Inactive')
    ])

    name = fields.Char(
        string="Vessel / Platform",
        required=True,
        tracking=True
    )

    previous_name = fields.Char(
        string="Previous Name",
        tracking=True
    )

    latest_effective_date=fields.Date(
        string="Effective Date",
        compute="_compute_latest_effective_date",
        store=True
    )
    imo_llods = fields.Char(
        string='IMO/Lloyds',
        tracking=True
    )

    ship_yard = fields.Char(
        string='Ship Yard',
        tracking=True
    )

    year_built = fields.Char(
        string='Year Built',
        size=4
    )

    hull_number = fields.Char(
        string='Hull No',
        tracking=True
    )

    class_id = fields.Many2one(
        'class.vessel.platform',
        string='Class'
    )

    type_id = fields.Many2one(
        'type.vessel.platform',
        string='Type'
    )

    country_id = fields.Many2one(
        'registered.country',
        string='Registered'
    )

    credit_status = fields.Selection([
        ('0', 'Bad'),
        ('1', 'Good')
    ])

    credit_limit = fields.Float(
        string='Credit Limit'
    )

    notes = fields.Html(
        string='Notes'
    )

    image_asset = fields.Binary()

    name_history_ids = fields.One2many(
        'history.report',
        'asset_id',
        string='Name History'
    )

    service_report_ids = fields.One2many(
        'service.report',
        'asset_id',
        string='Service Report'
    )

    manual_report_ids = fields.One2many(
        'manuals.report',
        'asset_id',
        string='Manual Report'
    )

    drawing_report_ids = fields.One2many(
        'drawings.report',
        'asset_id',
        string='Drawings Report'
    )

    correspondence_report_ids = fields.One2many(
        'correspondence.report',
        'asset_id',
        string='Correspondence Report'
    )

    image_report_ids = fields.One2many(
        'image.report',
        'asset_id',
        string='Image'
    )

    crane_regist_ids = fields.One2many(
        'crane.registration',
        'vessel_platform_id',
        string="Crane Registration"
    )

    owner_history_ids = fields.One2many(
        'owner.history',
        'asset_id',
        string='Owner History',
    )

    current_owner_id=fields.Many2one(
        'res.partner',
        string="Current Client",
        compute='_compute_current_owner',
        store=True,
    )
    quatation_sales_ids=fields.One2many(
        'sale.order',
        'platform_vessel_id',
        string="Quatation and Order History"
    )
    @api.depends(
            'owner_history_ids.owner_id',
            'owner_history_ids.effective_date',
    )

    def _compute_current_owner(self):
        for record in self:
            latest_owner=self.env['owner.history'].search(
                [
                    ('asset_id','=',record.id),
                    ('owner_id','!=',False)
                ],
                order='effective_date desc, id desc',
                limit=1
            )

            record.current_owner_id =(latest_owner.owner_id if latest_owner else False)
    @api.model
    def create(self, vals):
        record = super().create(vals)

        record.previous_name = record.name

        self.env['history.report'].create({
            'asset_id': record.id,
            'previous_name': record.name,
            'new_name': record.name,
            'effective_date': fields.Date.context_today(record),
        })

        return record

    def write(self, vals):

        old_names = {
            record.id: record.name
            for record in self
        }


        res = super().write(vals)

        if 'name' in vals:

            History = self.env['history.report']

            for record in self:
                old_name = old_names.get(record.id)
                new_name = record.name

                if old_name and old_name != new_name:

                    record.previous_name = old_name

                    History.create({
                        'asset_id': record.id,
                        'previous_name': old_name,
                        'new_name': new_name,
                        'effective_date': fields.Date.context_today(record),
                    })

        return res

    @api.depends(
        'name_history_ids.effective_date',
        'name_history_ids.asset_id'
    )
    def _compute_latest_effective_date(self):
        for record in self:
            latest_history=self.env['history.report'].search(
                [
                    ('asset_id', '=', record.id)
                ],
                order='effective_date desc, id desc',
                limit=1
            )

            record.latest_effective_date=(
                latest_history.effective_date
                if latest_history
                else False
            )

    def unlink(self):
        for record in self:
            if record.crane_regist_ids:
                raise UserError(
                    "Vessel/Platform cannot be delete because it has Crane Registation data. Please delete the Crane Registration first"
                )
        return super().unlink()