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

    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('contract.update.seq')
        return super(ContractUpdateWizard, self).create(vals)

    def create_update_for_contract(self):
        self.env['contract.update'].create({
            'name': self.name,
            'contract_start_date': self.contract_start_date,
            'contract_end_date': self.contract_end_date,
            'old_contract_start_date': self.old_contract_start_date,
            'old_contract_end_date': self.old_contract_end_date,
            'contract_id': self.contract_id.id,
            'old_lines_ids': [(0, 0, {
                'old_product_id': old_line.old_product_id.id,
                'old_qty': old_line.old_qty,
                'old_price': old_line.old_price,
                'old_load_place': old_line.old_load_place.id,
                'old_unloading_place': old_line.old_unloading_place.id
            }) for old_line in self.old_lines_ids],
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








