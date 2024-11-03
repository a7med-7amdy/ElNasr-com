from odoo import api, fields, models


class ContractUpdateWizard(models.TransientModel):
    _name = 'contract.update.wizard'
    _description = 'Contract Update Wizard'

    name = fields.Char(string='Update Name')
    contract_start_date = fields.Date(string='Contract Start Date')
    contract_end_date = fields.Date(string='Contract End Date')
    old_contract_start_date = fields.Date(string='Old Contract Start Date')
    old_contract_end_date = fields.Date(string='Old Contract End Date')
    old_lines_ids = fields.One2many('contract.update.wizard.line', 'contract_update_id', string='Old Contract Lines')
    new_lines_ids = fields.One2many('contract.update.wizard.line', 'contract_update_id', string='New Contract Lines')
    contract_id = fields.Many2one('contract.contract', string="Contract")

    def create_update_for_contract(self):
        # Filter lines to include only non-empty values
        list_1 = [(0, 0, {
            'old_product_id': old_line.old_product_id.id,
            'old_qty': old_line.old_qty,
            'old_price': old_line.old_price,
            'tax_id': old_line.tax_id.ids,
            'old_load_place': old_line.old_load_place.id if old_line.old_load_place else None,
            'old_unloading_place': old_line.old_unloading_place.id if old_line.old_unloading_place else None,
            'old_lot_id': old_line.lot_id.id if old_line.lot_id else None,
        }) for old_line in self.old_lines_ids if
                  old_line.old_product_id and old_line.old_qty > 0 and old_line.old_price > 0]

        list_2 = [(0, 0, {
            'product_id': new_line.old_product_id.id,
            'qty': new_line.old_qty,
            'price': new_line.old_price,
            'tax_id': new_line.tax_id.ids,
            'load_place': new_line.old_load_place.id if new_line.old_load_place else None,
            'unloading_place': new_line.old_unloading_place.id if new_line.old_unloading_place else None,
            'new_lot_id': new_line.lot_id.id if new_line.lot_id else None
        }) for new_line in self.new_lines_ids if
                  new_line.old_product_id and new_line.old_qty > 0 and new_line.old_price > 0]

        # Set list to False if empty to avoid creating empty lines
        list_1 = list_1 if list_1 else False
        list_2 = list_2 if list_2 else False

        self.env['contract.update'].create({
            'contract_start_date': self.contract_start_date,
            'contract_end_date': self.contract_end_date,
            'old_contract_start_date': self.old_contract_start_date,
            'old_contract_end_date': self.old_contract_end_date,
            'contract_id': self.contract_id.id,
            'old_lines_ids': list_1,
            'new_lines_ids': list_2,
        })


class ContractUpdateWizardLine(models.TransientModel):
    _name = 'contract.update.wizard.line'
    _description = 'Contract Update Wizard Lines'

    name = fields.Char()
    product_id = fields.Many2one('product.product', string='Product')
    qty = fields.Float(string='Quantity')
    price = fields.Float(string='Unit Price')
    load_place = fields.Many2one('place.place', string='Load Place')
    unloading_place = fields.Many2one('place.place', string='Unloading Location')
    contract_update_id = fields.Many2one('contract.update.wizard')
    old_product_id = fields.Many2one('product.product', string='Old Product')
    old_qty = fields.Float(string='Old Quantity')
    old_price = fields.Float(string='Old Unit Price')
    old_load_place = fields.Many2one('place.place', string='Old Load Place')
    old_unloading_place = fields.Many2one('place.place', string='Old Unloading Location')
    lot_id = fields.Many2one('stock.lot',string='Operation', domain="[('id', 'in', lots_id)]")
    tax_id = fields.Many2many(
        comodel_name='account.tax',
        string="Taxes",
        store=True, readonly=False, precompute=True, )








