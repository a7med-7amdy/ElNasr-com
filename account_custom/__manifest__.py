# -*- coding: utf-8 -*-
{
    'name': "account_custom",
    'summary': "SAccount Custom",
    'description': """account custom for stock""",
    'author': "Engineer / Mohamed Sobhy",
    'website': "",
    'category': 'Accounting/Accounting',
    'version': '0.1',
    'depends': ['base','stock'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/stock.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

