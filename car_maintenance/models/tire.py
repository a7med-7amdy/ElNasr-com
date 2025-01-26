from odoo import api, fields, models

class CarsTire(models.Model):
    _name = 'tire.tire'
    _description = 'Cars Tire'

    name = fields.Char(
        string='Name',
        required=True,
        default='/',
        readonly=True)
    kilometer = fields.Char(
        string='Kilometer',
        required=True)
    change_date = fields.Date(
        string='Change Date',
        required=True)
    tire_type = fields.Many2one(
        comodel_name='tire.type',
        string='Tire Type',
        required=True)
    year_of_manufacturing = fields.Date(
        string='Manufacturing Date',
        required=True)
    number_of_tires = fields.Integer(
        string='Number Of Tires',
        required=False)
    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'),
                   ('confirmed', 'Confirmed'), ('cancel', 'Cancel')],
        default='draft',
        required=False)
    notes = fields.Text(
        string="Notes",
        required=False)

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('tire.tire') or '/'
        return super(CarsTire, self).create(vals)

    def reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


class TireType(models.Model):
    _name = 'tire.type'
    _description = 'TireType'

    name = fields.Char()


    def reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


class TireType(models.Model):
    _name = 'tire.type'
    _description = 'TireType'

    name = fields.Char()
    

