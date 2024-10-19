# -*- coding: utf-8 -*-

from odoo import api, Command, fields, models, _
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import UserError


class purchaseOrderLine(models.Model):
    """
    Inherits the model purchase Order Line to extend and add extra field and method
    for the working of the app.
    """
    _inherit = 'purchase.order.line'



    lot_id = fields.Many2one('stock.lot', string='Operation',help='Lot from which the product will be sold')

    def _create_stock_moves(self, picking):
        res=super(purchaseOrderLine, self)._create_stock_moves(picking)
        for order_line in self:
            move = self.env['stock.move'].search(
                [('purchase_line_id', '=', order_line.id)])
            for items in move.move_line_ids:
                items.unlink()
            for lot in order_line.lot_id:
                print(move)
                print(lot)

                move.move_line_ids = [fields.Command.create({
                    'lot_id': lot.id,
                    'lot_name': lot.name,
                    'quantity': move.purchase_line_id.product_uom_qty,
                    'product_id': move.purchase_line_id.product_id.id,
                    'product_uom_id': move.purchase_line_id.product_uom.id,
                    'location_id': move.location_id.id,
                    'location_dest_id': move.location_dest_id.id,
                    # 'product_uom_qty': move.purchase_line_id.product_uom_qty,
                    'company_id': self.env.company.id,
                    'picking_id': move.picking_id.id,
                })]
        return res



class purchaseOrder(models.Model):
    """
    Inherits the model purchase Order Line to extend and add extra field and method
    for the working of the app.
    """
    _inherit = 'purchase.order'









