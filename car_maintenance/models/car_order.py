from odoo import api, fields, models ,_

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




class HrTimesheetSheetCustom(models.Model):
    _name = 'account.analytic.custom'
    _description = 'HrTimesheetSheet'

    name = fields.Char(
        string='',
        required=False)



    car_repair_request_id = fields.Many2one(
        'car.order',
        string="Repair Request"
    )
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
        required=False)
    start_date = fields.Datetime(
        string='Start Date',
        required=False)
    end_date = fields.Datetime(
        string='End Date',
        required=False)
    time_difference = fields.Float(
        string='Hours',
        compute='_compute_time_difference',
        store=True,
        help="Difference in time (hours) between Start Date and End Date")
    hourly_cost = fields.Monetary(
        string='Hour Cost',related='employee_id.hourly_cost',readonly=False,
        required=False)
    total_cost = fields.Monetary(
        string='Total', compute='_compute_total_cost', store=True,
        required=False)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )

    @api.depends('hourly_cost','time_difference')
    def _compute_total_cost(self):
        for rec in self:
            if rec.hourly_cost or rec.time_difference:
                rec.total_cost = rec.time_difference * rec.hourly_cost
            else:
                rec.total_cost = 0

    @api.depends('start_date', 'end_date')
    def _compute_time_difference(self):
        for record in self:
            if record.start_date and record.end_date:
                # Extract only the time part from datetime fields
                start_time = record.start_date.time()
                end_time = record.end_date.time()

                # Convert time to seconds for difference calculation
                start_seconds = (start_time.hour * 3600) + (start_time.minute * 60) + start_time.second
                end_seconds = (end_time.hour * 3600) + (end_time.minute * 60) + end_time.second

                # Calculate the difference in hours
                diff_seconds = end_seconds - start_seconds
                record.time_difference = diff_seconds / 3600.0
            else:
                record.time_difference = 0.0



class CarOrderLine(models.Model):
    _name = 'order.line'
    _description = 'CarOrderLine'

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



class MaterialRequisitionCarRepair(models.Model):
    _name = "material.requisition.car.repair"
    _description = 'material.requisition.car.repair'

    requisition_id = fields.Many2one(
        'car.order',
        string='Requisitions',
    )
    custom_requisition_line_id = fields.Many2one(
        'material.purchase.requisition.line',
        string='Requisition Line',
        copy=False,
        readonly=True
    )
    # custom_material_requisition_id = fields.Many2one(
    #     'material.purchase.requisition',
    #     string='Material Requisition',
    #     related ='custom_requisition_line_id.requisition_id',
    #     copy=False,
    #     readonly=True,
    # )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
    )
    qty = fields.Float(
        string='Quantity',
        default=1,
        required=True,
    )
    uom = fields.Many2one(
        'uom.uom',
        string='Unit of Measure',
        required=True,
    )
    description = fields.Char(
        string='Description',
        required=True,
    )
    requisition_type = fields.Selection(
        selection=[
                    ('internal','Internal Picking'),
                    ('purchase','Purchase Order'),
        ],
        string='Requisition Action',
        default='purchase',
        required=True,
    )

    @api.onchange('product_id')
    def onchange_product_id(self):
        for rec in self:
            rec.description = rec.product_id.name
            rec.uom = rec.product_id.uom_id.id


class MaterialPurchaseRequisitionLine(models.Model):
    _name = "material.purchase.requisition.line"
    _description = 'Material Purchase Requisition Lines'

    requisition_id = fields.Many2one(
        'material.purchase.requisition',
        string='Requisitions',
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
    )
    #     layout_category_id = fields.Many2one(
    #         'sale.layout_category',
    #         string='Section',
    #     )
    description = fields.Char(
        string='Description',
        required=True,
    )
    qty = fields.Float(
        string='Quantity',
        default=1,
        required=True,
    )
    uom = fields.Many2one(
        'uom.uom',  # product.uom in odoo11
        string='Unit of Measure',
        required=True,
    )
    partner_id = fields.Many2many(
        'res.partner',
        string='Vendors',
    )
    requisition_type = fields.Selection(
        selection=[
            ('internal', 'Internal Picking'),
            ('purchase', 'Purchase Order'),
        ],
        string='Requisition Action',
        default='purchase',
        required=True,
    )

    @api.onchange('product_id')
    def onchange_product_id(self):
        for rec in self:
            # rec.description = rec.product_id.name
            rec.description = rec.product_id.display_name
            rec.uom = rec.product_id.uom_id.id



    
