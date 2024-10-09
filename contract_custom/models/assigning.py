from odoo import api, fields, models 

class AssignParty(models.Model):
    _name = 'assign.assign'
    _description = 'Assign Party'

    name = fields.Char()
    
