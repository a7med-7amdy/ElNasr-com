from odoo import api, fields, models

class CarStockCustom(models.Model):
    _inherit = 'stock.picking'

    picking_id = fields.Many2one(
        comodel_name='car.order',
        string='Car Order')





class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    origin_car_order_id = fields.Many2one(
        'car.order',
        string='Car Order',
    )