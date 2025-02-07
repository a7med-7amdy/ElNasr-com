from odoo import api, fields, models


class StockAccountCustom(models.Model):
    _inherit = 'stock.location'
    _description = 'StockAccountCustom'

    location_stock_valuation_account_id = fields.Many2one(
        'account.account', "Stock Valuation Account",
        check_company=True,
        domain="[('deprecated', '=', False)]", )




class ProductCategory(models.Model):
    _inherit = 'product.category'

    property_stock_valuation_account_id = fields.Many2one(
        'account.account', 'Stock Valuation Account',
        company_dependent=True,
        domain="[('deprecated', '=', False)]",
        check_company=True,
        compute='_compute_property_stock_account',
        inverse='_set_property_stock_valuation_account_id',
        store=True
    )

    @api.depends('property_stock_valuation_account_id')
    def _compute_property_stock_account(self):
        for category in self:
            stock_location = self.env['stock.location'].search([
                ('usage', '=', 'internal'),
                ('company_id', '=', self.env.company.id)
            ], limit=1)

            if stock_location and stock_location.location_stock_valuation_account_id:
                category.property_stock_valuation_account_id = stock_location.location_stock_valuation_account_id
            else:
                category.property_stock_valuation_account_id = category.property_stock_valuation_account_id
