from odoo import fields, models

class StockDock(models.Model):
    _name = "stock.dock"
    _description = "Dock for stock"

    name = fields.Char(string="Name")
