from odoo import api, fields, models


class SalesCustom(models.Model):
    _inherit = 'sale.order'


    contract_id = fields.Many2one(comodel_name='contract.contract',contract="Contract",domain=[('state', '=', 'confirmed')])
    total_qty  = fields.Float(
        string='Total qty', compute='total_qty_for_lines',
        required=False)

    @api.depends('order_line.product_uom_qty')
    def total_qty_for_lines(self):
        for rec in self:
            total = 0
            if rec.order_line:
                for line in rec.order_line:
                    total += line.product_uom_qty
            rec.total_qty = total

