# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
# from odoo.exceptions import Warning , UserError
from odoo.exceptions import UserError

class JobCostSheetUpdateWizard(models.TransientModel):
    _name = "jobcostsheet.update.wizard"
    _description = 'JobCost Sheet Update Wizard'
    
    costsheet_type = fields.Selection(
        [('create_costsheet','Create Job Cost Sheet'),
         ('update_costsheet','Update Job Cost Sheet')],
        string='Options',
        default='create_costsheet',
        required=True,
    )
    project_id = fields.Many2one(
        'project.project',
        string='Project',
        required=True,
        readonly=True,
    )
    job_costsheet_id = fields.Many2one(
        'job.costing',
        string='Job Cost Sheet',
        required=False,
    )
    
    # @api.multi
    def create_edit_jobcostsheet(self):
        active_id = self._context.get('active_id')
        project_task_obj = self.env['project.task'].browse(active_id)
        job_type = self.env['job.type'].search([('name','=','Material')])
        job_cost_line = self.env['job.cost.line']
        job_costsheet = self.env['job.costing']
        flag1 = False
        if self.costsheet_type == 'create_costsheet':
            for material in project_task_obj.material_plan_ids:
                if not material.is_material_created:
                    flag1 = False
                    break
                else:
                    flag1 = True
            if flag1:
                # raise UserError(_('No Material Line Found.'))
                raise UserError(_('No Material Line Found.'))
            if not project_task_obj.partner_id.id:
                # raise UserError(_('Job order not on Customer.'))
                raise UserError(_('Job order not on Customer.'))
            costsheet_vals = {
                              'name':'New',
                              'project_id': project_task_obj.project_id.id,
                              'analytic_id': project_task_obj.project_id.analytic_account_id.id,
                              'partner_id': project_task_obj.partner_id.id,
                              'task_id': project_task_obj.id,
                              'state': 'draft',
                              }
            costsheet = job_costsheet.create(costsheet_vals)
            for material in project_task_obj.material_plan_ids:
                if not material.is_material_created:
                    material_line_vals= {
                                            'date': fields.date.today(),
                                            'job_type_id': job_type.id,
                                            'job_type' : 'material',
                                            'product_id': material.product_id.id,
                                            'product_qty': material.product_uom_qty,
                                            'uom_id': material.product_uom.id,
                                            'cost_price': material.product_id.standard_price,
                                            'description': material.product_id.name,
                                            'direct_id':costsheet.id,
                                            'custom_material_id': material.id
                                        }
                    job_costing_material_line = job_cost_line.create(material_line_vals)
                    material.custom_material_job_id = job_costing_material_line.id
                    material.is_material_created = True
        else:
            if project_task_obj.material_plan_ids:
                if self.job_costsheet_id:
                    for material in project_task_obj.material_plan_ids:
                        flag = False
                        if not material.is_material_created:
                            flag = False
                            break
                        else:
                            flag = True
                    if flag:
                        # raise UserError(_('No Material Line Found.'))
                        raise UserError(_('No Material Line Found.'))
                    for material in project_task_obj.material_plan_ids:
                        if not material.is_material_created:
                            vals= {
                                'date': fields.date.today(),
                                'job_type_id': job_type.id,
                                'job_type' : 'material',
                                'product_id': material.product_id.id,
                                'product_qty': material.product_uom_qty,
                                'uom_id': material.product_uom.id,
                                'cost_price': material.product_id.standard_price,
                                'description': material.product_id.name,
                                'direct_id':self.job_costsheet_id.id,
                                'custom_material_id': material.id
                            }
                            job_costing_material_line = job_cost_line.create(vals)
                            material.custom_material_job_id = job_costing_material_line.id
                            material.is_material_created = True
