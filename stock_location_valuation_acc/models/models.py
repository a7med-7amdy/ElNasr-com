from odoo import models, fields,api,_

class StockLocation(models.Model):
    _inherit = 'stock.location'

    stock_val_account_id = fields.Many2one('account.account', string='Stock Valuation Account',
                                       help='This account will be used for stock journal entries when receiving goods.')

# models/stock_move.py

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _get_accounting_data_for_valuation(self):
        journal_id, acc_src, acc_dest, acc_valuation = super(StockMove,self)._get_accounting_data_for_valuation()
        loc_dest_account = self.location_dest_id.stock_val_account_id
        loc_src_account = self.location_id.stock_val_account_id
        if loc_dest_account:
            acc_valuation = loc_dest_account.id
        print(self.picking_code)
        if self.picking_code == 'incoming':  # Purchase
            if loc_dest_account:
                acc_valuation = acc_dest = loc_dest_account.id
            if loc_src_account:
                acc_src = loc_src_account.id
        elif self.picking_code == 'outgoing':  # Sales
            if loc_src_account:
                acc_valuation = acc_src = loc_src_account.id
            if loc_dest_account:
                acc_dest = loc_dest_account.id
        elif self.picking_code == 'internal':  # Internal Transfer
            if loc_src_account:
                acc_valuation = acc_src = loc_src_account.id
            if loc_dest_account:
                acc_dest = loc_dest_account.id
        elif self.picking_code == 'scrap':  # Scrap
            if loc_dest_account:
                acc_valuation = acc_src = loc_src_account.id
        print('MMMM>>>',journal_id, acc_src, acc_dest, acc_valuation)
        ac_model = self.env['account.account'].sudo()
        for ac in [ acc_src, acc_dest, acc_valuation]:
            print(ac_model.browse(ac).name)


        return journal_id, acc_src, acc_dest, acc_valuation




# class AccMove(models.Model):
#     _inherit = 'account.move'
#
#
#
#     @api.model
#     def create(self, values):
#         # Add code here
#         res = super(AccMove, self).create(values)
#         print(res.name)
#         print(res.state)
#         for l in res.line_ids:
#             print('l.account_id.name',l.account_id.name)
#             print('l.account_id.debit',l.debit)
#         return res
#
