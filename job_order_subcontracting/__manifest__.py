# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.
{
    'name': 'Subcontracting in Job Order / Construction / Contracting Industry',
    'version': '11.1.10',
    'currency': 'EUR',
    'price': 49.00,
    'license': 'Other proprietary',
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'website': 'https://www.probuse.com',
    'depends': [
                'portal',
                'website',
                'odoo_job_costing_management',
                ],
    'support': 'contact@probuse.com',
    'images': ['static/description/img1.jpeg'],
    'live_test_url': 'https://probuseappdemo.com/probuse_apps/job_order_subcontracting/681',#'https://youtu.be/m9fL5csLjAg', #'https://youtu.be/yMq7i_j3Zsw',
    'category' : 'Services/Project',
    'data': [
        'security/ir.model.access.csv',
        'wizard/sub_contractor_wizard.xml',
        'wizard/purchase_order_wizard.xml',
        'views/project_task_view.xml',
        'views/purchase_order_view.xml',
        # 'views/subcontractor_joborder_template.xml',
        'views/subcontractor_joborder_templates.xml',
        # 'data/subcontractor_mail_template.xml',
        'data/subcontractor_mail_template_new.xml',
    ],
    'summary': 'This app allow you to create subcontractor job order in system and allow subcontractor to view jobs in portal.',
    'description': """Job order Subcontracting.
This module allow create sub contractor and its purchase order
Subcontracting Job Orders
Subcontracting Details,
Subcontracting Job Orders My Account
Subcontracting
subcontractor
subcontractor job
Subcontracting job
job Subcontracting
job Subcontract
job Subcontractor
job costing
costing
cost sheet
subcontract
construction subcontract
construction subcontracting
construction subcontractor
Create Subcontracting Job Orders
Create Purchase Order on Subcontracting Job Orders
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

This module provide feature to manage Construction Management activity.
Menus:
Construction
Construction/Configuration
Construction/Configuration /Stages
Construction/Construction
Construction/Construction/Budgets
Construction/Construction/Notes
Construction/Construction/Projects
Construction/Job Orders
Construction/Job Orders /Issues
Construction/Job Orders /Job Orders
Construction/Job Orders /Notes
Construction/Materials / BOQ
Construction/Materials /Material Requisitions / BOQ
Construction/Materials /Materials
Construction/Vendors
Construction/Vendors /Contractors
Defined Reports
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
Job costing is a method of costing applied in industries where production is measured in terms of completed jobs. Industries where job costing is generally applied are Printing Press. Automobile Garage, Repair workshops, Ship Building, Foundry and other similar manufacturing units which manufacture to customers� specific requirements.

Job costing is a method of costing whereby cost is compiled for a job or work order. The production is against customer�s orders and not for stock. The cost is not related to the unit of production but is a cost for the job, e. g printing of 5000 ledger sheets, repairs of 50 equipment�s, instead of printing one sheet or repair of one equipment.

The elements of cost comprising Prime Cost viz. direct materials, direct labour and direct expenses are charged directly to the jobs concerned, the overhead charged to a job is an apportioned portion of the departmental overhead.
Advantages of Job Order Costing

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
odoo Construction
Create Project/Contract -> Create Job Orders -> Create Multiple Job Cost Sheets under Same Project -> Plan your materials, labour and overhead for each Jobs -> View of Planned and Actual Amount/Qty by each Cost Sheet Lines (Material, Labour and Overheads) -> Allow your purchase, accounting and HR department to select cost center (cost sheet) and cost center line (cost sheet line) to encode for expenses and labour works. -> Create Job Order Issues -> Create Material Requision Request -> Prepare Notes/ToDo lists for Projects and Jobs. ->

    
    """,
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
