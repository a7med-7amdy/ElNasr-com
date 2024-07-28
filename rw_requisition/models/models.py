# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RequisitionOperation(models.Model):
    _name = 'requistion.operation'

    name = fields.Char()


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    _description = 'Purchase Requisition'

    contract_start_date = fields.Date(string='Contract Start Date')
    contract_end_date = fields.Date(string='Contract End Date')
    operation_name = fields.Many2one('requistion.operation', string='Operation Name')
    assigned_to = fields.Many2one('res.partner', string='Assigned To')


class PurchaseRequisitionLine(models.Model):
    _inherit = 'purchase.requisition.line'

    _description = 'Purchase Requisition Line'

    vendor_id = fields.Many2one(related='requisition_id.vendor_id',store=True)
    operation_name = fields.Many2one(related='requisition_id.operation_name',store=True)
    contract_start_date = fields.Date(related='requisition_id.contract_start_date',store=True)
    contract_end_date = fields.Date(related='requisition_id.contract_end_date',store=True)
    assigned_to = fields.Many2one(related='requisition_id.assigned_to',store=True)

    lot_id = fields.Many2one('stock.lot', string='Lot',
                               domain="[('product_id','=', product_id)]",
                               help='Lot from which the product will be sold')



    def _prepare_purchase_order_line(self, name, product_qty=0.0, price_unit=0.0, taxes_ids=False):
            res = super(PurchaseRequisitionLine, self)._prepare_purchase_order_line(name, product_qty, price_unit, taxes_ids)
            res['lot_id'] = self.lot_id.id   or []
            return res



# self.env.ref('rw_requisition.vehicle_analytic_plan')




