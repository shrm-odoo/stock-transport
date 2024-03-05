from odoo import fields, models, api

class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    dock_id = fields.Many2one("stock.dock", string="Dock")
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle")
    vehicle_category_id = fields.Many2one("fleet.vehicle.model.category", string="Vehicle Category", related="vehicle_id.category_id", store=True)
    weight = fields.Float(string="Weight", compute="_compute_weight", readonly=True)
    weight_total = fields.Float(string="Weight", compute="_compute_weight", store=True)
    volume = fields.Float(string="Volume", compute="_compute_volume", readonly=True)
    volume_total = fields.Float(string="Volume", compute="_compute_volume", store=True)
    transfer_count = fields.Float(string="Transfers", compute="_compute_transfer_count", store=True)
    lines_count = fields.Float(string="Lines", compute="_compute_lines", store=True)

    @api.depends('vehicle_category_id', 'move_line_ids.product_id.weight', 'move_line_ids.quantity')
    def _compute_weight(self):
        for batch in self:
            counted_weight = sum(transfers.product_id.weight * transfers.quantity for transfers in batch.move_line_ids if transfers.product_id and transfers.product_id.weight)
            batch.weight_total = counted_weight
            max_weight = batch.vehicle_category_id.max_weight
            if max_weight == 0.0:
                batch.weight = 0.0  # Set weight to 0 if max weight is 0
            else:
                batch.weight = round(100.0 * counted_weight / max_weight)

    @api.depends('vehicle_category_id', 'move_line_ids.product_id.volume', 'move_line_ids.quantity')
    def _compute_volume(self):
        for batch in self:
            counted_volume = sum(transfers.product_id.volume * transfers.quantity for transfers in batch.move_line_ids if transfers.product_id and transfers.product_id.volume)
            batch.volume_total = counted_volume
            max_volume = batch.vehicle_category_id.max_volume
            if max_volume == 0.0:
                batch.volume = 0.0  # Set volume to 0 if max volume is 0
            else:
                batch.volume = round(100.0 * counted_volume / max_volume)

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = "%s: %s kg, %s m3" % (record.name, record.weight, record.volume)

    @api.depends('picking_ids')
    def _compute_transfer_count(self):
        for record in self:
            record.transfer_count = len(record.picking_ids)
    
    @api.depends('move_line_ids')
    def _compute_lines(self):
        for record in self:
            record.lines_count = len(record.move_line_ids)
