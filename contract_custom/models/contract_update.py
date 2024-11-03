from odoo import api, fields, models,_


class ContractUpdate(models.Model):
    _name = 'contract.update'
    _description = 'Contract Update'

    name = fields.Char()
    contract_start_date = fields.Date(string='Contract Start Date')
    contract_end_date = fields.Date(string='Contract End Date')
    old_contract_start_date = fields.Date(string='Old Contract Start Date')
    old_contract_end_date = fields.Date(string='Old Contract End Date')
    old_lines_ids = fields.One2many('contract.update.line', 'contract_update_ids2', string='Old Contract Lines',required=True)
    new_lines_ids = fields.One2many('contract.update.line', 'contract_update_ids', string='New Contract Lines',required=True)
    contract_id = fields.Many2one('contract.contract', string="Contract")
    state = fields.Selection([
        ("update", "Updated"),
        ("return", "Return"),], string="Status", required=True, index=True, tracking=True, default="update", copy=False)


    @api.model
    def create(self, vals):
        '''sequence'''
        if 'name' not in vals or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('contract.update.seq') or _('New')
        return super(ContractUpdate, self).create(vals)

    def action_update(self):
        '''update'''
        # Fetch the contract record
        contract = self.env['contract.contract'].search([('id', '=', self.contract_id.id)], limit=1)

        # Initialize a list to hold the commands for updating contract lines
        contract_lines_commands = []

        for old_line in self.new_lines_ids:
            if old_line.product_id:
                # Extract necessary fields
                qty = old_line.qty
                price = old_line.price
                load_place_id = old_line.load_place.id if old_line.load_place else False
                unloading_place_id = old_line.unloading_place.id if old_line.unloading_place else False
                lot_id = old_line.new_lot_id.id if old_line.new_lot_id else False
                tax_ids = old_line.tax_id.ids if old_line.tax_id else []

                # Find existing lines with the same product and lot
                existing_lines = contract.contract_lines.filtered(
                    lambda cl: cl.product_id.id == old_line.product_id.id and cl.lot_id.id == lot_id
                )

                if existing_lines:
                    for line in existing_lines:
                        # Prepare the update command for existing lines
                        contract_lines_commands.append((1, line.id, {
                            'qty': line.qty + qty,
                            'price': line.price + price,
                            'load_place': load_place_id,
                            'unloading_place': unloading_place_id,
                            'tax_id': [(6, 0, list(set(line.tax_id.ids + tax_ids)))],  # Avoid duplicate taxes
                        }))
                else:
                    # Prepare the create command for new lines
                    contract_lines_commands.append((0, 0, {
                        'product_id': old_line.product_id.id,
                        'qty': qty,
                        'price': price,
                        'load_place': load_place_id,
                        'unloading_place': unloading_place_id,
                        'lot_id': lot_id,
                        'tax_id': [(6, 0, tax_ids)],
                    }))

        if contract_lines_commands:
            # Apply the commands to the contract lines
            contract.write({
                'contract_lines': contract_lines_commands
            })

        # Update the contract with the new commands
        contract.contract_lines = contract_lines_commands

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

    product_id = fields.Many2one('product.product', string='Product',required=True)
    qty = fields.Float(string='Quantity')
    price = fields.Float(string='Unit Price')
    load_place = fields.Many2one('place.place', string='Load Place')
    unloading_place = fields.Many2one('place.place', string='Unloading Location')
    contract_update_ids = fields.Many2one('contract.update')
    contract_update_ids2 = fields.Many2one('contract.update')

    old_product_id = fields.Many2one('product.product', string='Old Product',required=True)
    old_qty = fields.Float(string='Old Quantity')
    old_price = fields.Float(string='Old Unit Price')
    old_load_place = fields.Many2one('place.place', string='Old Load Place')
    old_unloading_place = fields.Many2one('place.place', string='Old Unloading Location')
    old_lot_id = fields.Many2one(
        'stock.lot',
        string='Operation',
    )
    lots_id = fields.Many2many(
        comodel_name='stock.lot',
        string='')
    new_lot_id = fields.Many2one(
        'stock.lot',
        string='Operation', domain="[('id', 'in', lots_id)]"
    )
    tax_id = fields.Many2many(
        comodel_name='account.tax',
        string="Taxes",
        store=True, readonly=False, precompute=True, )

