# -*- coding: utf-8 -*-
{
    'name': "car_maintenance",
    'summary': "This Addon For management of repair and maintenance ",
    'description': """This Addon For management of repair and maintenance """,
    'author': "ُEngineer / Mohamed Sobhy",
    'website': "hamdy company",
    'category': 'Cars',
    'version': '1.2',
    'depends': ['base','rw_vehicle_move'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/car_inspection.xml',
        'views/car_order.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',

    ],
    'installable': True,
    'application': True,
}
