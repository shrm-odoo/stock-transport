from odoo import fields, models, api

class FleetVehicleModelCategory(models.Model):
    _inherit = 'fleet.vehicle.model.category'

    max_weight = fields.Float(string = "Max Weight(kg)")
    max_volume = fields.Float(string = "Max Volume(m3)")

    @api.depends('name')
    def _compute_display_name(self):
        for category in self:
            category.display_name = "%s (%s kg, %s m3)" % (category.name, category.max_weight, category.max_volume)
