from odoo import api, fields, models ,_

class CarJobOrder(models.Model):
    _name = 'car.order'
    _description = 'CarJobOrder'


    name = fields.Char(
        string='Order Name',
        required=False,
        readonly=True,
        default=lambda self: _('New'))
    vehicle = fields.Many2one(
        comodel_name='fleet.vehicle',
        string='Vehicle',
        required=True)
    car_unit_number = fields.Char(related='vehicle.unit_number',
                                  readonly=True)
    car_license = fields.Char(related='vehicle.license_plate',
                              readonly=True)
    car_Brand = fields.Char(
        string='Brand', related='vehicle.brand',
        required=False)
    kilometer = fields.Char(
        string='Kilometer',
        required=False)
    date = fields.Datetime(
        string='Order Date',
        default=fields.Date.context_today,
        index=True,
        tracking=True,
        required=False)
    order_ids = fields.One2many(
        comodel_name='order.line',
        inverse_name='order_id',
        string='Lines',
        required=False)
    inspection_id = fields.Many2one(
        comodel_name='inspection.inspection',
        string='inspection_id',
        required=False)
    request_id = fields.Many2one(
        comodel_name='request.request',
        string='Request',
        required=False)
    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'),
                   ('confirmed', 'Confirmed'),
                   ('done', 'Done'),
                   ('cancel', 'Canceled'),
                   ], default='draft',
        required=False, )

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('car.order') or _('New')
        return super(CarJobOrder, self).create(vals)
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
    #
    # def action_open_inspection(self):
    #     """
    #     Open related inspections.
    #     """
    #     self.ensure_one()
    #     return {
    #         'name': 'Inspections',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'inspection.inspection',
    #         'view_mode': 'tree,form',
    #         'domain': [('request_id', '=', self.id)],
    #         'context': {'default_vehicle': self.vehicle.id},
    #     }


class CarOrderLine(models.Model):
    _name = 'order.line'
    _description = 'CarOrderLine'

    name = fields.Char(
        string='Name',readonly=True,
        required=False)
    discreption = fields.Text(
        string='Discreption',
        required=True)
    order_id = fields.Many2one(
        comodel_name='car.order',
        string='request',
        required=False)


    @api.model
    def create(self, vals):
        if 'inspection_id' in vals:
            inspection_id = vals['inspection_id']
            existing_count = self.search_count([('inspection_id', '=', inspection_id)])
            vals['name'] = f"Line-{existing_count + 1}"
        return super(CarOrderLine, self).create(vals)

    def write(self, vals):
        if 'inspection_id' in vals:
            inspection_id = vals['inspection_id']
            existing_count = self.search_count([('inspection_id', '=', inspection_id)])
            vals['name'] = f"Line-{existing_count + 1}"
        return super(CarOrderLine, self).write(vals)



    
