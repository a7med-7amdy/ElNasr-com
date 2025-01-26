from odoo import api, fields, models


class CarCompanySitting(models.Model):
    _inherit = 'res.company'

    location_id = fields.Many2one(
        'stock.location',
        string='Source Location',
        help='Default source location for internal transfers.',
        required=False,
    )
    location_dest_id = fields.Many2one(
        'stock.location',
        string='Destination Location',
        help='Default destination location for internal transfers.',
        required=False,
    )


class CarSittingCustom(models.TransientModel):
    _inherit = 'res.config.settings'

    
    location_id = fields.Many2one(
        'stock.location',related='company_id.location_id',
        string='Source Location',
        help='Default source location for internal transfers.',
        required=False,readonly=False,
    )
    location_dest_id = fields.Many2one(
        'stock.location',
        string='Destination Location',
        help='Default destination location for internal transfers.',related='company_id.location_dest_id',
        required=False,readonly=False,
    )