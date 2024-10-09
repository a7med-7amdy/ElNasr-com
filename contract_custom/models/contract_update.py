from odoo import api, fields, models


class ContractUpdate(models.Model):
    _name = 'contract.update'
    _description = 'Contract Update'

    name = fields.Char()
    contract_start_date = fields.Date(string='Contract Start Date')
    contract_end_date = fields.Date(string='Contract End Date')
    old_contract_start_date = fields.Date(string='Old Contract Start Date')
    old_contract_end_date = fields.Date(string='Old Contract End Date')
    old_lines_ids = fields.One2many('contract.update.line', 'contract_update_ids', string='Old Contract Lines')
    new_lines_ids = fields.One2many('contract.update.line', 'contract_update_ids', string='New Contract Lines')
    contract_id = fields.Many2one('contract.contract', string="Contract")
    state = fields.Selection([
        ("update", "Updated"),
        ("return", "Return"),], string="Status", required=True, index=True, tracking=True, default="update", copy=False)

    def action_update(self):
        contract = self.env['contract.contract'].search([('id', '=', self.contract_id.id)], limit=1)

        contract_lines_commands = []

        for old_line in self.new_lines_ids:
            if old_line.product_id:
                existing_lines = contract.contract_lines.filtered(
                    lambda cl: cl.product_id.id == old_line.product_id.id)
                if existing_lines:
                    existing_lines.unlink()
                contract_lines_commands.append((0, 0, {
                    'product_id': old_line.product_id.id,
                    'qty': old_line.qty,
                    'price': old_line.price,
                    'load_place': old_line.load_place.id,
                    'unloading_place': old_line.unloading_place.id
                }))
        contract.write({
            'contract_start_date': self.contract_start_date,
            'contract_end_date': self.contract_end_date,
            'contract_lines': contract_lines_commands,
        })
        for rec in self:
            rec.state = "return"




    def action_return(self):
        for rec in self:
            rec.state = "update"


class ContractUpdateLine(models.Model):
    _name = 'contract.update.line'
    _description = 'Contract Update Lines'

    product_id = fields.Many2one('product.product', string='Product')
    qty = fields.Float(string='Quantity')
    price = fields.Float(string='Unit Price')
    load_place = fields.Many2one('place.place', string='Load Place')
    unloading_place = fields.Many2one('place.place', string='Unloading Location')
    contract_update_ids = fields.Many2one('contract.update')

    old_product_id = fields.Many2one('product.product', string='Old Product')
    old_qty = fields.Float(string='Old Quantity')
    old_price = fields.Float(string='Old Unit Price')
    old_load_place = fields.Many2one('place.place', string='Old Load Place')
    old_unloading_place = fields.Many2one('place.place', string='Old Unloading Location')

