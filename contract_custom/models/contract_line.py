from odoo import api, fields, models



class ContractLines(models.Model):
    _name = 'contract.lines'
    _description = 'Contract Lines'

    name = fields.Char()
    product_id = fields.Many2one(
        comodel_name='product.product',domain=[('is_vehicle', '=', True)],
        string='',
        required=False)
    contract_start_date = fields.Date(
        string='Contract Start Date',
        required=False)
    contract_end_date = fields.Date(
        string='Contract End Date',
        required=False)
    qty = fields.Float(
        string='Quantity',
        required=False)
    price = fields.Float(
        string='unit Price',
        required=False)
    withdrawn_quantity = fields.Float(
        string='Withdrawn Quantity',compute='_compute_ordered_qty_po'

    )

    remaining_quantity = fields.Float(
        string='Remaining Quantity',
        compute='_get_remaining_quantity',
        readonly=True,
        required=False)
    remaining_quantity_sent = fields.Float(
        string='Remaining Sent',
        compute='_get_remaining_quantity_sent',
        readonly=True,
        required=False)
    quantity_sent = fields.Float(
        string='Quantity Sent',compute='_compute_vehicles_qty_sent')
    contract_ids = fields.Many2one(
        comodel_name='contract.contract',
        string='Contract Ids',
        required=False)
    load_place = fields.Many2one(
        comodel_name='place.place',
        string='Load Place',
        required=False)
    unloading_place = fields.Many2one(
        comodel_name='place.place',
        string='Unloading Location',
        required=False)
    contract_type = fields.Selection(related='contract_ids.contract_type' ,)

    contract  = fields.Boolean(
        string='', 
        required=False)
    lots_id = fields.Many2many(
        comodel_name='stock.lot',
        string='')

    lot_id = fields.Many2one(
        'stock.lot',
        string='Operation',domain="[('id', 'in', lots_id)]"
    )
    total_price  = fields.Float(
        string='cost',compute='_compute_total_price',store=True,
        required=False)
    assigning_party  = fields.Many2one(
        comodel_name='assign.assign',
        string='assigning',
        required=False)
    tax_id = fields.Many2many(
        comodel_name='account.tax',
        string="Taxes",
        store=True, readonly=False, precompute=True,)
    taxed_total_price = fields.Float(
        string='taxed Cost',compute='calculate_taxed_total_price',
        required=False)
    tax_unit_price  = fields.Float(compute='calculate_taxed_total_price',
        string='Tax Price',
        required=False)
    total_amount_with_tax  = fields.Float(
        string='', 
        required=False)
    taxed_total_amount  = fields.Float(
        string='', compute='calculate_taxed_total_price',
        required=False)

    qty_entry_sent = fields.Float(
        string='Qty Entry', compute='get_total_qty_per_product_sent',
        required=False)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'), ('done', 'Done'),
                              ('cancel', 'Canceled'),
                              ], 'State', default='draft',related='contract_ids.state')
    # on_hand_qty = fields.Float(
    #     string="On Hand Quantity",
    #     compute="_compute_on_hand_qty",
    #     store=True
    # )
    #
    #
    # @api.depends('product_id')
    # def _compute_on_hand_qty(self):
    #     for record in self:
    #         record.on_hand_qty = record.product_id.qty_available if record.product_id else 0.0

    max_qty = fields.Float(
        string='Max qty',
        required=False)

    @api.onchange('qty')
    def check_qty(self):
        for record in self:
            if record.max_qty and record.max_qty >= record.withdrawn_quantity:
                return {
                    'warning': {
                        'title': "Low Stock Warning",
                        'message': f"The on-hand quantity ({record.max_qty}) is below 5. Please check stock availability.",
                    }
                }

    def get_total_qty_per_product_sent(self):
        for line in self:
            total_sent_quantity = 0.0
            vehicles = line.contract_ids.vehicles_entry
            if vehicles:
                for vehicle in vehicles:
                    if vehicle.service_id == line.product_id and vehicle.lot_id == line.lot_id:
                        total_sent_quantity += vehicle.loaded_qty
            line.qty_entry_sent = total_sent_quantity

    def calculate_taxed_total_price(self):
        for rec in self:
            total_taxes_amount = 0
            for tax in rec.tax_id:
                total_taxes_amount += (tax.amount / 100)
            rec.tax_unit_price = rec.price * total_taxes_amount + rec.price
            rec.taxed_total_price = rec.tax_unit_price * rec.qty
            rec.taxed_total_amount = total_taxes_amount * rec.price






    @api.depends('qty', 'price')
    def _compute_total_price(self):
        for rec in self:
            if rec.qty or rec.price:
                rec.total_price = rec.price * rec.qty





    def _get_remaining_quantity(self):
        for rec in self:
            if rec.remaining_quantity or rec.qty:
                rec.remaining_quantity = rec.qty - rec.withdrawn_quantity

    def _get_remaining_quantity_sent(self):
        for rec in self:
            if rec.quantity_sent or rec.qty:
                rec.remaining_quantity_sent = rec.qty - rec.quantity_sent
            else:
                rec.remaining_quantity_sent = rec.qty



    def _compute_ordered_qty_po(self):
        for line in self:
            if line.contract_ids.contract_type == 'indirect':
                total = 0.0
                if line.contract_ids:
                    purchase = self.env['purchase.order'].search([('contract_id','=',line.contract_ids.id)])
                    for po in purchase.filtered(
                            lambda po: po.state in ['purchase', 'done']):
                        for po_line in po.order_line.filtered(
                                lambda po_line: po_line.product_id == line.product_id and po_line.lot_id == line.lot_id):
                            total += po_line.product_qty
                    line.withdrawn_quantity = total
                else:
                    line.withdrawn_quantity = 0
            elif line.contract_ids.contract_type == 'transfer':
                total_withdrawn_quantity = 0.0
                contracts = line.contract_ids.orders
                for contract in contracts:
                    if contract.partner_id == line.contract_ids.customer:
                        for product in contract.order_line:
                            if product.product_id == line.product_id:
                                total_withdrawn_quantity += product.product_uom_qty
                line.withdrawn_quantity = total_withdrawn_quantity
            else:
                total_withdrawn_quantity = 0.0
                vehicles = line.contract_ids.vehicles
                if vehicles:
                    for vehicle in vehicles:
                        if vehicle.partner_id == line.contract_ids.customer and vehicle.service_id == line.product_id and vehicle.lot_id == line.lot_id:
                            qty = vehicle.loaded_qty
                            total_withdrawn_quantity += qty
                line.withdrawn_quantity = total_withdrawn_quantity

    def _compute_vehicles_qty_sent(self):
        for line in self:
            total_sent_quantity = 0.0
            orders = self.env['sale.order'].search([('contract_id', '=', line.contract_ids.id)])
            if orders:
                for order in orders:
                    for order_line in order.order_line:
                        if order_line.product_id == line.product_id:
                            total_sent_quantity += order_line.product_uom_qty
            line.quantity_sent = total_sent_quantity

    @api.depends('purchase_ids')
    def _compute_orders_number(self):
        for requisition in self:
            requisition.qty_entry_sent = len(requisition.purchase_ids)



    @api.onchange('product_id')
    def _get_lots_for_products(self):
        po = None
        lots = []
        if self.product_id:
            products_ids = self.env['stock.lot'].sudo().search([('product_id', '=', self.product_id.id)])
            print("@@@@@@@@@@@@@@@@@@@", products_ids)
            for lot in products_ids:
                print("lots is", lot.id)
                po = lot.id
                lots.append(lot.id)
                self.lots_id = lots
            print("po", po)
        if po:
            return {'domain': {'lot_id': [('id', 'in', lots)]}}
        else:
            return {'domain': {'lot_id': [('id', '=', False)]}}
















