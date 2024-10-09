from odoo import api, fields, models

class ProductTemplateCustom(models.Model):
    _inherit = 'product.template'

    is_vehicle = fields.Boolean(
        string='',
        required=False)


class ProductCustom(models.Model):
    _inherit = 'product.product'

    is_vehicle = fields.Boolean(related='product_tmpl_id.is_vehicle')
