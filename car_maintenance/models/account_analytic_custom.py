from odoo import api, fields, models 

class HrTimesheetSheetCustom(models.Model):
    _name = 'account.analytic.custom'
    _description = 'HrTimesheetSheet'



    name = fields.Char(
        string='Name',
        required=False)

    car_repair_request_id = fields.Many2one(
        'car.order',
        string="Repair Request"
    )
    company_id = fields.Many2one('res.company', string='Company', change_default=True,
                                 default=lambda self: self.env.company)
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
        required=False)
    start_date = fields.Datetime(
        string='Start Date',
        required=False)
    end_date = fields.Datetime(
        string='End Date',
        required=False)
    time_difference = fields.Float(
        string='Hours',
        compute='_compute_time_difference',
        store=True,
        help="Difference in time (hours) between Start Date and End Date")
    hourly_cost = fields.Monetary(
        string='Hour Cost',related='employee_id.hourly_cost',readonly=False,
        required=False)
    total_cost = fields.Monetary(
        string='Total', compute='_compute_total_cost', store=True,
        required=False)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    order_line = fields.Many2one(
        comodel_name='order.line',
        string='Order',
        domain="[('order_id', '=', car_repair_request_id)]",
        required=False,
    )
    @api.depends('hourly_cost','time_difference')
    def _compute_total_cost(self):
        for rec in self:
            if rec.hourly_cost or rec.time_difference:
                rec.total_cost = rec.time_difference * rec.hourly_cost
            else:
                rec.total_cost = 0

    @api.depends('start_date', 'end_date')
    def _compute_time_difference(self):
        for record in self:
            if record.start_date and record.end_date:
                # Extract only the time part from datetime fields
                start_time = record.start_date.time()
                end_time = record.end_date.time()

                # Convert time to seconds for difference calculation
                start_seconds = (start_time.hour * 3600) + (start_time.minute * 60) + start_time.second
                end_seconds = (end_time.hour * 3600) + (end_time.minute * 60) + end_time.second

                # Calculate the difference in hours
                diff_seconds =  end_seconds - start_seconds
                record.time_difference = diff_seconds / 3600.0
            else:
                record.time_difference = 0.0