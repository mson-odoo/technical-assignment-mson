# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Stock Transport',
    'data': [
        'security/ir.model.access.csv',
        'views/fleet_dock_station_views.xml',
        'views/fleet_vehicle_model_category_views.xml',
        'views/stock_picking_batch_views.xml', 
        'views/stock_picking_views.xml',   
    ],
    'depends':[
        'fleet',
        'stock_picking_batch',
    ],
    'installable': True,
    'application': True,
}