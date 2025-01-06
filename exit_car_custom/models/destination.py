from odoo import api, fields, models 

class Destination(models.Model):
    _name = 'destination.destination'
    _description = 'Destination'

    name = fields.Char(
        string='Name',
        required=False)
    
