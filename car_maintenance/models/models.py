from email.policy import default

from odoo import api, fields, models

class CarRequestForMaintenance(models.Model):
    _name = 'request.request'
    _description = 'CarRequestForMaintenance'

    name = fields.Char(
        string='Name',
        required=False,readonly=True)
    date = fields.Datetime(
        string='Request Date',
        default=fields.Date.context_today,
        index=True,
        tracking=True,
        required=False)
    technical_name = fields.Many2one(
        comodel_name='res.partner',
        string='Technical Name',
        required=True)
    malfunction = fields.Char(
        string='Malfunction Place',
        required=True)
    malfunction_type = fields.Selection(
        string='Malfunction Type',
        selection=[('internal', 'Internal'),
                   ('external', 'External'), ],default='internal',
        required=False, )

    malfunction_natural = fields.Selection(
        string='Malfunction Natural',
        selection=[('natural_disaster', 'Natural Disaster'),
                   ('misuse', 'Misuse'), ],default='misuse',
        required=False, )
    reason = fields.Text(
        string="Reason",
        required=False)
    vehicle= fields.Many2one(
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
    discreption_ids = fields.One2many(
        comodel_name='request.discreption',
        inverse_name='request_id',
        string='Discreption',
        required=True)
    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'),
                   ('confirmed', 'Confirmed'), ('inspection', 'Inspection'), ('cancel', 'Cancel')],default='draft',
        required=False, )

    inspection_count = fields.Integer(
        string="Inspection Count",
        compute="_compute_inspection_count",
        store=False
    )
    company_id = fields.Many2one('res.company', string='Company', change_default=True,
                                 default=lambda self: self.env.company)

    @api.depends('name')  # Depends on the name because inspections are created based on the request
    def _compute_inspection_count(self):
        for rec in self:
            rec.inspection_count = self.env['inspection.inspection'].search_count([('request_id', '=', rec.id)])

    def action_open_inspections(self):
        """
        Open related inspections.
        """
        self.ensure_one()
        return {
            'name': 'Inspections',
            'type': 'ir.actions.act_window',
            'res_model': 'inspection.inspection',
            'view_mode': 'tree,form',
            'domain': [('request_id', '=', self.id)],
            'context': {'default_vehicle': self.vehicle.id},
        }


    def action_confirm(self):
        for rec in self:
            rec.state='confirmed'

    def action_cancel(self):
        for rec in self:
            rec.state='cancel'

    def action_create_inspection(self):
        for rec in self:
            if rec.discreption_ids:
                inspection_vals = {
                    'vehicle': rec.vehicle.id,
                    'request_id': rec.id,
                    'kilometer': rec.kilometer,
                    'inspection_ids': [(0, 0, {
                        'name': line.name,
                        'received_faults': line.discreption
                    }) for line in rec.discreption_ids],
                }
                self.env['inspection.inspection'].create(inspection_vals)





    def reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'



    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            seq = self.env['ir.sequence'].next_by_code('request.request') or '/'
            vals['name'] = seq
        return super(CarRequestForMaintenance, self).create(vals)




class RequestDiscreption(models.Model):
    _name = 'request.discreption'
    _description = 'RequestDiscreption'

    name = fields.Char(
        string='Name',readonly=True,
        required=False)
    discreption = fields.Text(
        string='Discreption',
        required=True)
    request_id = fields.Many2one(
        comodel_name='request.request',
        string='request',
        required=False)
    company_id = fields.Many2one('res.company', string='Company', change_default=True,
                                 default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        if 'request_id' in vals:
            request_id = vals['request_id']
            existing_count = self.search_count([('request_id', '=', request_id)])
            vals['name'] = f"Desc-{existing_count + 1}"
        return super(RequestDiscreption, self).create(vals)

