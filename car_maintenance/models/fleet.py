from odoo import api, fields, models


class FleetVehicleCustom(models.Model):
    _inherit = 'fleet.vehicle'


    unit_number = fields.Char(
        string='Unit Number',
        required=False)
    brand = fields.Char(
        string='Brand',
        required=False)
    loading = fields.Char(
        string='Loading',
        required=False)


    tools_ids = fields.Many2many(
        comodel_name='tools.tools',
        string='Vehicles Tools')

    tools_group = fields.Char(
        string="Tools Group",
        compute="_compute_tools_group",
        store=True,
    )

    @api.model
    @api.depends('tools_ids')
    def _compute_tools_group(self):
        for rec in self:
            if rec.tools_ids:
                # Combine tool names for display
                tools_group = ', '.join([tool.name for tool in rec.tools_ids])
            else:
                tools_group = ''  # Initialize tools_group if no tools are present

            rec.tools_group = tools_group  # Set the value for tools_group
    @api.onchange('tools_ids')
    def _onchange_tools_ids(self):
        """Synchronize tools with their vehicles."""
        for tool in self.tools_ids:
            if self not in tool.vehicle_ids:
                tool.vehicle_ids = [(4, self.id)]

    def write(self, vals):
        """Override write to ensure bi-directional updates."""
        if 'tools_ids' in vals:
            tools_operations = vals.get('tools_ids', [])
            if tools_operations:
                for operation in tools_operations:
                    if len(operation) < 3:
                        continue  # Skip invalid entries

                    op_type, _, tool_ids = operation
                    if op_type == 6:  # Replace all records
                        new_tool_ids = tool_ids
                        current_tool_ids = self.tools_ids.ids

                        # Unlink vehicle from tools being removed
                        for tool in self.env['tools.tools'].browse(current_tool_ids):
                            if tool.id not in new_tool_ids:
                                tool.vehicle_ids = [(3, self.id)]

                        # Link vehicle to new tools
                        for tool in self.env['tools.tools'].browse(new_tool_ids):
                            if self.id not in tool.vehicle_ids.ids:
                                tool.vehicle_ids = [(4, self.id)]
                    elif op_type == 4:  # Add a tool
                        tool = self.env['tools.tools'].browse(tool_ids)
                        for t in tool:
                            if self.id not in t.vehicle_ids.ids:
                                t.vehicle_ids = [(4, self.id)]
                    elif op_type == 3:  # Remove a tool
                        tool = self.env['tools.tools'].browse(tool_ids)
                        for t in tool:
                            if self.id in t.vehicle_ids.ids:
                                t.vehicle_ids = [(3, self.id)]

        return super(FleetVehicleCustom, self).write(vals)


class ToolsForCars(models.Model):
    _name = 'tools.tools'
    _description = 'ToolsForCars'

    name = fields.Char(
        string='Tool Name',
        required=True)
    vehicle_ids = fields.Many2many(
        comodel_name='fleet.vehicle',
        string='Available Vehicle')


    @api.onchange('vehicle_ids')
    def _onchange_vehicle_ids(self):
        """Synchronize vehicles with their tools."""
        for vehicle in self.vehicle_ids:
            if self not in vehicle.tools_ids:
                vehicle.tools_ids = [(4, self.id)]

    def write(self, vals):
        """Override write to ensure bi-directional updates."""
        if 'vehicle_ids' in vals:
            # Get the new vehicles being added/removed
            new_vehicles = self.env['fleet.vehicle'].browse(vals['vehicle_ids'][0][2])
            current_vehicles = self.vehicle_ids

            # Remove the tool from vehicles that are removed
            for vehicle in current_vehicles - new_vehicles:
                vehicle.tools_ids = [(3, self.id)]

            # Add the tool to newly added vehicles
            for vehicle in new_vehicles - current_vehicles:
                vehicle.tools_ids = [(4, self.id)]

        return super(ToolsForCars, self).write(vals)


