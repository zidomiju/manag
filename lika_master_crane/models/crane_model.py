from odoo import models, fields, api
from odoo.exceptions import UserError


class LikaMasterCrane(models.Model):
    _name = 'crane.model'
    _inherit = ['mail.thread']
    _inherits = {'product.product': 'product_id'}
    _description = 'Master crane model details and specification'
    _rec_name = 'crane_model'

    # GENERAL INFORMATIONS
    product_id = fields.Many2one('product.product', string='Product', required=True, ondelete='cascade')
    
    crane_model = fields.Char(string="Crane Model", required=True, tracking=True)
    image_1920 = fields.Binary(string='Crane Image', attachment=True)
    status = fields.Selection(
        string="Status",
        selection=[
            ('active', "Active"),
            ('inactive', "Inactive")
        ],
        required=True,
        tracking=True
    )

    make_id = fields.Many2one('crane.make', string='Make', required=True, tracking=True)
    make_code = fields.Char(
        string='Make Code', 
        related='make_id.make_code',
        inverse='_inverse_make_code',
        store=True,
        tracking=True
    )
    type_id = fields.Many2one('crane.type', string="Type", required=True, tracking=True)
    model_code = fields.Char(string="Model Code", tracking=True)
    model_year = fields.Char(string="Year / Model Year", tracking=True)
    description = fields.Text(string="Description", required=False, tracking=True)

    # TECHNICAL SPECIFICATIONS
    lifting_capacity = fields.Char(string="Lifting Capacity / SWL", tracking=True)
    max_outreach = fields.Char(string="Max. Outreach", tracking=True)
    min_outreach = fields.Char(string="Min. Outreach", tracking=True)
    operating_pressure = fields.Char(string="Operating Pressure", tracking=True)
    power_source = fields.Char(string="Power Source", tracking=True)

    # DOCUMENTS
    document_ids = fields.One2many('crane.document', 'model_id', tracking=True)

    def _inverse_make_code(self):
        """Update the make_code on the related crane.make"""
        for crane in self:
            if crane.make_id:
                crane.make_id.make_code = crane.make_code

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Check if this crane already has a product, if not create the product relation
            if not vals.get('product_id'):
                # Get the default "Units" UoM
                unit_uom = self.env.ref('uom.product_uom_unit', raise_if_not_found=False)
                if not unit_uom:
                    # Fallback: get first UoM in category "Unit"
                    unit_uom = self.env['uom.uom'].search([
                        ('category_id', '=', self.env.ref('uom.product_uom_categ_unit').id)
                    ], limit=1)
                
                # Create the product automatically
                product_vals = {
                    'name': vals.get('crane_model') or vals.get('make', 'New Crane'),
                    'type': 'consu',  # Storable product (Goods)
                    'sale_ok': True,
                    'purchase_ok': True,
                    'uom_id': unit_uom.id if unit_uom else False,  # Default to Units
                    # 'uom_po_id': unit_uom.id if unit_uom else False,  # Default to Units for purchasing
                }
                
                # Add description if available
                if vals.get('description'):
                    product_vals['description'] = vals['description']
                
                # Clean None values to avoid errors
                product_vals = {k: v for k, v in product_vals.items() if v is not False}
                
                product = self.env['product.product'].create(product_vals)
                vals['product_id'] = product.id
                
        return super().create(vals_list)
    
    def write(self, vals):
        """Sync changes to the underlying product"""
        result = super().write(vals)
        
        # Map crane fields to product fields
        product_field_mapping = {
            'crane_model': 'name',
            'description': 'description',
        }
        
        for crane in self:
            product_vals = {}
            for crane_field, product_field in product_field_mapping.items():
                if crane_field in vals:
                    product_vals[product_field] = vals[crane_field]
            
            if product_vals and crane.product_id:
                crane.product_id.write(product_vals)
        
        return result


class CraneDocument(models.Model):
    _name = "crane.document"
    _inherit =['mail.thread']
    _description = "Provide documents list for crane models"
    _rec_name = 'document_filename'

    # DOCUMENTS
    model_id = fields.Many2one('crane.model', ondelete='cascade', tracking=True)
    name = fields.Char(string="Name", required=True, tracking=True)
    document_filename = fields.Char(string="Document Name", tracking=True)
    document_data = fields.Binary(string="Document File", filename='document_filename')

    # view document action
    def action_view_document_file(self):
            self.ensure_one()
            if not self.document_data:
                raise UserError("Belum ada file yang di unggah.")
    
            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{self._name}/{self.id}/document_data/{self.document_filename}',
                'target': 'new',
            }


class CraneMake(models.Model):
    _name = 'crane.make'
    _inherit = ['mail.thread']
    _description = 'Crane Make'
    _rec_name = 'name'
    _order = 'name'
    _unique_make_name = models.Constraint('unique(name)', 'Make name must be unique!')
    
    name = fields.Char(string='Make', required=True, tracking=True)
    make_code = fields.Char(
        string='Make Code', required=True, tracking=True,
        help="Auto filled when Make is selected."
    )
    crane_model_ids = fields.One2many('crane.model', 'make_id', string='Crane Models')
    crane_model_count = fields.Integer(string='Crane Models', compute='_compute_crane_model_count')
    
    @api.depends('crane_model_ids')
    def _compute_crane_model_count(self):
        for make in self:
            make.crane_model_count = len(make.crane_model_ids)
    
    @api.depends('name', 'make_code')
    def _compute_display_name(self):
        """Custom display name showing make and code"""
        for make in self:
            if make.make_code:
                make.display_name = f"{make.name} ({make.make_code})"
            else:
                make.display_name = make.name
    
    @api.model
    def name_create(self, name):
        """Called when user types a new make name and presses Enter"""
        # Check if already exists
        existing = self.search([('name', 'ilike', name)], limit=1)
        if existing:
            return existing.id, existing.display_name
        
        # Create new make
        record = self.create({'name': name})
        return record.id, record.display_name


class CraneType(models.Model):
    _name = "crane.type"
    _inherit = ['mail.thread']
    _description = "Provide type selection for crane models"
    _rec_name = "type"

    type = fields.Char(string="Crane Type", required=True, tracking=True)