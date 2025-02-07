from odoo import api, fields, models

class ProductTemplateCustomMaintenance(models.Model):
    _inherit = 'product.template'


    spare_parts = fields.Boolean(
        string='Spars Parts',
        required=False)
    row_material = fields.Boolean(
        string='Row Material',
        required=False)


class ProductCustomMaintenance(models.Model):
    _inherit = 'product.product'


    spare_parts = fields.Boolean(
        string='Spars Parts',
        related='product_tmpl_id.spare_parts',
        required=False)
    row_material = fields.Boolean(
        string='Row Material',
        related='product_tmpl_id.row_material',
        required=False)
