from odoo import api, fields, models


class FleetCustom(models.Model):
    _inherit = 'fleet.vehicle'

    car_owner = fields.Many2one(
        comodel_name='res.partner',
        string='Car Owner',
        required=False)
    traffic = fields.Char(
        string='Traffic',
        required=False)
    license_date = fields.Date(
        string='License Date',
        required=False)
    license_end_date = fields.Date(
        string='License End Date',
        required=False)
