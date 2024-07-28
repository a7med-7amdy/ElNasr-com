# -*- coding: utf-8 -*-

from odoo import models, fields,api,_
from odoo.exceptions import UserError



class MoveType(models.Model):
    _name = 'vehicle.move.type'

    name = fields.Char()


class FleetVehicleMoves(models.Model):
    _name = 'vehicle.move'
    _description = 'Vehicle Moves'


    name= fields.Char( string='Name',copy=False)
    type_id= fields.Many2one(
        comodel_name='vehicle.move.type',
        string='Move Type',
        required=True)

    @api.model
    def create(self, vals):
        if 'name' not in vals or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('vehicle.moves.seq') or _('New')
        return super(FleetVehicleMoves, self).create(vals)

    state= fields.Selection(
        string='State',
        selection=[('draft', 'Draft'),
                   ('confirmed', 'Confirm'),
                   ('invoiced', 'Invoiced'),
                   ],default='draft',readonly=True
        )

    def confirm(self):
        self.state = 'confirmed'

    def reset_to_draft(self):
        self.state = 'draft'

    def create_invoice(self):
        for rec in self:
            if rec.state!='confirmed':
                raise models.ValidationError("Please Confirm Vehicle Move First !!",rec.name)
            if not rec.invoice_id:
                invoice_vals = {
                    'partner_id': rec.partner_id.id,
                    'invoice_date': rec.date,
                    'ref': rec.name,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [(0, 0, {
                        'name': rec.service_id.name,
                        'product_id': rec.service_id.id,
                        'quantity': rec.qty,
                        # 'price_unit': self.price,
                        'price_unit': 0.0,
                        'analytic_distribution': {rec.vehicle_id.analytic_account_id.id: 100},


                    })],
                }

                invoice = self.env['account.move'].create(invoice_vals)
                rec.invoice_id=invoice.id
                rec.state='invoiced'


    date = fields.Date(string='Date',default=fields.Date.today(),required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle',required=True)
    driver_id = fields.Many2one('res.partner', string='Driver',required=True)
    follower_id = fields.Many2one('res.partner', string='Follower')
    partner_id = fields.Many2one('res.partner', string='Partner',required=True)
    service_id = fields.Many2one('product.product', string='Service',required=True,domain=[('detailed_type','=','service')])
    qty = fields.Float(string='Quantity',default=1)
    price = fields.Float(string='Price' )
    uom = fields.Many2one('uom.uom', string='Unit of Measure')
    destination = fields.Char(string='Destination')
    notes = fields.Char(string='Notes')
    sale_id = fields.Many2one('sale.order', string='Sale Order',domain=[('state','=','sale')] )
    invoice_id = fields.Many2one('account.move',readonly=True,copy=False)
    payment_state = fields.Selection(related='invoice_id.payment_state', readonly=True ,tracking=True)

    @api.onchange('sale_id')
    def sale_changed(self):
        if self.sale_id:
            self.partner_id=self.sale_id.partner_id.id


    @api.onchange('vehicle_id')
    def vehicle_changed(self):
        if self.vehicle_id:
            self.driver_id=self.vehicle_id.driver_id.id
            self.service_id=self.vehicle_id.service_id.id


    @api.onchange('service_id')
    def service_changed(self):
        if self.service_id:
            self.price=self.service_id.lst_price
            self.uom=self.service_id.uom_id.id




class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    service_id = fields.Many2one('product.product', string='Service', domain=[('detailed_type','=','service')])


    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account',readonly=True)

    @api.model
    def create(self, values):
        res = super(FleetVehicle, self).create(values)
        if not res.analytic_account_id:
            analytic_account_id = self.env['account.analytic.account'].create(
                {
                    'name': res.name,
                    'plan_id': self.env.ref('rw_vehicle_move.vehicle_analytic_plan').id
                }
            )
            res.analytic_account_id = analytic_account_id.id

        return res

#


class AnalyticPlan(models.Model):
    _inherit = 'account.analytic.plan'

    no_delete= fields.Boolean(
        string='',
        copy=False)


    def unlink(self):
        for rec in self:
            if rec.no_delete  :
                raise UserError(_('You can not delete This Record'))
        return super(AnalyticPlan, self).unlink()
