# -*- coding: utf-8 -*-

from odoo import models, fields,api,_



class SaleOrder(models.Model):
    _inherit = 'sale.order'
    vehicle_move_ids= fields.One2many(comodel_name='vehicle.move', inverse_name='sale_id',string='Vehicle Move',)
    vehicle_move_count = fields.Integer(
        string='Vehicle Moves Count',
        compute='get_vehicle_move_count')

    @api.depends('vehicle_move_ids')
    def get_vehicle_move_count(self):
        for rec in self:
            rec.vehicle_move_count = len(rec.vehicle_move_ids)


    def action_view_vehicle_moves(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'name': _('Vehicle Moves'),
            'res_model': 'vehicle.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.vehicle_move_ids.ids)],
            'context': dict(self._context, default_partner_id=self.partner_id.id ,default_sale_id=self.id  )
        }
        if self.vehicle_move_count == 1:
            action.update({
                'view_mode': 'form',
                'res_id': self.vehicle_move_ids.id
            })
        return action


class AccountMove(models.Model):
    _inherit = 'account.move'
    vehicle_move_ids = fields.One2many(comodel_name='vehicle.move', inverse_name='invoice_id', string='Vehicle Move', )
    vehicle_move_count = fields.Integer(
        string='Vehicle Moves Count',
        compute='get_vehicle_move_count')

    @api.depends('vehicle_move_ids')
    def get_vehicle_move_count(self):
        for rec in self:
            rec.vehicle_move_count = len(rec.vehicle_move_ids)

    def action_view_vehicle_moves(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'name': _('Vehicle Moves'),
            'res_model': 'vehicle.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.vehicle_move_ids.ids)],
            'context':  {     'create':False, 'delete':False,
            'edit':False}
        }
        if self.vehicle_move_count == 1:
            action.update({
                'view_mode': 'form',
                'res_id': self.vehicle_move_ids.id
            })
        return action


