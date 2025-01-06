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
    Start_meter_reading  = fields.Char(
        string='Start Meter Reading',
        required=False)
    return_date = fields.Datetime(
        string='Return Data',
        required=False)
    distance = fields.Char(
        string='Distance',
        required=False)
    secret_line = fields.Text(
        string="Secret Line",
        required=False)
    car_id = fields.Many2one(
        comodel_name='car.car',
        string='Car',
        required=False)

