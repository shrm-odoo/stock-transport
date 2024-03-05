from odoo import fields, models, api

class StockPicking(models.Model):
    _inherit = "stock.picking"

    volume = fields.Float(string="Volume", compute="_compute_volume")

    @api.depends('move_ids.product_id.volume', 'move_ids.quantity')
    def _compute_volume(self):
        for record in self:
            counted_volume = sum(transfers.product_id.product_tmpl_id.volume * transfers.quantity for transfers in record.move_ids if transfers.product_id and transfers.product_id.product_tmpl_id.volume)
            record.volume = counted_volume
