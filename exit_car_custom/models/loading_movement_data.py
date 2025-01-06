from odoo import api, fields, models


class LoadingMovementData(models.Model):
    _name = 'loading.loading'
    _description = 'LoadingMovementData'

    name = fields.Char(
        string='',
        required=False)
    attachment_number = fields.Char(
        string='Document',
        required=False)
    download_destination = fields.Many2one(
        comodel_name='res.partner',
        string='Destination',
        required=False)

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=False)
    manufacturing_entry_data = fields.Datetime(
        string='Entry Data',
        required=False)
    manufacturing_exit_data  = fields.Datetime(
        string='Exit Data',
        required=False)
    portion_client = fields.Many2one(
        comodel_name='stock.lot',
        string='Client Portion',
        required=False)
    loading_quantity = fields.Float(
        string='Loading Quantity',
        required=False)
    discharge_direction = fields.Many2one(
        comodel_name='res.partner',
        string='Direction',
        required=False)

    client_name = fields.Many2one(
        comodel_name='res.partner',
        string='Client',
        required=False)
    empty_quantity  = fields.Float(
        string='Empty Quantity',
        required=False)
    enter_empty_date = fields.Datetime(
        string='Empty Entry',
        required=False)
    exit_empty_date  = fields.Datetime(
        string='Empty Exit',
        required=False)
    notes  = fields.Char(
        string='Note', 
        required=False)
    car_id = fields.Many2one(
        comodel_name='car.car',
        string='',
        required=False)
