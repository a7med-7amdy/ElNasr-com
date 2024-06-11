# -*- coding: utf-8 -*-

from odoo import models, fields, api



class StockMove(models.Model):
    _inherit = 'stock.move'

    qty_percentage = fields.Float(string='Quantity Percentage', )

    @api.onchange('qty_percentage')
    def onchange_qty_percentage(self):
        if self.qty_percentage:
            try:
                self.product_uom_qty = self.raw_material_production_id.product_qty * (self.qty_percentage / 100)
            except:
                pass

    @api.onchange('product_uom_qty')
    def onchange_product_uom_qty(self):
        if self.product_uom_qty:
            try:
                self.qty_percentage = (self.product_uom_qty  / self.raw_material_production_id.product_qty )*100
            except:
                pass



class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    qty_percentage = fields.Float(string='Quantity Percentage', )

    @api.onchange('qty_percentage')
    def onchange_qty_percentage(self):
        if self.qty_percentage:
            try:
                self.product_qty = self.bom_id.product_qty * (self.qty_percentage / 100)
            except:
                pass

    @api.onchange('product_qty')
    def onchange_product_qty(self):
        if self.product_qty:
            try:
                self.qty_percentage = (self.product_qty  / self.bom_id.product_qty )*100
            except:
                pass

