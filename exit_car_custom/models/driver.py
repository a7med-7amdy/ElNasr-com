from odoo import api, fields, models


class DriverCustom(models.Model):
    _name = 'driver.driver'
    _description = 'Driver Custom'

    name = fields.Char(
        string='Name',
        required=False)
    driver_license_number = fields.Char(
        string='Driver License Number',
        required=False)



class SoldCustom(models.Model):
    _name = 'sold.sold'
    _description = 'Driver Custom'

    name = fields.Char(
        string='Name',
        required=False)
    national_id = fields.Char(
        string='National Id', default=1,
        required=False)


