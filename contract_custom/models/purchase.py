from odoo import api, fields, models

class purchaseOrderCustom(models.Model):
    """
    Inherits the model purchase Order Line to extend and add extra field and method
    for the working of the app.
    """
    _inherit = 'purchase.order'



    contract_id = fields.Many2one(
        comodel_name='contract.contract',
        string='Contract',
        required=False)
    contract_ids = fields.Many2one(
        comodel_name='contract.contract',
        string='Contract Ids',
        required=False)


class purchaseOrderLineCustom(models.Model):
    """
    Inherits the model purchase Order Line to extend and add extra field and method
    for the working of the app.
    """
    _inherit = 'purchase.order.line'



    contract_id = fields.Many2one(comodel_name='contract.contract', related='order_id.contract_id')