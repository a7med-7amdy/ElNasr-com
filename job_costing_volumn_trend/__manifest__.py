# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name': 'Job Costing / Contracting Volumn Trends Report',
    'currency': 'EUR',
    'license': 'Other proprietary',
    'price': 19.0,
    'summary': """Trends analysis report for Job Costing and Contracting Sheets.""",
    'description': """
This module adds Reporting for Job Costing management
job cost sheet
Odoo Job Costing And Job Cost Sheet (Contracting)
Odoo job cost sheet
job cost sheet odoo
contracting odoo
odoo construction
job costing (Contracting)
odoo job costing (Contracting)
odoo job costing Contracting
job order odoo
work order odoo
job Contracting
job costing
job cost Contracting
odoo Contracting
Contracting odoo job
Jobs
Jobs/Configuration
Jobs/Configuration/Job Types
Jobs/Configuration/Stages
Jobs/Job Costs
Jobs/Job Costs/Job Cost Sheets
Jobs/Job Orders
Jobs/Job Orders/Job Notes
Jobs/Job Orders/Job Orders
Jobs/Job Orders/Project Issues
BOQ
Job Costing
Notes
Project Report
Task Report
Jobs/Materials / BOQ 
Jobs/Materials / BOQ /Material Requisitions/ BOQ
Jobs/Materials / BOQ /Materials
Jobs/Projects
Jobs/Projects/Project Budgets
Jobs/Projects/Project Notes
Jobs/Projects/Projects
Jobs/Sub Contractors 
Jobs/Sub Contractors /Sub Contractors
material requision odoo
Contracting
job Contracting
job sheet
job cost Contracting
job cost plan
costing
cost Contracting
subcontracting
Email: contact@probuse.com for more details.
This module provide Construction Management Related Activity.
Construction
Construction Projects
Budgets
Notes
Materials
Material Request For Job Orders
Add Materials
Job Orders
Create Job Orders
Job Order Related Notes
Issues Related Project
Vendors
Vendors / Contractors
Construction Management
Construction Activity
Construction Jobs
Job Order Construction
Job Orders Issues
Job Order Notes
Construction Notes
Job Order Reports
Construction Reports
Job Order Note
Construction app
Construction 
Construction Management
Notes
Project Report
Task Report
Construction Project - Project Manager
real estate property
propery management
bill of material
Material Planning On Job Order
Bill of Quantity On Job Order
Bill of Quantity construction
job costing
job cost sheet
cost sheet
project cost sheet
project planning
project sheet cost
job costing plan
Construction cost sheet
Construction job cost sheet
Construction jobs
Construction job sheet
Construction material
Construction labour
Construction overheads
Construction sheet plan
costing
workshop
job workshop
workshop
jobs
cost centers
Construction purchase order
Construction activities
Basic Job Costing
Job Costing Example
job order costing
job order
job orders
Tracking Labor
Tracking Material
Tracking Overhead
overhead
material plan
job overhead
job labor
Job Cost Sheet
Example For Larger Job
Features of Job Costing
Enabling Job Costing
Creating Cost Centres for Job Costing
project job cost
project job costing
project job contracting
project job contract
job contract
jobs contract
construction
Construction app
Construction odoo

    """,
    'author': "Probuse Consulting Service Pvt. Ltd.",
    'website': "http://www.probuse.com",
    'support': 'contact@probuse.com',
    'images': ['static/description/images.jpg'],
    'live_test_url': 'https://probuseappdemo.com/probuse_apps/job_costing_volumn_trend/659',#'https://youtu.be/JcWQRC3LtW0',
    'version': '5.1.4',
    'category' : 'Operations/Project',
    'depends': [
        'odoo_job_costing_management',
        'material_requisition_cost_sheet',
    ],
    'data':[
        'security/ir.model.access.csv',
        'report/job_costing_trends.xml',
        'views/view.xml',
    ],
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
