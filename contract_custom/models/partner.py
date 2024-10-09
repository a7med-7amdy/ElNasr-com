from odoo import api, fields, models


class NewModule(models.Model):
    _inherit = 'res.partner'

    construction_date = fields.Date(
        string='Construction Date',
        required=False)
    mixing_date = fields.Date(
        string='Mixing Date',
        required=False)
    commercial_registration_number = fields.Char(
        string='Commercial Registration Number',
        required=False)
