from odoo import fields,models,api,_

class ServiceTransactionHistory(models.Model):
    _name="service.transaction.history"
    _description="Service and Transaction History Per Asset"
    _rec_name="serial_number"

    crane_id=fields.Many2one(
        'crane.registration',
        string="Crane",
        required=True,
        ondelete="cascade"
    )

    serial_number=fields.Char(
        string="Serial Number",
        related="crane_id.serial_number", 
        store=True, 
        readonly=True
    )

    model_id=fields.Many2one(
        'crane.model',
        string="Model",
        related="crane_id.model_id",
        store=True,
        readonly=True
    )

    image_crane=fields.Binary(
        related="crane_id.image_crane",
        store=True,
        readonly=True
    )
    make=fields.Char(
        string="Make",
        related="crane_id.make",
        store=True,
        readonly=True
    )

    type_crane=fields.Char(
        string="Type",
        related="crane_id.type_crane",
        store=True,
        readonly=True
    )

    year_built=fields.Char(
        string="Year Built",
        related='crane_id.year_built',
        store=True,
        readonly=True
    )

    customer_id=fields.Many2one(
        'res.partner',
        string="Customer (Current)",
        related="crane_id.customer_id",
        store=True,
        readonly=True
    )


    vessel_platform_id=fields.Many2one(
        'platform.vessel',
        string="Vessel/Platform (current)",
        related="crane_id.vessel_platform_id",
        store=True,
        readonly=True
    )

    country_id=fields.Many2one(
        'registered.country',
        string="Location",
        related="crane_id.vessel_platform_id.country_id",
        store=True,
        readonly=True
    )

    installation_year=fields.Char(
        string="Installation Year",
        related='crane_id.installation_year',
        store=True,
        readonly=True
    )
    status=fields.Selection(
        string="Status",
        related="crane_id.status",
        store=True,
        readonly=True
    )

    document_ids=fields.One2many(
        'document.crane.regist',
        'crane_id',
        string="Documents",
        related="crane_id.document_ids",
        readonly=True
    )
    unit_condition_ids=fields.One2many(
        'unit.condition.report',
        'crane_registration_id',
        string="Unit Condition Report",
        related="crane_id.unit_condition_ids",
        readonly=True,
    )
    service_maintenance_history_ids=fields.One2many(
        'service.maintenance.history',
        'service_trans_his_id',
        string="Service and Maintenance History"
    )