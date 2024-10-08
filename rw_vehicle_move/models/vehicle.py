# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MoveType(models.Model):
    _name = 'vehicle.move.type'

    name = fields.Char()


class FleetVehicleMoves(models.Model):
    _name = 'vehicle.move'
    _description = 'Vehicle Moves'



    date = fields.Date(string='Date', default=fields.Date.today(), required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle', required=True)
    driver_id = fields.Many2one('res.partner', string='Driver', required=True)
    follower_id = fields.Many2one('res.partner', string='Follower')
    partner_id = fields.Many2one('res.partner', string='Discharging', required=True)
    customer_share = fields.Many2one('res.partner',string='Partner',required=True)

    service_id = fields.Many2one('product.product', string='Product', required=True, domain=[('is_vehicle', '=', True)])
    loaded_qty = fields.Float(string='Quantity', default=1)
    discharged_qty = fields.Float(string='Discharged Quantity', default=1)

    price = fields.Float(string='Price')
    uom = fields.Many2one('uom.uom', string='Unit of Measure')
    destination = fields.Char(string='Destination')
    notes = fields.Char(string='Notes')
    sale_id = fields.Many2one('sale.order', string='Sale Order', domain=[('state', '=', 'sale')])
    invoice_id = fields.Many2one('account.move', readonly=True, copy=False)
    payment_state = fields.Selection(related='invoice_id.payment_state', readonly=True, tracking=True)
    lots_id = fields.Many2many(
        comodel_name='stock.lot',
        string='')
    lot_id = fields.Many2one(
        'stock.lot',
        string='Operation', domain="[('id', 'in', lots_id)]"
    )
    trailer  = fields.Many2one(
        comodel_name='fleet.vehicle',domain=[('trailer', '=', True)],
        string='Trailer',
        required=False)

    def unlink(self):
        for rec in self:
            if rec.state not in ('draft'):
                raise UserError(_('You can not delete Vehicle Moves which is not in draft state'))
        return super(FleetVehicleMoves, self).unlink()

    name = fields.Char(string='Name', copy=False)
    type_id = fields.Many2one(
        comodel_name='vehicle.move.type',
        string='Move Type',
        required=True)

    @api.model
    def create(self, vals):
        if 'name' not in vals or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('vehicle.moves.seq') or _('New')
        return super(FleetVehicleMoves, self).create(vals)

    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'),
                   ('confirmed', 'Confirm'),
                   ('invoiced', 'Invoiced'),
                   ], default='draft', readonly=True
    )
    journal_id = fields.Many2one('account.journal', string="Journal")

    def confirm(self):
        self.state = 'confirmed'

    def reset_to_draft(self):
        self.state = 'draft'

    def create_invoice(self):
        for rec in self:
            if rec.state != 'confirmed' :
                raise models.ValidationError("Please Confirm Vehicle Move First !!", rec.name)
            elif rec.sale_id:
                raise models.ValidationError("There Are Quotations So You Can Not Create Invoices !!")
            if not rec.invoice_id:
                invoice_vals = {
                    'partner_id': rec.partner_id.id,
                    'invoice_date': rec.date,
                    'ref': rec.name,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [(0, 0, {
                        'name': rec.service_id.name,
                        'product_id': rec.service_id.id,
                        'quantity': rec.loaded_qty,
                        'price_unit': 0.0,
                        'analytic_distribution': {rec.vehicle_id.analytic_account_id.id: 100},

                    })],
                }

                invoice = self.env['account.move'].create(invoice_vals)
                rec.invoice_id = invoice.id
                rec.state = 'invoiced'

    def generate_entries(self):
        # journal_pool = self.env['account.journal']
        # journal = journal_pool.search([('type', '=', 'general')], limit=1)
        journal = self.env.company.journal_id
        if not journal:
            raise UserError(_('Please set sales accounting journal!'))

        account_move_obj = self.env['account.move']

        total_debit = 0.0
        total_credit = 0.0
        partner_id = False

        for rec in self:
            contract = rec.contract_id
            if not contract:
                raise UserError(_('Please choose a contract first!'))
            if contract.contract_type != 'general':
                raise UserError(_('Contract Type should be general'))

            debit = self.env.company.debit_account
            credit = self.env.companycredit_account
            entry = rec.vehicle_id.analytic_account_id

            if not debit:
                raise UserError(_('Please set a receivable account for this contract!'))
            if not credit:
                raise UserError(_('Please set an income account for this contract!'))

            matching_line = contract.contract_lines.filtered(lambda r: r.product_id == rec.service_id)
            if not matching_line:
                raise UserError(_('There is no product in this contract like vehicle product!'))
            price = matching_line[0].price
            total_line_cost = rec.loaded_qty * price

            total_debit += total_line_cost
            total_credit += total_line_cost

            if not partner_id:
                partner_id = rec.partner_id.id
            elif partner_id != rec.partner_id.id:
                raise UserError(_('All entries must have the same partner!'))

        account_move_obj.create({
            'ref': "Vehicle Entry",
            'journal_id': journal.id,
            'vehicle_id': self[0].id,
            'contract_id': self[0].contract_id.id,
            'line_ids': [
                (0, 0, {
                    'name': 'Vehicle Service',
                    'partner_id': partner_id,
                    'account_id': debit.id,  # Single debit line
                    'debit': total_debit,
                    'analytic_distribution': {entry.id: 100},
                    'credit': 0.0,
                }),
                (0, 0, {
                    'name': 'Vehicle Service',
                    'partner_id': partner_id,
                    'account_id': credit.id,  # Single credit line
                    'debit': 0.0,
                    'credit': total_credit,
                })
            ]
        })



    @api.constrains('service_id')
    def service_per_contract(self):
        for rec in self:
            if rec.contract_id and rec.service_id:
                if rec.service_id not in (line.product_id for line in rec.contract_id.contract_lines):
                    raise UserError(_('you should choose service same as in contract products'))

    @api.constrains('lot_id')
    def lot_per_contract(self):
        for rec in self:
            if rec.contract_id and rec.lot_id:
                if rec.lot_id not in (line.lot_id for line in rec.contract_id.contract_lines):
                    raise UserError(_('you should choose lot same as in contract lots'))





    @api.onchange('service_id')
    def _get_lots_for_products(self):
        po = None
        lots = []
        if self.service_id:
            products_ids = self.env['stock.lot'].sudo().search([('product_id', '=', self.service_id.id)])
            for lot in products_ids:
                po = lot.id
                lots.append(lot.id)
                self.lots_id = lots
        if po:
            return {'domain': {'lot_id': [('id', 'in', lots)]}}
        else:
            return {'domain': {'lot_id': [('id', '=', False)]}}

    def action_create_quotation(self):
        for rec in self:
            if not rec.contract_id:
                raise UserError(_('Please Choose Contract To Create Quotation'))
            elif rec.state != 'confirmed':
                raise UserError(_('You Can Create Quotation For Confirmed Moves Only'))
            elif rec.sale_id:
                raise UserError(_('You Can Not Create Quotation For 2 Times For The Same Vehicle Move'))

        first_contract = self[0].contract_id
        first_partner = self[0].partner_id

        for rec in self:
            if rec.contract_id != first_contract:
                raise UserError(
                    _('All selected records must have the same Contract. Please select one contract for all records.'))
            elif rec.partner_id != first_partner:
                raise UserError(
                    _('All selected records must have the same Partner. Please select one Partner for all records.'))
        for rec in self:
            order_lines = [(0, 0, {
                'product_id': rec.service_id.id,
                'lot_id': rec.lot_id.id,
                'analytic_distribution': {rec.vehicle_id.analytic_account_id.id: 100},
                'product_uom_qty': rec.loaded_qty,
            })]

            so = self.env['sale.order'].create({
                'partner_id': rec.partner_id.id,
                'contract_id': rec.contract_id.id,
                'order_line': order_lines,
            })
            rec.sale_id = so.id

    @api.onchange('sale_id')
    def sale_changed(self):
        if self.sale_id:
            self.partner_id = self.sale_id.partner_id.id

    @api.onchange('vehicle_id')
    def vehicle_changed(self):
        if self.vehicle_id:
            self.driver_id = self.vehicle_id.driver_id.id
            self.service_id = self.vehicle_id.service_id.id

    @api.onchange('service_id')
    def service_changed(self):
        if self.service_id:
            self.price = self.service_id.lst_price
            self.uom = self.service_id.uom_id.id


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    service_id = fields.Many2one('product.product', string='Service', domain=[('detailed_type', '=', 'service')])

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True)

    trailer = fields.Boolean(
        string='Trailer',
        required=False)

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


class AnalyticPlan(models.Model):
    _inherit = 'account.analytic.plan'

    no_delete = fields.Boolean(
        string='',
        copy=False)

    def unlink(self):
        for rec in self:
            if rec.no_delete:
                raise UserError(_('You can not delete This Record'))
        return super(AnalyticPlan, self).unlink()
