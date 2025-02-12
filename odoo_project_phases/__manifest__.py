# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name': 'Project by Phases',
    'version': '6.1.9',
    'price': 12.0,
    'currency': 'EUR',
    'depends': [
                'project',
                ],
    'license': 'Other proprietary',
    'category': 'Services/Project',
    'summary': 'Allow you to manage your project and task by phases',
    'description': """
Odoo Project Phases
Odoo Project Phases
project phase
task phase
scrum project
project scrum
project phases
task phases
phase management
phase
odoo phase
project task
project app
task app
            """,
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'website': 'www.probuse.com',
    'support': 'contact@probuse.com',
    'images': ['static/description/img.jpg'],
    # 'live_test_url': 'https://youtu.be/HmvGPM8Ddkg',
    'live_test_url': 'https://probuseappdemo.com/probuse_apps/odoo_project_phases/983',#'https://youtu.be/esHrEhySiaE',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/project_phase_view.xml',
        'views/project_view.xml',
        'views/task_view.xml',
        'report/project_report_view.xml',
             ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
