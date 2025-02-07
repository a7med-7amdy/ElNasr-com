from odoo import api, fields, models 

class CarTechnicalInspection(models.Model):
    _name = 'inspection.inspection'
    _description = 'CarTechnicalInspection'

    name = fields.Char(
        string='Name',
        required=False,readonly=True)
    date = fields.Datetime(
        string='Inspection Date',
        default=fields.Date.context_today,
        index=True,
        tracking=True,
        required=False)
    vehicle = fields.Many2one(
        comodel_name='fleet.vehicle',
        string='Vehicle',
        required=True)
    car_unit_number = fields.Char(
        string='Car Unit Number', related='vehicle.unit_number',
        required=False)
    car_license = fields.Char(
        string='Car License', related='vehicle.license_plate',
        required=False)
    car_Brand = fields.Char(
        string='Brand', related='vehicle.brand',
        required=False)
    kilometer = fields.Char(
        string='Kilometer',
        required=False)
    inspection_ids = fields.One2many(
        comodel_name='inspection.line',
        inverse_name='inspection_id',
        string='Inspections',
        required=False)
    request_id = fields.Many2one(
        comodel_name='request.request',
        string='Request',
        required=False)
    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'),
                   ('confirmed', 'Confirmed'),
                   ('order', 'Ordered'),
                   ('cancel', 'Canceled'),
                   ],default='draft',
        required=False, )
    orders_count = fields.Integer(
        string="Order Count",
        compute="_compute_order_count",
        store=False
    )

    def action_confirm(self):
        for rec in self:
            rec.state='confirmed'

    def action_cancel(self):
        for rec in self:
            rec.state='cancel'

    def reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_create_order(self):
        for rec in self:
            if rec.inspection_ids:
                order_vals = {
                    'vehicle': rec.vehicle.id,
                    'inspection_id': rec.id,
                    'kilometer': rec.kilometer,
                    'request_id': rec.request_id.id,
                    'order_ids': [(0, 0, {
                        'name': line.name,
                        'discreption': line.received_faults
                    }) for line in rec.inspection_ids],
                }
                order = self.env['car.order'].create(order_vals)

                return {
                    'name': 'Car Order',
                    'type': 'ir.actions.act_window',
                    'res_model': 'car.order',
                    'view_mode': 'form',
                    'res_id': order.id,  # Open the last created order
                    'context': {'default_vehicle': rec.vehicle.id},
                }

    @api.depends('name')  # Depends on the name because inspections are created based on the request
    def _compute_order_count(self):
        for rec in self:
            rec.orders_count = self.env['car.order'].search_count([('inspection_id', '=', rec.id)])

    def action_open_orders(self):
        """
        Open related inspections.
        """
        self.ensure_one()
        return {
            'name': 'Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'car.order',
            'view_mode': 'tree,form',
            'domain': [('inspection_id', '=', self.id)],
        }

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            seq = self.env['ir.sequence'].next_by_code('inspection.inspection') or '/'
            vals['name'] = seq
        return super(CarTechnicalInspection, self).create(vals)



class CarTechnicalInspectionLines(models.Model):
    _name = 'inspection.line'
    _description = 'CarTechnicalInspection'


    name = fields.Char(
        string='Name', readonly=True,
        required=False)
    received_faults = fields.Text(
        string='Received Faults',
        required=False)
    maintenance_specialist_inspection = fields.Text(
        string="specialist",
        required=False)
    maintenance_specialist_decision = fields.Text(
        string="Decision",
        required=False)
    fault_technician = fields.Many2one(
        comodel_name='hr.employee',
        string='Fault Technician',
        required=False)
    notes = fields.Text(
        string="Notes",
        required=False)
    inspection_id = fields.Many2one(
        comodel_name='inspection.inspection',
        string='inspection id',
        required=False)
    company_id = fields.Many2one('res.company', string='Company', change_default=True,
                                 default=lambda self: self.env.company)


    @api.model
    def create(self, vals):
        if 'inspection_id' in vals:
            inspection_id = vals['inspection_id']
            existing_count = self.search_count([('inspection_id', '=', inspection_id)])
            vals['name'] = f"Line-{existing_count + 1}"
        return super(CarTechnicalInspectionLines, self).create(vals)

    def write(self, vals):
        if 'inspection_id' in vals:
            inspection_id = vals['inspection_id']
            existing_count = self.search_count([('inspection_id', '=', inspection_id)])
            vals['name'] = f"Line-{existing_count + 1}"
        return super(CarTechnicalInspectionLines, self).write(vals)
