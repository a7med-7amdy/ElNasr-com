# -*- coding: utf-8 -*-
{
    'name': "car_maintenance",
    'summary': "This Addon For management of repair and maintenance ",
    'description': """This Addon For management of repair and maintenance """,
    'author': "ُEngineer / Mohamed Sobhy",
    'website': "hamdy company",
    'category': 'Cars',
    'version': '1.2',
    'depends': ['base','fleet','hr','hr_hourly_cost','purchase','product',],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/car_inspection.xml',
        'views/car_order.xml',
        'views/fleet.xml',
        'views/stock.xml',
        'views/templates.xml',
        'views/base.xml',
        'views/tire.xml',
        'views/oils.xml',
        'views/tools.xml',
        'views/product.xml',
        'views/oil_type.xml',
        'views/change_type.xml',
        'views/filter_type.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',

    ],
    'installable': True,
    'application': True,
}
