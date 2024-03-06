# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    weight = fields.Float(string="Weight", compute="_compute_measurements")
    volume = fields.Float(string="Volume", compute="_compute_measurements")
    
    @api.depends("move_ids")
    def _compute_measurements(self):
        for record in self:
            weights = record.move_ids.product_id.mapped('weight')
            volumes = record.move_ids.product_id.mapped('volume')
            quantities = record.move_ids.mapped('quantity')
            total_weight = sum(weight * quantity for weight, quantity in zip(weights, quantities))
            total_volume = sum(volume * quantity for volume, quantity in zip(volumes, quantities))
            record.weight = round(total_weight, 2)
            record.volume = round(total_volume, 2)