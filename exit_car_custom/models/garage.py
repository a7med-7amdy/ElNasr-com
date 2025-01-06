from odoo import api, fields, models

class Garage(models.Model):
    _name = 'garage.garage'
    _description = 'Garage'

    name = fields.Char()

