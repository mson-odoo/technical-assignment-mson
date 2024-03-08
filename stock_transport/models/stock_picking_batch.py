# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare


class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    dock_id = fields.Many2one(comodel_name="fleet.dock.station", string="Dock")
    vehicle_id = fields.Many2one(comodel_name='fleet.vehicle', string="Vehicle")
    category_id = fields.Many2one(comodel_name='fleet.vehicle.model.category', string='Vehical Category')
    weight = fields.Float(string="Weight", compute="_compute_measurements", store=True)
    weight_percentage = fields.Float(string="Weight", compute="_compute_percentage")
    volume = fields.Float(string="Volume", compute="_compute_measurements", store=True)
    volume_percentage = fields.Float(string="Volume", compute="_compute_percentagets")
    transfers = fields.Integer(string="Transfer", compute="_compute_transfers", store=True)
    lines = fields.Integer(string="Lines", compute="_compute_lines", store=True)
    
    @api.onchange('vehicle_id')
    def _onchange_vehical_id(self):
        for batch in self:
            batch.category_id = batch.vehicle_id.category_idreal_estate
    
    @api.depends("picking_ids.weight", "picking_ids.volume", "category_id")
    def _compute_measurements(self):
        for batch in self:
            if(batch.category_id):
                batch.weight = sum(self.picking_ids.mapped("weight"))
                batch.volume = sum(self.picking_ids.mapped("volume"))
            
    @api.depends("picking_ids.weight", "picking_ids.volume", "category_id")
    def _compute_percentage(self):
        for batch in self:
            if(batch.category_id):
                batch.weight_percentage = round((batch.weight / batch.category_id.max_weight) * 100, 2)
                batch.volume_percentage = round((batch.volume / batch.category_id.max_volume) * 100, 2)
            else:
                batch.weight_percentage = 0
                batch.volume_percentage = 0
    
                
    @api.depends("picking_ids")
    def _compute_transfers(self):
        for batch in self:
            batch.transfers = len(self.mapped('picking_ids'))
    
    @api.depends("move_ids")
    def _compute_lines(self):
        for batch in self:
            batch.lines = len(batch.mapped('move_ids'))
    
    @api.depends('weight', 'volume')
    def _compute_display_name(self):
        for batch in self:
            batch.display_name = f"{batch.name}: {batch.weight}kg, {batch.volume}m\N{SUPERSCRIPT THREE} {batch.vehicle_id.driver_id.name}"
            
            
    @api.constrains('weight', 'category_id.max_weight)')
    def _check_weight(self):
        for batch in self:
            if (float_compare(batch.weight, batch.category_id.max_weight, 2) == 1):
                raise ValidationError('The weight must be lower than vehical\'s max weight!!')
                
    @api.constrains('volume', 'category_id.max_volume)')
    def _check_volume(self):
        for batch in self:
            if (float_compare(batch.volume, batch.category_id.max_volume, 2) == 1):
                raise ValidationError('The volume must be lower than vehical\'s max volume!!')