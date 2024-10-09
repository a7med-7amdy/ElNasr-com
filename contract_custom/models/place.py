from odoo import api, fields, models 

class Places(models.Model):
    _name = 'place.place'
    _description = 'Places'

    name = fields.Char(string="string")

    
