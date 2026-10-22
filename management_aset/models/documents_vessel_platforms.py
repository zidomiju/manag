from odoo import fields, models,_ 

class serviceReport(models.Model):
    _name="service.report"
    _description="Upload Your Document"

    name=fields.Char(string="File Name",required=True)
    file_pdf=fields.Binary(string="Title")
    file_date=fields.Datetime(string="Date", default=fields.Datetime.now,readonly=True)
    asset_id=fields.Many2one(
        'platform.vessel',
        string='Vessel / Platform',
        ondelete='cascade'
    )

    def action_view_file(self):
        self.ensure_one()

        return {
            'type':'ir.actions.act_url',
            'url': '/web/content/service.report/%s/file_pdf/%s?download=false' % (
                self.id,
                self.name,
            ),
            'target':'new',
        }

class drawingsReport(models.Model):
    _name="drawings.report"
    _description="Upload Your Drawing Report"
    _rec_name="name"

    name=fields.Char(string="File Name", required=True)
    file_pdf=fields.Binary(string="Title")
    file_date=fields.Datetime(string='Date', default=fields.Datetime.now, readonly=True)
    asset_id=fields.Many2one('platform.vessel', string='Platform / Vessel', ondelete='cascade')

    def action_view_file(self):
        self.ensure_one()
        
        return{
            'type':'ir.actions.act_url',
            'url': '/web/content/drawings.report/%s/file_pdf/%s?download=false' % (
                self.id,
                self.name,
            ),
            'target':'new',
        }


class manualsReport(models.Model):
    _name="manuals.report"
    _description="Manual Report"
    _rec_name="name"

    name=fields.Char(string="File Name", required=True)
    file_pdf=fields.Binary(string="Title")
    file_date=fields.Datetime(string='Date',default=fields.Datetime.now,readonly=True)

    asset_id=fields.Many2one('platform.vessel',string='Vessels / Platform', ondelete='cascade')

    def action_view_file(self):
        self.ensure_one()

        return{
            'type':'ir.actions.act_url',
            'url': '/web/content/manuals.report/%s/file_pdf/%s?download=false' % (
                self.id,
                self.name,
            ),
            'target':'new',
        }

class correspondenceReport(models.Model):
    _name="correspondence.report"
    _description="Upload Your Correspondence.report"
    _rec_name="name"

    name=fields.Char(string="File Name")
    file_pdf=fields.Binary(string="Title")
    file_date=fields.Datetime(string='Date', default=fields.Datetime.now, readonly=True)
    asset_id=fields.Many2one('platform.vessel', string='Platform / Vessel', ondelete='cascade')

    def action_view_file(self):
        self.ensure_one()

        return{
            'type':'ir.actions.act_url',
            'url': '/web/content/correspondence.report/%s/file_pdf/%s?download=false' % (
                self.id,
                self.name,
            ),
            'target':'new',
        }

class imageReport(models.Model):
    _name="image.report"
    _description="Upload Your Drawing Report"
    _rec_name="name"

    name=fields.Char(string="File Name", required=True)
    img_file=fields.Binary(string="Title")
    file_date=fields.Datetime(string='Date', default=fields.Datetime.now, readonly=True)
    asset_id=fields.Many2one('platform.vessel', string='Platform / Vessel', ondelete='cascade')

    def action_view_file(self):
        self.ensure_one()

        return {
            'type':'ir.actions.act_url',
            'url': '/web/content/image.report/%s/img_file/%s?download=false' % (
                self.id,
                self.name,
            ),
            'target':'new'
        }