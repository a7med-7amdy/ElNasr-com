from odoo import api, fields, models

class CarStockCustom(models.Model):
    _inherit = 'stock.picking'

    picking_id = fields.Many2one(
        comodel_name='car.order',
        string='Car Order')

    vehicle = fields.Many2one(
        comodel_name='fleet.vehicle',
        string='Vehicle',related='picking_id.vehicle',
        required=True)

    # def button_validate(self):
    #     res = super(CarStockCustom, self).button_validate()
    #     for rec in self:
    #         for line in rec.move_ids_without_package:
    #             if line.requisition_line and line.price_unit:
    #                 line.requisition_line.write({
    #                     'avg_cost': line.price_unit,
    #                 })
    #     return res





class PurchaseOrderCustom(models.Model):
    _inherit = 'purchase.order'

    origin_car_order_id = fields.Many2one(
        'car.order',
        string='Car Order',
    )

    def action_view_picking(self):
        res = super(PurchaseOrderCustom, self).action_view_picking()
        for rec in self:
            if rec.order_line:
                print("Right")
                for line in rec.order_line:  # Iterate through order lines
                    if line.requisition_line:
                        print("Found")
                        line.requisition_line.update({'avg_cost': line.price_unit})
                        print("line.price_unit",line.price_unit)
        return res


class PurchaseOrderLinesCustom(models.Model):
    _inherit = 'purchase.order.line'


    requisition_line = fields.Many2one(
        comodel_name='material.requisition.car.repair',
        string='Requisition',
        required=False)
    product_on_hand_qty = fields.Float(
        string='On Hand', related='product_id.qty_available',
        required=False)


class StockMovesLinesCustom(models.Model):
    _inherit = 'stock.move'

    requisition_line = fields.Many2one(
        comodel_name='material.requisition.car.repair',
        string='Requisition',
        required=False)







