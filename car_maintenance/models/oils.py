from odoo import api, fields, models ,_

class CarsOilsMaintenance(models.Model):
    _name = 'oil.oil'
    _description = 'Cars Oils Maintenance'

    name = fields.Char(
        string='Name',
        readonly=True,
        default=lambda self: _('New'))
    date = fields.Date(
        string='Request Date',
        default=fields.Date.today(),
        index=True,
        tracking=True,
        required=False)

    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'),
                   ('confirmed', 'Confirmed'), ('cancel', 'Cancel')],
        default='draft',
        required=False)
    oil_ids = fields.One2many(
        comodel_name='oil.line',
        inverse_name='oil_id',
        string='Oils',
        required=False)




    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('oil.oil') or _('New')
        return super(CarsOilsMaintenance, self).create(vals)


    
    
    
    
    
    
    def reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


class CarsOilsMaintenanceLines(models.Model):
    _name = 'oil.line'
    _description = 'Cars Oils Maintenance Lines'


    name = fields.Char(
        string='Name',
        required=False)
    maintenance_id = fields.Many2one(
        comodel_name='request.request',
        string='Maintenance',
        required=False)
    order_id = fields.Many2one(
        comodel_name='car.order',
        string='Order',
        required=False)
    vehicle = fields.Many2one(
        comodel_name='fleet.vehicle',
        string='Vehicles',
        required=False)
    car_code = fields.Many2one(
        comodel_name='code.code',
        string='Car Code',
        required=False)
    oil_type = fields.Many2one(
        comodel_name='oil.type',
        string='Oil Type',
        required=False)

    vehicles_numbers = fields.Integer(
        string='Vehicles Numbers',
        required=False)

    car_license = fields.Char(related='vehicle.license_plate',
                              readonly=True)
    kilometer = fields.Char(
        string='Kilometer',
        required=True)
    change_type = fields.Many2one(
        comodel_name='change.change',
        string='Change Type',
        required=False)
    oil_kilometer  = fields.Char(
        string='Oil Kilometer', 
        required=False)
    filter_type = fields.Many2one(
        comodel_name='filter.filter',
        string='Filter Type',
        required=False)
    filter_km  = fields.Char(
        string='Filter KM',
        required=False)
    oil_id = fields.Many2one(
        comodel_name='oil.oil',
        string='oil',
        required=False)
    time_start = fields.Datetime(string='Start Time', required=False)
    time_end = fields.Datetime(string='End Time', required=False)

    difference = fields.Float(
        string='Hours',
        compute='_compute_difference',
        store=True
    )

    @api.onchange('car_code')
    def _onchange_car_code(self):
        if self.car_code:
            vehicle = self.env['fleet.vehicle'].search([('car_code', '=', self.car_code.id)], limit=1)
            if vehicle:
                self.vehicle = vehicle if vehicle else False


    @api.depends('time_start', 'time_end')
    def _compute_difference(self):
        for record in self:
            if record.time_start and record.time_end:
                duration = record.time_end - record.time_start
                record.difference = duration.total_seconds() / 3600  # Convert seconds to hours
            else:
                record.difference = 0.0

    
    
    
class Changes(models.Model):
    _name = 'change.change'
    _description = 'CarChanges'

    name = fields.Char()
    
    
class FilterForCar(models.Model):
    _name = 'filter.filter'
    _description = 'FilterForCar'

    name = fields.Char()
    
    
class OilType(models.Model):
    _name = 'oil.type'
    _description = 'OilType'

    name = fields.Char()
    kilometer = fields.Float(
        string='Kilometer',
        required=False)
    work_hours = fields.Float(
        string='Work Hours',
        required=False)
    

    

    
