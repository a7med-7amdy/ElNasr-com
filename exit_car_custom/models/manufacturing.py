from odoo import api, fields, models 

class Manufacturing(models.Model):
    _name = 'manufacturing.manufacturing'
    _description = 'Manufacturing'

    name = fields.Char(
        string='Name',
        required=False)
    
