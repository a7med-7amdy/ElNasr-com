from odoo import api, fields, models


class CarCompanySitting(models.Model):
    _inherit = 'res.company'


    location_dest_id = fields.Many2one(
        'stock.location',
        string='Destination Location',
        help='Default destination location for internal transfers.',
        required=False,
    )


class CarSittingCustom(models.TransientModel):
    _inherit = 'res.config.settings'

    

    location_dest_id = fields.Many2one(
        'stock.location',
        string='Destination Location',
        help='Default destination location for internal transfers.',related='company_id.location_dest_id',
        required=False,readonly=False,
    )