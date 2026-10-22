from odoo import fields, models, _ 

class TypeVesselPlatform(models.Model):
    _name="type.vessel.platform"
    _description="Type for Vessel or Platform"
    _rec_name="name"

    name=fields.Char(string="String", required=True)

class ClassVesselPlatform(models.Model):
    _name="class.vessel.platform"
    _description="This is for registering class for Vessel"
    _rec_name="name"

    name=fields.Char(string="Class", required=True)

class RegisteredCountry(models.Model):
    _name="registered.country"
    _description="This is for registering country for Vessel or Platform assests for PT Buana Lintas Khatulistiwa"
    _rec_name="name"

    name=fields.Char(string="Registered", required=True)


class OwnerHistory(models.Model):
    _name="owner.history"
    _description="Owner History"

    owner_id=fields.Many2one(
        'res.partner',
        string="Customer",
        required=True,
    )

    asset_id=fields.Many2one(
        'platform.vessel',
        string="Platform / Vessel",
        ondelete='cascade'
    )

    association=fields.Char(
            string="Association"
    )
    effective_date=fields.Date(
        string="Effective Date"
    )


class HistoryReport(models.Model):
    _name="history.report"
    _description="History Report"
    _rec_name="new_name"

    asset_id=fields.Many2one(
        'platform.vessel',
        string="Asset",
        required=True,
        ondelete="cascade"
    )

    previous_name=fields.Char(
        string="Previous Name"
    )
    
    new_name=fields.Char(
        string="Asset Name",
        required=True
    )
    effective_date=fields.Date(
        string="Effective Date"
    )
