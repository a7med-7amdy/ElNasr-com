from odoo import api, fields, models


class PartnerCustomForContract(models.Model):
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
    is_coa_installed = fields.Integer(
        string='',
        required=False)

