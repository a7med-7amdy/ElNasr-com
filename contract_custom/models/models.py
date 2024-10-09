
from odoo import api, fields, models,_
from odoo.exceptions import UserError


class ContractsCustom(models.Model):
    _name = 'contract.contract'
    _description = 'Custom For Contracts'


    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),('done', 'Done'),
                              ('cancel', 'Canceled'),
                              ], 'State', default='draft')
    contract_type = fields.Selection(
        string='Contract Type',
        selection=[('indirect', 'Indirect'),
                   ('transfer', 'Transfer'),
                   ('general', 'General'),
                   ],  default='indirect', required=True)


    vendor = fields.Many2one(
        comodel_name='res.partner',
        string='Vendor')
    customer = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        required=True)
    name = fields.Char(
        string='Contract Number',
        required=True)
    contract_date = fields.Datetime(
        string='Contract Date',
        required=False)
    construction_date = fields.Date(
        string='Construction Date',related='customer.construction_date',readonly=False,
        required=False)
    mixing_date = fields.Date(related='customer.mixing_date',readonly=False,
        string='Mixing Date',
        required=False)
    purchase_ids = fields.One2many('purchase.order', 'contract_ids')


    sales_ids = fields.One2many('sale.order', 'contract_id')

    contract_lines = fields.One2many(
        comodel_name='contract.lines',
        inverse_name='contract_ids',
        string='',
        required=False)

    commercial_registration_number= fields.Char(
        string='Commercial Registration Number',related='customer.commercial_registration_number',readonly=False,
        required=False)
    tax_number  = fields.Char(related='customer.vat',
        string='Tax Number',
        required=False)
    purchased = fields.Boolean(
        string='',
        required=False)
    sales = fields.Boolean(
        string='',
        required=False)

    total_cost  = fields.Float(
        string='Total',compute='_compute_total_cost',store=True,
        required=False)
    total_qty = fields.Float(
        string='Quantity',compute='_compute_total_cost',
        required=False)
    total_remaining_quantity = fields.Float(
        string='Total Remaining Quantity', compute='_compute_total_cost',
        required=False)
    total_withdrawn_quantity = fields.Float(
        string='Total Withdrawn Quantity', compute='_compute_total_cost',
        required=False)
    total_quantity_sent= fields.Float(
        string='Total Quantity Sent', compute='_compute_total_cost',
        required=False)
    contract_start_date = fields.Date(
        string='Contract Start Date',
        required=False)
    contract_end_date = fields.Date(
        string='Contract End Date',
        required=False)

    orders = fields.Many2many(
        comodel_name='sale.order',
        string='',compute='get_qty',
        required=False)
    vehicles = fields.Many2many(
        comodel_name='vehicle.move',compute='get_qty_general',
        required=False)


    def unlink(self):
        for rec in self:
            if rec.state not in ('draft'):
                raise UserError(_('You can not delete Contracts  which is not in draft state'))
        return super(ContractsCustom, self).unlink()


    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_reset(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_reset_draft(self):
        for rec in self:
            rec.state = 'draft'


    def sent_to_contract_update(self):
        action = self.env.ref('contract_custom.wizard_contract_update_action')
        result = action.read()[0]
        res = self.env.ref('contract_custom.wizard_contract_update_action_view_form', False)
        result['views'] = [(res and res.id or False, 'form')]
        lines = []
        for line in self.contract_lines:
            lines.append((0, 0, {
                'old_product_id': line.product_id.id,
                'old_qty': line.qty,
                'old_price': line.price,
                'old_load_place': line.load_place.id,
                'old_unloading_place': line.unloading_place.id,
            }))
        result['context'] = {
            'default_old_contract_start_date': self.contract_start_date,
            'default_old_contract_end_date': self.contract_end_date,
            'default_contract_id': self.id,
            'default_old_lines_ids': lines,
        }
        return result

    
    
    def get_qty(self):
        orders = self.env['sale.order'].search([('contract_id','=',self.id)])
        self.orders = orders.ids

    def get_qty_general(self):
        vehicles = self.env['vehicle.move'].search([('contract_id','=',self.id)])
        self.vehicles = vehicles.ids


    # @api.depends('contract_lines.total_price')
    def _compute_total_cost(self):
        for contract in self:
            contract.total_cost = sum(line.total_price for line in contract.contract_lines if line.total_price)
        for contract in self:
            contract.total_qty = sum(line.qty for line in contract.contract_lines if line.qty)
        for contract in self:
            contract.total_remaining_quantity = sum(line.remaining_quantity for line in contract.contract_lines if line.total_price)
        for contract in self:
            contract.total_withdrawn_quantity = sum(line.withdrawn_quantity for line in contract.contract_lines if line.total_price)
        for contract in self:
            contract.total_quantity_sent = sum(line.quantity_sent for line in contract.contract_lines if line.total_price)

  




    def action_confirm(self):
        for rec in self:
            rec.state='confirmed'

    def action_cancel(self):
        for rec in self:
            rec.state='cancel'

    def create_purchase_order(self):
        for rec in self:
            lines = []
            for line in rec.contract_lines:
                lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'name': line.product_id.name,
                    'product_qty': line.remaining_quantity,
                    'lot_id': line.lot_id.id,
                    'price_unit': line.price,
                }))

            po = self.env['purchase.order'].create({
                'partner_id': rec.customer.id,
                'contract_id': rec.id,
                'order_line': lines,
            })
            rec.purchased = True
            rec.purchase_ids = [(4, po.id)]






    def open_purchase_order(self):
        return {
            'name': _('Contract Purchase Order'),
            'domain': [('contract_id', '=', self.id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'target': 'current',
        }
    
    def open_vehicles_entry(self):
        return {
            'name': _('Vehicles Entry'),
            'domain': [('contract_id', '=', self.id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'target': 'current',
        }

    def open_contract_update(self):
        return {
            'name': _('Contract Updates'),
            'domain': [('contract_id', '=', self.id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'contract.update',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'target': 'current',
        }



    def create_sales_order(self):
        for rec in self:
            if rec.contract_type=='indirect':
                lines = []
                for line in rec.contract_lines:
                    lines.append((0, 0, {
                        'product_id': line.product_id.id,
                        'name': line.product_id.name,
                        'product_uom_qty': line.withdrawn_quantity,
                        'lot_id': line.lot_id.id,
                        'price_unit': line.price,
                    }))

                # Create the purchase order and link it to the contract
                so = self.env['sale.order'].create({
                    'partner_id': rec.customer.id,
                    'contract_id': rec.id,  # Make sure this links the PO to the contract
                    'order_line': lines,
                })
            else:
                lines = []
                for line in rec.contract_lines:
                    lines.append((0, 0, {
                        'product_id': line.product_id.id,
                        'name': line.product_id.name,
                        'product_uom_qty': line.remaining_quantity,
                        'lot_id': line.lot_id.id,
                        'price_unit': line.price,
                    }))

                # Create the purchase order and link it to the contract
                so = self.env['sale.order'].create({
                    'partner_id': rec.customer.id,
                    'contract_id': rec.id,  # Make sure this links the PO to the contract
                    'order_line': lines,
                })
            rec.sales = True

            # Add the purchase order to the contract's purchase_ids
            rec.sales_ids = [(4, so.id)]

    def open_sales_order(self):
        return {
            'name': _('Contract Sales Order'),
            'domain': [('contract_id', '=', self.id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'target': 'current',
        }
    def open_vehicle_of_contract(self):
        return {
            'name': _('Vehicle Of Contract'),
            'domain': [('contract_id', '=', self.id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'vehicle.move',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'target': 'current',
        }



class FleetVehicleMovesCustom(models.Model):
    _inherit = 'vehicle.move'

    contract_id = fields.Many2one(comodel_name='contract.contract', string="contract", domain=[('state', '=', 'confirmed')])


class AccountMoveCustom(models.Model):
    _inherit = 'account.move'


    vehicle_id  = fields.Many2one(
        comodel_name='vehicle.move',
        string='',
        required=False)
    contract_id = fields.Many2one(comodel_name='contract.contract', string="contract")









    








