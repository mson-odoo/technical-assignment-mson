# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class FleetVehicleModelCategory(models.Model):
    _inherit = 'fleet.vehicle.model.category'
    
    max_weight = fields.Float(string="Max Weight (Kg)")
    max_volume = fields.Float(string="Max Volume (m\N{SUPERSCRIPT THREE})")
    
    _sql_constraints = [
        ('check_max_weight','CHECK(max_weight > 0)','Weight must be greater than 0'),
        ('check_max_volume','CHECK(max_volume > 0)','Volume must be greater than 0')
    ]
    
    @api.depends('max_weight', 'max_volume')
    def _compute_display_name(self):
        for category in self:
            category.display_name = f"{category.name} ({category.max_weight}kg, {category.max_volume}m\N{SUPERSCRIPT THREE})"