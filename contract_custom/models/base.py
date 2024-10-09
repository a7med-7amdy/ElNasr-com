from odoo import api, fields, models


class CompanySitting(models.Model):
    _inherit = 'res.company'

    debit_account = fields.Many2one('account.account',
                                    'Debit Account',
                                    required=False, )
    credit_account = fields.Many2one('account.account',
                                     'Credit Account',
                                     required=False, )
    journal_id = fields.Many2one('account.journal',
                                 string="Journal")


class NewModule(models.TransientModel):
    _inherit = 'res.config.settings'

    name = fields.Char()




    debit_account = fields.Many2one('account.account',
                                    'Debit Account',related='company_id.debit_account',readonly=False,
                                    required=False, )
    credit_account = fields.Many2one('account.account',related='company_id.credit_account',readonly=False,
                                     required=False, )
    journal_id = fields.Many2one('account.journal',related='company_id.journal_id',readonly=False,
                                 string="Journal")

