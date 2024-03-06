# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    dock_id = fields.Many2one(comodel_name="fleet.dock.station", string="Dock")
    vehicle_id = fields.Many2one(comodel_name='fleet.vehicle', string="Vehicle")
    category_id = fields.Many2one(comodel_name='fleet.vehicle.model.category', string='Vehical Category')
    weight = fields.Float(string="Weight", compute="_compute_measurements", store=True)
    volume = fields.Float(string="Volume", compute="_compute_measurements", store=True)
    transfers = fields.Integer(string="Transfer", compute="_compute_transfers", store=True)
    lines = fields.Integer(string="Lines", compute="_compute_lines", store=True)
    
    @api.onchange('vehicle_id')
    def _onchange_vehical_id(self):
        for batch in self:
            batch.category_id = batch.vehicle_id.category_id
    
    @api.depends("picking_ids.weight", "picking_ids.volume", "category_id")
    def _compute_measurements(self):
        for batch in self:
            if(batch.category_id):
                total_weight = sum(self.picking_ids.mapped("weight"))
                total_volume = sum(self.picking_ids.mapped("volume"))
                batch.weight = round((total_weight / batch.category_id.max_weight) * 100, 2)
                batch.volume = round((total_volume / batch.category_id.max_volume) * 100, 2)
            else:
                batch.weight = 0
                batch.volume = 0
                
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