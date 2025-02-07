from odoo import api, fields, models

class CarExitDate(models.Model):
    _name = 'exit.exit'
    _description = 'Car Exit Date'

    name = fields.Char(
        string='Name',
        required=False)
    exit_date = fields.Datetime(
        string='Exit Data',
        required=False)
    Start_meter_reading  = fields.Float(
        string='Start Meter',default=1,
        required=False)
    end_meter_reading = fields.Float(
        string='End Meter',default=1,
        required=False)
    return_date = fields.Datetime(
        string='Return Data',
        required=False)
    distance = fields.Float(
        string='Distance',compute='get_distance_of_reding',store=True,default=1,
        required=False)
    secret_line = fields.Text(
        string="Secret Line",
        required=False)
    car_id = fields.Many2one(
        comodel_name='car.car',
        string='Car',
        required=False)


    @api.depends('Start_meter_reading','end_meter_reading')
    def get_distance_of_reding(self):
        for rec in self:
            if rec.Start_meter_reading or rec.end_meter_reading:
                rec.distance = rec.Start_meter_reading - rec.end_meter_reading
            else:
                rec.distance = 0






