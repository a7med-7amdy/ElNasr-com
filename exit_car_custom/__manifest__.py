# -*- coding: utf-8 -*-
{
    'name': "Cars",
    'summary': "Cars",
    'description': """Long description of module's purpose """,
    'author': "Rwad",
    'category': 'Contracts',
    'version': '17.0.1.8',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'sequence': 7,
    'depends': ['base','car_maintenance'],
    'data': [
        'security/ir.model.access.csv',
        'views/driver.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

