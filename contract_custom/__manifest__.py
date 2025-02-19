# -*- coding: utf-8 -*-
{
    'name': "Transfer Contracts",
    'summary': "Custom To Make New Module For Contract",
    'description': """Custom To Make New Module For Contract""",
    'author': "Rwad",
    'website': "https://www.yourcompany.com",
    'category': 'Contracts',
    'version': '17.0.1.8',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'sequence': 7,
    'depends': ['base', 'contacts', 'sale_management', 'purchase_auto_lot_selection', 'stock', 'rw_vehicle_move',
                'account'],
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/views.xml',
        'views/indirect_contract_views.xml',
        'views/partner.xml',
        'views/general_contract.xml',
        'views/transfer_contract.xml',
        'views/sales.xml',
        'views/vehicle.xml',
        'views/contract_update.xml',
        'views/update_contract_wizard.xml',
        'views/company.xml',
        'views/templates.xml',
        'views/ir_cron.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
