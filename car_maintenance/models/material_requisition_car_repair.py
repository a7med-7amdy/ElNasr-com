from odoo import api, fields, models 



class MaterialRequisitionCarRepair(models.Model):
    _name = "material.requisition.car.repair"
    _description = 'material.requisition.car.repair'

    requisition_id = fields.Many2one(
        'car.order',
        string='Requisitions',
    )

    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
        domain="['|',('spare_parts', '=', True), ('row_material', '=', True)]"
    )

    qty = fields.Float(
        string='Quantity',
        default=1,
        required=True,
    )
    description = fields.Char(
        string='Description',
        required=True,
    )
    requisition_type = fields.Selection(
        selection=[
                    ('internal','Internal Picking'),
                    ('purchase','Purchase Order'),
        ],
        string='Requisition Action',
        default='purchase',
        required=True,
    )
    order_line = fields.Many2one(
        comodel_name='order.line',
        string='Order',
        domain="[('order_id', '=', requisition_id)]",
        required=False,
    )

    product_on_hand_qty = fields.Float(
        string='On Hand',related='product_id.qty_available',
        required=False)
    avg_cost = fields.Float(
        string="Cost",
        required=False
    )
    company_currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        string='Company Currency',
        store=True
    )

    company_id = fields.Many2one('res.company', string='Company', change_default=True,
                                 default=lambda self: self.env.company)
    product_uom_qty = fields.Integer(
        'Quantity',
        default=1.0
    )
    product_uom = fields.Many2one(
        'uom.uom',  # product.uom
        'Unit',default=lambda self: self.env.ref('uom.product_uom_unit', raise_if_not_found=False)
    )

    required = fields.Float(
        string='Required Quantity',
        compute='_compute_required',
        store=True,
        help="The absolute value of the difference between requested and available quantities."
    )
    total_cost = fields.Monetary(
        string='Total',
        compute='_compute_total_cost',
        currency_field='company_currency_id',
        store=True,
        help='Total cost calculated as Required Quantity * Average Cost'
    )


    @api.depends('product_uom_qty', 'product_on_hand_qty')
    def _compute_required(self):
        for record in self:
            record.required = abs(record.product_uom_qty - record.product_on_hand_qty)

    @api.depends('required', 'avg_cost')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.required * record.avg_cost if record.avg_cost else 0.0

    @api.onchange('product_id')
    def onchange_product_id(self):
        result = {}
        if not self.product_id:
            return result
        self.product_uom = self.product_id.uom_po_id or self.product_id.uom_id
        self.description = self.product_id.name



