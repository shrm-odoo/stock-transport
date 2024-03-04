{
    'name' : "Transport Management System",
    'version' : "1.0",
    'category': "stock transport",
    'summary' : "The Transport Management System module",
    'depends': ['stock_picking_batch','fleet'],
    'installable' : True,
    'application' : True,
    'license' : "LGPL-3",
    'data' : [
        'security/ir.model.access.csv',
        'views/fleet_vehicle_category_views.xml',
        'views/stock_picking_batch_views.xml'
    ]
}
