from odoo import api, fields, models,_

class CarsCustom(models.Model):
    _name = 'car.car'
    _description = 'CarsCustom'

    name = fields.Char(
        string='أمر شغل',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('car.car') or _('New')
        return super(CarsCustom, self).create(vals)
    # الجراج
    garage = fields.Many2one(
        comodel_name='garage.garage',
        string='The garage',
        required=True)
    # المحافظة
    governorate_id = fields.Many2one(
        comodel_name='governorate.governorate',
        string='Governorate',
        required=True)
    manufacturing_id = fields.Many2one(
        comodel_name='manufacturing.manufacturing',
        string='Manufacturing',
        required=False)
    car_data = fields.Many2one(
        comodel_name='fleet.vehicle',
        string='Car Data', domain=[('trailer','=',False)],
        required=True)
    car_unit_number = fields.Char(
        string='Car Unit Number',related ='car_data.unit_number',
        required=False)
    car_license = fields.Char(
        string='Car License',related ='car_data.license_plate',
        required=False)
    car_Brand = fields.Char(
        string='Brand',related ='car_data.brand',
        required=False)
    trailer_data = fields.Many2one(
        comodel_name='fleet.vehicle',
        string='Trailer Data', domain=[('trailer', '=', True)],
        required=True)
    trailer_unit_number = fields.Char(
        string='Trailer Unit Number', related='trailer_data.unit_number',
        required=False)
    trailer_license = fields.Char(
        string='Trailer License', related='trailer_data.license_plate',
        required=False)
    trailer_loading  = fields.Char(
        string='Trailer Loading', related='trailer_data.loading',
        required=False)
    driver = fields.Many2one(
        comodel_name='driver.driver',
        string='Driver',
        required=False)
    driver_license_number = fields.Char(
        string='Driver License Number',related='driver.driver_license_number',
        required=False)
    driver_sold_name = fields.Many2one(
        comodel_name='sold.sold',
        string='Driver Sold Name',
        required=False)
    national_id = fields.Char(
        string='National Id', default=1,related='driver_sold_name.national_id',
        required=False)
    exit_ids = fields.One2many(
        comodel_name='exit.exit',
        inverse_name='car_id',
        string='Loading Data',
        required=False)
    move_ids = fields.One2many(
        comodel_name='loading.loading',
        inverse_name='car_id',
        string='Movement Data',
        required=False)



    

