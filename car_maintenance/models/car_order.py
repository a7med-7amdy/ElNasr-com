from odoo import api, fields, models ,_
from odoo.exceptions import UserError


class CarJobOrder(models.Model):
    _name = 'car.order'
    _description = 'CarJobOrder'


    name = fields.Char(
        string='Order Name',
        required=False,
        readonly=True,
        default=lambda self: _('New'))
    vehicle = fields.Many2one(
        comodel_name='fleet.vehicle',
        string='Vehicle',
        required=True)
    car_unit_number = fields.Char(related='vehicle.unit_number',
                                  readonly=True)
    car_license = fields.Char(related='vehicle.license_plate',
                              readonly=True)
    car_Brand = fields.Char(
        string='Brand', related='vehicle.brand',
        required=False)
    kilometer = fields.Char(
        string='Kilometer',
        required=False)
    date = fields.Datetime(
        string='Order Date',
        default=fields.Date.context_today,
        index=True,
        tracking=True,
        required=False)
    order_ids = fields.One2many(
        comodel_name='order.line',
        inverse_name='order_id',
        string='Lines',
        required=False)
    inspection_id = fields.Many2one(
        comodel_name='inspection.inspection',
        string='inspection_id',
        required=False)
    request_id = fields.Many2one(
        comodel_name='request.request',
        string='Request',
        required=False)
    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'),
                   ('confirmed', 'Confirmed'),
                   ('done', 'Done'),
                   ('cancel', 'Canceled'),
                   ], default='draft',
        required=False, )
    timesheet_line_ids = fields.One2many(
        'account.analytic.custom',
        'car_repair_request_id',
        string='Timesheets',
    )
    material_requisition_car_repair_ids = fields.One2many(
        'material.requisition.car.repair',
        'requisition_id',
        string='Material Requisitions Car Repair',
        copy=False,
    )

    requisition_count = fields.Integer(
        compute='_compute_requisition_counter',
        string="Requisition Count",
    )

    total_hours = fields.Float(
        string='Total Hours',
        compute='_compute_total_hours_and_cost',
        store=True,
    )
    total_cost = fields.Monetary(
        string='Total Cost',
        compute='_compute_total_hours_and_cost',
        store=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )

    # Existing fields ...

    purchase_order_ids = fields.One2many(
        'purchase.order',
        'origin_car_order_id',
        string='Purchase Orders',
        readonly=True,
    )
    purchase_order_count = fields.Integer(
        compute='_compute_purchase_order_count',
        string='Purchase Order Count',
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Vendor',
        required=False)
    total_cost_requisitions = fields.Monetary(
        string='Total Cost',
        compute='_compute_total_cost',
        currency_field='currency_id',  # Use the appropriate currency field
        store=True,
        help='Total cost from all material requisitions'
    )

    total_required_quantity = fields.Float(
        string='Total Required Quantity',
        compute='_compute_total_required_quantity',
        store=True,
        help='Total required quantity calculated from all material requisitions'
    )
    location_id = fields.Many2one(
        'stock.location',
        string='Source Location',
        help='Default source location for internal transfers.',
        required=False,
    )
    oil_ids = fields.One2many(
        comodel_name='oil.line',
        inverse_name='order_id',
        string='Oils',
        required=False)
    maintenance_id = fields.Many2one(
        comodel_name='request.request',
        string='Maintenance',
        required=False)

    # Many2many for labors from timesheets
    labour_ids = fields.Many2many('hr.employee', string="Labours", compute="_compute_labour_ids", store=True)

    # Total cost of timesheet labors
    total_labour_cost = fields.Float(string="Total Labour Cost", compute="_compute_total_labour_cost", store=True)

    # Many2many for products from requisition lines
    product_ids = fields.Many2many('product.product', string="Products", compute="_compute_product_ids", store=True)

    # Total cost of requisition products based on stock valuation layer
    total_product_cost = fields.Float(string="Total Product Cost", compute="_compute_total_product_cost", store=True)

    @api.depends('timesheet_line_ids.employee_id')
    def _compute_labour_ids(self):
        for order in self:
            order.labour_ids = order.timesheet_line_ids.mapped('employee_id')

    @api.depends('timesheet_line_ids.total_cost')
    def _compute_total_labour_cost(self):
        for order in self:
            order.total_labour_cost = sum(order.timesheet_line_ids.mapped('total_cost'))

    @api.depends('material_requisition_car_repair_ids.product_id')
    def _compute_product_ids(self):
        for order in self:
            order.product_ids = order.material_requisition_car_repair_ids.mapped('product_id')

    @api.depends('product_ids')
    def _compute_total_product_cost(self):
        for order in self:
            total_cost = 0.0
            for product in order.product_ids:
                valuation_layer = self.env['stock.valuation.layer'].search([('product_id', '=', product.id)],
                                                                           order="create_date desc", limit=1)
                if valuation_layer:
                    total_cost += valuation_layer.unit_cost * sum(
                        order.material_requisition_car_repair_ids.filtered(lambda r: r.product_id == product).mapped(
                            'product_uom_qty'))
            order.total_product_cost = total_cost

    @api.depends('material_requisition_car_repair_ids.required')
    def _compute_total_required_quantity(self):
        for order in self:
            total_required = sum(line.required for line in order.material_requisition_car_repair_ids)
            order.total_required_quantity = total_required

    @api.depends('material_requisition_car_repair_ids.total_cost')
    def _compute_total_cost(self):
        for order in self:
            total = sum(order.material_requisition_car_repair_ids.mapped('total_cost'))
            order.total_cost_requisitions = total

    def create_purchase_order(self):
        """Create Purchase Orders for lines with product_uom_qty = 0."""
        self.ensure_one()  # Ensure this method is called on a single record
        if not self.material_requisition_car_repair_ids:
            raise UserError(_('Please create requisition lines first!'))

        purchase_order = self.env['purchase.order'].create({
            'partner_id': self.partner_id.id if hasattr(self, 'partner_id') else None,
            'origin': self.name,
            'origin_car_order_id': self.id,
            'order_line': [
                (0, 0, {
                    'product_id': line.product_id.id,
                    'name': line.description or line.product_id.name,
                    'product_qty': line.required or 1,  # Default qty for purchase
                    'product_uom': line.product_uom.id,
                    'price_unit': line.product_id.standard_price,
                    'date_planned': fields.Datetime.now(),
                    'requisition_line': line.id,
                }) for line in self.material_requisition_car_repair_ids
            ],
        })

        # Return action to open the created purchase order
        return {
            'name': _('Purchase Order'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.order',
            'res_id': purchase_order.id,
            'type': 'ir.actions.act_window',
            'target': 'current',  # Open in the same window
        }


    @api.depends('purchase_order_ids')
    def _compute_purchase_order_count(self):
        for record in self:
            record.purchase_order_count = len(record.purchase_order_ids)

    def action_open_purchase_orders(self):
        """Open related purchase orders."""
        self.ensure_one()
        return {
            'name': _('Purchase Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'domain': [('origin_car_order_id', '=', self.id)],
        }


    picking_ids = fields.One2many('stock.picking', 'picking_id', string="Pickings", readonly=True)
    picking_count = fields.Integer(string="Picking Count", compute='_compute_picking_count', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', change_default=True,
                                 default=lambda self: self.env.company)

    def _compute_picking_count(self):
        for record in self:
            record.picking_count = len(record.picking_ids)

    def action_open_pickings(self):
        """Open related picking orders."""
        picking_ids = self.env['stock.picking'].search([('origin', '=', self.name)]).ids
        return {
            'name': _('Car Picking Order'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',  # Corrected model
            'type': 'ir.actions.act_window',
            'domain': [('picking_id', '=', self.id)],
            'context': self.env.context,
        }

    def create_piking_order(self):
        """Create an Internal Picking Order for Car Orders."""
        for rec in self:
            if not rec.location_id or not rec.company_id.location_dest_id:
                raise UserError(
                    _('Please set Source and Destination Locations for Internal Picking in the Company Settings!'))
            if not rec.material_requisition_car_repair_ids:
                raise UserError(
                    _('Please Create Requisition Lines!'))

            picking = self.env['stock.picking'].sudo().create({
                'picking_type_id': self.env.ref('stock.picking_type_internal').id,
                'location_id': rec.location_id.id,
                'location_dest_id': rec.company_id.location_dest_id.id,
                'picking_id': rec.id,
                'partner_id': rec.partner_id.id if hasattr(rec, 'partner_id') else None,
                'origin': rec.name,  # Link the picking to the current record
                'move_ids_without_package': [
                    (0, 0, {
                        'name': line.description,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_uom_qty,
                        'product_uom': line.product_uom.id,
                        'location_id': rec.location_id.id,
                        'location_dest_id': rec.company_id.location_dest_id.id,
                        'analytic_distribution': {rec.vehicle.analytic_account_id.id: 100},
                    }) for line in rec.material_requisition_car_repair_ids if line.product_uom_qty > 0
                ],
            })





    @api.depends('timesheet_line_ids.time_difference', 'timesheet_line_ids.total_cost')
    def _compute_total_hours_and_cost(self):
        for order in self:
            order.total_hours = sum(line.time_difference for line in order.timesheet_line_ids)
            order.total_cost = sum(line.total_cost for line in order.timesheet_line_ids)


    # @api.multi
    def action_material_requisition(self):
        self.ensure_one()
        # action = self.env.ref('car_repair_material_requisition.car_action_material_purchase_requisition').sudo().read()[0]
        action = self.env['ir.actions.actions']._for_xml_id(
            'car_repair_material_requisition.car_action_material_purchase_requisition')
        # action['domain'] = [('custom_car_repair_id','in', self.ids)]
        action['domain'] = [('custom_car_repair_id', '=', self.id)]
        return action

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('car.order') or _('New')
        return super(CarJobOrder, self).create(vals)
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_done(self):
        for rec in self:
            rec.state = 'done'


class CarOrderLine(models.Model):
    _name = 'order.line'
    _description = 'CarOrderLine'

    company_id = fields.Many2one('res.company', string='Company', change_default=True,
                                 default=lambda self: self.env.company)
    name = fields.Char(
        string='Name',readonly=True,
        required=False)
    discreption = fields.Text(
        string='Discreption',
        required=True)
    order_id = fields.Many2one(
        comodel_name='car.order',
        string='request',
        required=False)


    @api.model
    def create(self, vals):
        if 'inspection_id' in vals:
            inspection_id = vals['inspection_id']
            existing_count = self.search_count([('inspection_id', '=', inspection_id)])
            vals['name'] = f"Line-{existing_count + 1}"
        return super(CarOrderLine, self).create(vals)

    def write(self, vals):
        if 'inspection_id' in vals:
            inspection_id = vals['inspection_id']
            existing_count = self.search_count([('inspection_id', '=', inspection_id)])
            vals['name'] = f"Line-{existing_count + 1}"
        return super(CarOrderLine, self).write(vals)





    
