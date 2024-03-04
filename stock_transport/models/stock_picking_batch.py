from odoo import fields, models, api

class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    dock_id = fields.Many2one("stock.dock", string="Dock")
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle")
    vehicle_category_id = fields.Many2one("fleet.vehicle.model.category", string="Vehicle Category")
    weight = fields.Float(string="Weight", compute="_compute_weight", readonly=True, store=True)
    volume = fields.Float(string="Volume", compute="_compute_volume", readonly=True, store=True)

    @api.depends('vehicle_category_id', 'move_line_ids')
    def _compute_weight(self):
        for batch in self:
            counted_weight = sum(transfers.product_id.product_tmpl_id.weight * transfers.quantity for transfers in batch.move_line_ids if transfers.product_id and transfers.product_id.product_tmpl_id.weight)
            max_weight = batch.vehicle_category_id.max_weight or 1.0  # Default max weight to 1.0 if not set to avoid division by zero
            batch.weight = round(100.0 * counted_weight / max_weight)

    @api.depends('vehicle_category_id', 'move_line_ids')
    def _compute_volume(self):
        for batch in self:
            counted_volume = sum(transfers.product_id.product_tmpl_id.volume * transfers.quantity for transfers in batch.move_line_ids if transfers.product_id and transfers.product_id.product_tmpl_id.volume)
            max_volume = batch.vehicle_category_id.max_volume or 1.0  # Default max volume to 1.0 if not set to avoid division by zero
            batch.volume = round(100.0 * counted_volume / max_volume)
