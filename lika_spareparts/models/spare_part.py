from odoo import models, fields
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_spare_part = fields.Boolean(string="Spare Part", default=False, index=True)

    # Sub Assembly (Many2many directly to product.product)
    sub_assembly_ids = fields.Many2many(
        comodel_name='product.product',
        relation='product_template_sub_assembly_rel',
        column1='parent_template_id',
        column2='child_product_id',
        string='Sub Assembly',
        tracking=True,
    )

    related_part_ids = fields.Many2many(
        comodel_name='product.product',
        relation='product_template_related_part_rel',
        column1='parent_template_id',
        column2='child_product_id',
        string='Related Parts',
        tracking=True,
    )

    # Crane Specific Details
    part_number = fields.Char(string='Part Number', index=True, tracking=True)
    make_id = fields.Many2one('crane.make', string='Make', tracking=True)
    drawing_no = fields.Char(string='Drawing No', tracking=True)
    drawing_pos = fields.Char(string='Pos', tracking=True)
    dimensions = fields.Char(string='Dimensions', tracking=True)
    material = fields.Char(string='Material', tracking=True)
    manufacture = fields.Char(string='Manufacture', tracking=True)
    part_description = fields.Text(string='Part Description', tracking=True) # 14

    # specifiaction documents
    specification_ids = fields.One2many('spare.part.specification', 'part_id', string='Specifications', tracking=True) # 26
    # images
    image_ids = fields.One2many('spare.part.images', 'part_id', string='Images', tracking=True) # 27


class SparePartSpecification(models.Model): # 26
    _name = 'spare.part.specification'
    _inherit = ['mail.thread']
    _description = 'Spare Part Specification'
    _rec_name = "file_name"

    part_id = fields.Many2one('product.template', ondelete='cascade', tracking=True)
    title = fields.Char(string='Title', tracking=True) # 28
    file_name = fields.Char(string='File Name', tracking=True) # 29
    attachment = fields.Binary(string='File', filename='file_name', tracking=True) # 30

    def action_view_file(self):
        self.ensure_one()
        if not self.attachment:
            raise UserError("Belum ada file yang di unggah.")

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self._name}/{self.id}/attachment/{self.file_name}',
            'target': 'new',
        }

class SparePartImage(models.Model): #27
    _name = 'spare.part.images'
    _inherit = ['mail.thread']
    _description = 'Spare Part Images'
    _rec_name = "file_name"

    part_id = fields.Many2one('product.template', ondelete='cascade', tracking=True)
    title = fields.Char(string='Title', tracking=True) # 28
    file_name = fields.Char(string='File Name', tracking=True) # 29
    attachment = fields.Binary(string="Upload Image", filename="file_name", tracking=True)

    def action_view_image(self):
        self.ensure_one()
        if not self.attachment:
            raise UserError("Belum ada gambar yang di unggah.")

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self._name}/{self.id}/attachment/{self.file_name}',
            'target': 'new',
        }


# class SparePartSubAssembly(models.Model):
#     _name = 'spare.part.sub.assembly'
#     _inherit = ['mail.thread']
#     _description = 'Spare Part Sub Assembly'
#     _rec_name = "component_part_id"
#
#     parent_part_id = fields.Many2one('product.template', string='Parent Part', ondelete='cascade', tracking=True)
#
#     # Link to product.product
#     component_part_id = fields.Many2one(
#         'product.product',
#         string='Component Part No',
#         tracking=True,
#         domain="[('type', '=', 'consu')]"  # Only show storable products
#     )

# from odoo import models, fields, api
# from odoo.exceptions import UserError
#
# # class SparePartCategory(models.Model):
# #     _name = 'spare.part.category'
# #     _inherit = ['mail.thread']
# #     _description = 'Spare Part Category'
# #     _rec_name = "sp_category_name"
# #
# #     sp_category_name = fields.Char(string='Category Name', required=True, tracking=True)
#
# class SparePart(models.Model):
#     _name = 'spare.part'
#     _inherit = ['mail.thread']
#     _inherits = {'product.product': 'product_id'}
#     _description = 'Spare Part'
#     _rec_name = 'part_number'
#     _unique_make_name = models.Constraint('unique(part_number)', 'Part number must be unique!')
#
#     # relation to product
#     product_id = fields.Many2one('product.product', string='Product', required=True, ondelete='cascade')
#
#     # Section A: Header Details
#     part_number = fields.Char(string='Part Number', required=True, index=True, tracking=True) # 1
#     make_id = fields.Many2one('crane.make', string='Make', tracking=True)
#     drawing_no = fields.Char(string='Drawing No', tracking=True) # 3
#     drawing_pos = fields.Char(string='Pos', tracking=True) # 4
#     uom_id = fields.Many2one('uom.uom', string='Unit of Measure', tracking=True) # 5
#     barcode = fields.Char(string='Barcode', tracking=True) # 6
#
#     sales_currency_id = fields.Many2one('res.currency', string='Sales Currency', tracking=True) # 7
#     sales_price = fields.Monetary(string='Sales Price', currency_field='sales_currency_id', tracking=True) # 7
#     local_currency_id = fields.Many2one('res.currency', string='Local Currency', tracking=True) # 8
#     local_price = fields.Monetary(string='Local Price', currency_field='local_currency_id', tracking=True) # 8
#
#     weight = fields.Float(string='Weight', tracking=True) # 9
#     dimensions = fields.Char(string='Dimensions', tracking=True) # 10
#     part_type = fields.Selection([('part', 'Part'), ('assembly', 'Assembly')], string='Type', default='part', tracking=True) # 11
#     # sp_category_id = fields.Many2one('spare.part.category', string='Category', tracking=True) # 12
#
#     # Descriptions & Extra Info
#     part_description = fields.Text(string='Part Description', tracking=True) # 14
#     sales_description = fields.Text(string='Sales Description', tracking=True) # 15
#     material = fields.Char(string='Material', tracking=True) # 16
#     manufacture = fields.Char(string='Manufacture', tracking=True) # 24
#     notes = fields.Text(string='Notes', tracking=True) # 23
#
#     # Inventory Summary
#     # qty_add = fields.Float(string='Add', tracking=True) # 17
#     # qty_reserved = fields.Float(string='Reserved', tracking=True) # 18
#     # qty_backorder = fields.Float(string='Back Order', tracking=True) # 19
#     # qty_sales_order = fields.Float(string='Sales Order', tracking=True) # 20
#
#     # Tab / Relation Fields
#     image_1920 = fields.Image(string='Image / Illustration') # 25
#     # location_line_ids = fields.One2many('spare.part.location', 'part_id', string='Locations', tracking=True) # 21, 22
#     specification_ids = fields.One2many('spare.part.specification', 'part_id', string='Specifications', tracking=True) # 26
#     # image_ids = fields.One2many('spare.part.images', 'part_id', string='Images', tracking=True) # 27
#     # sub_assembly_ids = fields.One2many('spare.part.sub.assembly', 'parent_part_id', string='Sub Assembly', tracking=True) # 31
#     related_part_ids = fields.Many2many('spare.part', 'spare_part_rel', 'part_id', 'related_id', string='Related Parts', tracking=True) # 36
#     # vendor_supplier_ids = fields.One2many('spare.part.vendor', 'part_id', string='Vendor Supplying Part', tracking=True) # 38
#
#     # auto create sparepart as product (add to product)
#     @api.model_create_multi
#     def create(self, vals_list):
#         for vals in vals_list:
#             # check if this sparepart already a product, if not create the product relation
#             if not vals.get('product_id'):
#                 # Get default UoM (Units) if not provided
#                 if not vals.get('uom_id'):
#                     unit_uom = self.env.ref('uom.product_uom_unit', raise_if_not_found=False)
#                     if unit_uom:
#                         vals['uom_id'] = unit_uom.id
#
#                 # Create the product automatically
#                 product_vals = {
#                     'name': vals.get('part_description') or vals.get('part_number', 'New Spare Part'),
#                     'type': 'consu',  # Storable product (Goods)
#                     'is_spare_part': True,  # Flag on product to identify it
#                     'sale_ok': True,
#                     'purchase_ok': True,
#                 }
#
#                 # Set optional fields if they exist
#                 if vals.get('sales_price'):
#                     product_vals['list_price'] = vals['sales_price']
#
#                 if vals.get('local_price'):
#                     product_vals['standard_price'] = vals['local_price']
#
#                 if vals.get('weight'):
#                     product_vals['weight'] = vals['weight']
#
#                 if vals.get('barcode'):
#                     product_vals['barcode'] = vals['barcode']
#
#                 if vals.get('uom_id'):
#                     product_vals['uom_id'] = vals['uom_id']
#                     # product_vals['uom_po_id'] = vals['uom_id']
#
#                 if vals.get('sales_description'):
#                     product_vals['description_sale'] = vals['sales_description']
#
#                 if vals.get('part_description'):
#                     product_vals['description'] = vals['part_description']
#
#                 # Clean None values
#                 product_vals = {k: v for k, v in product_vals.items() if v is not None}
#
#                 product = self.env['product.product'].create(product_vals)
#                 vals['product_id'] = product.id
#
#         return super().create(vals_list)
#
#     def write(self, vals):
#         """Sync changes to the underlying product.product"""
#         # Call super first to update spare.part fields
#         result = super().write(vals)
#
#         # Define mapping between spare.part fields and product.product fields
#         product_field_mapping = {
#             'part_description': 'name',  # Update product name when description changes
#             'sales_description': 'description_sale',
#             'sales_price': 'list_price',
#             'local_price': 'standard_price',
#             'weight': 'weight',
#             'barcode': 'barcode',
#             'uom_id': 'uom_id',  # Also need to update uom_po_id
#             'image_1920': 'image_1920',
#         }
#
#         # Sync fields for each spare part record
#         for part in self:
#             if not part.product_id:
#                 continue
#
#             product_vals = {}
#
#             # Check each mapped field
#             for sp_field, product_field in product_field_mapping.items():
#                 if sp_field in vals:
#                     product_vals[product_field] = vals[sp_field]
#
#             # Special handling for uom_id (also update uom_po_id)
#             # if 'uom_id' in vals:
#             #     product_vals['uom_po_id'] = vals['uom_id']
#
#             # Special handling: if part_number changes but no description, update name
#             if 'part_number' in vals and 'part_description' not in vals:
#                 # Only update product name if it was using part_number
#                 if part.product_id.name == part.part_number:
#                     product_vals['name'] = vals['part_number']
#
#             # Special handling: if part_description changes, update both name and description
#             if 'part_description' in vals:
#                 product_vals['name'] = vals['part_description']
#                 product_vals['description'] = vals['part_description']
#
#             # Write to product if there are changes
#             if product_vals:
#                 part.product_id.write(product_vals)
#
#         return result
#
#     def unlink(self):
#         """Also delete the underlying product when spare part is deleted"""
#         products_to_delete = self.mapped('product_id')
#         result = super().unlink()
#         # Only delete products that are marked as spare parts
#         products_to_delete.filtered(lambda p: p.is_spare_part).unlink()
#         return result
#
#
# # add a checkbox if a product is spare part to product.product
# class ProductTemplate(models.Model):
#     _inherit = 'product.template'
#
#     is_spare_part = fields.Boolean(
#         string="Is Spare Part", default=False, tracking=True,
#         help="Check if this product is a spare part."
#     )
#
# #
# # class SparePartLocation(models.Model):
# #     _name = 'spare.part.location'
# #     _inherit = ['mail.thread']
# #     _description = 'Spare Part Location Quantity'
# #     _rec_name = "location_id"
# #
# #     part_id = fields.Many2one('spare.part', ondelete='cascade', tracking=True)
# #     location_id = fields.Many2one('stock.location', string='Location', tracking=True) # 21
# #     quantity = fields.Float(string='Quantity', tracking=True) # 22

# #     quantity = fields.Float(string='Quantity', default=1.0, tracking=True)
# #     position = fields.Integer(string='Position', tracking=True)
# #     drawing_no = fields.Char(string='Drawing No', tracking=True)
# #
# #     # Display-only fields to show info from selected product
# #     component_is_spare_part = fields.Boolean(
# #         string='Is Spare Part',
# #         related='component_part_id.is_spare_part',
# #         store=True
# #     )
#
# #
# # class SparePartVendor(models.Model):
# #     _name = 'spare.part.vendor'
# #     _inherit = ['mail.thread']
# #     _description = 'Spare Part Vendor Supplier'
# #     _rec_name = 'vendor_id'
# #
# #     part_id = fields.Many2one('spare.part', ondelete='cascade', tracking=True)
# #     vendor_id = fields.Many2one('res.partner', string='Vendor', tracking=True) # 39
# #     purchase_description = fields.Text(string='Purchase Description', tracking=True) # 40
# #     currency_id = fields.Many2one('res.currency', string='Currency', tracking=True) # 42
# #     cost_price = fields.Monetary(string='Cost Price', currency_field='currency_id', tracking=True) # 41
# #     vendor_part_number = fields.Char(string='Vendor Part Number', tracking=True) # 43
# #     uom_id = fields.Many2one('uom.uom', string='Unit', tracking=True) # 44
# #     delivery_schedule = fields.Char(string='Delivery Schedule', tracking=True) # 45
# #     notes = fields.Text(string='Notes', tracking=True) # 46
# #     dated = fields.Datetime(string='Dated', default=fields.Datetime.now, tracking=True) # 47
