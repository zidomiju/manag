from odoo import fields,models,_ 

class ServiceMaintenanceHistory(models.Model):
    _name="service.maintenance.history"


    service_trans_his_id=fields.Many2one(
        'service.transaction.history',
        string='Crane'
    )

    serial_number=fields.Char(
        string="Serial Number",
        related="service_trans_his_id.serial_number",
        store=True,
        readonly=True
    )

    date=fields.Date(
        string="Date"
    )
    model_id=fields.Many2one(
        'crane.model',
        string="Crane Model",
        related="service_trans_his_id.model_id",
        store=True,
        readonly=True
    )
    
    service_provider=fields.Char(string="Service Provider")
    next_inspection=fields.Date(string="Next Inspection")
    notes=fields.Text(string="Description")

    service_type_id=fields.Many2one(
            'service.type',
            string="Service Type",
            required=True
        )
    document_ids=fields.One2many('document.service.history',
                                 'service_maintenance_history_id',
                                 string="Upload")
    
class ServiceType(models.Model):
    _name="service.type"
    _description="Type of Service for LIKA"
    _rec_name="name"

    name=fields.Char(string="Service Type")

class DocumentMaintenanceHistory(models.Model):
    _name="document.service.history"
    _description="Document upload fro Service Maintenance History"
    _rec_name="name"

    name=fields.Char("Name")
    file_upload=fields.Binary(string="Upload")
    service_maintenance_history_id=fields.Many2one(
        'service.maintenance.history',
        string="Service Maintenance History",
        ondelete='cascade'
    )

    def action_view_file(self):
        self.ensure_one()

        return {
            'type':'ir.actions.act_url',
            'url': '/web/content/document.service.history/%s/file_upload/%s?download=false' % (
                self.id,
                self.name,
            ),
            'target':'new',
        }



