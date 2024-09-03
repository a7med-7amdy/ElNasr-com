# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RequisitionOperation(models.Model):
    _name = 'requistion.operation'

    name = fields.Char()


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    _description = 'Purchase Requisition'

    operation_name = fields.Many2one('requistion.operation', string='Operation Name')
    assigned_to = fields.Many2one('res.partner', string='Assigned To')
    customer_id = fields.Many2one('res.partner', string='Customer')

    alert_flag= fields.Boolean(
        string='Alert Flag',copy=False,readonly=True,store=True,
        compute="_compute_alert")

    alert_details = fields.Text(
        string='Alert Details',
        readonly=True,
        store=True,
        compute="_compute_alert")



    def _compute_alert_job(self):
        purchase_requisition_ids=self.env['purchase.requisition'].search([])
        for rec in purchase_requisition_ids:
            rec.alert_flag = False
            alert_lines = []
            today = fields.Date.today()

            for line in rec.line_ids:
                if line.date_to_notify and line.qty_ordered < line.qty_to_notify:
                    alert_date = fields.Date.from_string(line.date_to_notify)
                    if today > alert_date:
                        rec.alert_flag = True
                        alert_lines.append(
                            f"Product: {line.product_id.name}, Ordered: {line.qty_ordered}, Min Qty : {line.qty_to_notify}, TO : {line.date_to_notify}"
                        )

            rec.alert_details = "\n".join(alert_lines) if alert_lines else ""


    @api.depends('line_ids', 'line_ids.qty_to_notify', 'line_ids.date_to_notify', 'line_ids.product_qty',
                 'line_ids.qty_ordered')
    def _compute_alert(self):
        for rec in self:
            rec.alert_flag = False
            alert_lines = []
            today = fields.Date.today()

            for line in rec.line_ids:
                if line.date_to_notify and line.qty_ordered < line.qty_to_notify:
                    alert_date = fields.Date.from_string(line.date_to_notify)
                    if today > alert_date:
                        rec.alert_flag = True
                        alert_lines.append(
                            f"Product: {line.product_id.name}, Ordered: {line.qty_ordered}, Min Qty : {line.qty_to_notify}, TO : {line.date_to_notify}"
                        )

            rec.alert_details = "\n".join(alert_lines) if alert_lines else ""


class PurchaseRequisitionLine(models.Model):
    _inherit = 'purchase.requisition.line'

    _description = 'Purchase Requisition Line'

    vendor_id = fields.Many2one(related='requisition_id.vendor_id',store=True)
    operation_name = fields.Many2one(related='requisition_id.operation_name',store=True)
    least_qty= fields.Float(
        string='Least Quantities',
        compute="_compute_least_qty",readonly=True,store=True)
    contract_start_date = fields.Date( "Start Date")
    contract_end_date = fields.Date( "End Date")
    assigned_to = fields.Many2one('res.partner', string='Assigned To')

    qty_to_notify= fields.Float(string='Alert Qty', )
    date_to_notify= fields.Date(string="Alert Date")

    lot_id = fields.Many2one('stock.lot', string='Lot',
                               domain="[('product_id','=', product_id)]",
                               help='Lot from which the product will be sold')


    @api.depends('qty_ordered','product_qty')
    def _compute_least_qty(self):
        for line in self:
            line.least_qty=0.0
            if line.product_qty and line.product_qty>=line.qty_ordered:
                line.least_qty=line.product_qty - line.qty_ordered




    def _prepare_purchase_order_line(self, name, product_qty=0.0, price_unit=0.0, taxes_ids=False):
            res = super(PurchaseRequisitionLine, self)._prepare_purchase_order_line(name, product_qty, price_unit, taxes_ids)
            res['lot_id'] = self.lot_id.id   or []
            res['product_qty'] = self.least_qty if self.requisition_id.type_id.quantity_copy=='copy' else []
            return res



# self.env.ref('rw_requisition.vehicle_analytic_plan')




