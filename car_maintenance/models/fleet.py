from odoo import api, fields, models


class FleetVehicleCustom(models.Model):
    _inherit = 'fleet.vehicle'


    unit_number = fields.Char(
        string='Unit Number',
        required=False)
    brand = fields.Char(
        string='Brand',
        required=False)
    loading = fields.Char(
        string='Loading',
        required=False)