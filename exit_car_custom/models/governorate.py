from odoo import api, fields, models 


class Governorate(models.Model):
    _name = 'governorate.governorate'
    _description = 'Governorate'

    name = fields.Char(
        string='Name',
        required=False)
    
