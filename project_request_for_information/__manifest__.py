# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.
{
    'name': 'Request for Information (Construction and Contracting Business)',
    'currency': 'EUR',
    'price': 39.0,
    'depends': [
                'portal',
                'sales_team',
                'crm',
                'account',
                'survey',
                'odoo_job_costing_management',
                'website',
                'sale_timesheet'
                ],
    'license': 'Other proprietary',
    'summary': """Manage request for information for your contruction and contracting business projects.""",
    'author': "Probuse Consulting Service Pvt. Ltd.",
    'website': "http://www.probuse.com",
    'support': 'contact@probuse.com',
    # 'images': ['static/description/img1.jpg'],
    'images': ['static/description/image.png'],
    # 'live_test_url': 'https://youtu.be/JycKugv3iZ0', #'https://youtu.be/4iEiK-D1tEg',
    'live_test_url': 'https://probuseappdemo.com/probuse_apps/project_request_for_information/126',#'https://youtu.be/lC95VfPNiyI',
    'version': '10.1.9',
    'category' : 'Services/Project',
    'data':[
        'report/request_report_view.xml',
        'datas/request_information_sequence.xml',
#        'datas/mail_template_request.xml',
        'datas/request_team_data.xml',
        'datas/request_information_stages_data.xml',
        'security/request_information_security.xml',
        'security/ir.model.access.csv',
        'views/website_mail_message_template.xml',
        'views/request_information_stages_views.xml',
        'views/request_information_view.xml',
        # 'datas/mail_template_request.xml',
        'datas/mail_template_request_new.xml',
        'views/request_information_type_view.xml',
        'views/request_information_subject_view.xml',
        'views/create_request_information_template.xml',
        'views/request_team_view.xml',
        'views/request_information_template_view.xml',
        'views/request_information_attachment.xml',
        'views/successfull.xml',
        'views/feedback.xml',
        'views/thankyou.xml',
        'report/request_information_analysis_report.xml',
        'views/res_partner_view.xml',
        'views/project_view.xml',
        'views/project_task_view.xml',
        'views/menu.xml',
        'views/survey_view.xml',
        'views/job_costing_view.xml',
    ],
    'description': """
request for information
request information
request for quote
project request
project management
customer project
claim issue
claim management
issue management
helpdesk
support
ticket
support ticket
helpdesk support
Project Request For Information
Request Information
Job Cost Request Information
Print Request For Information
Attachment on website RFI
Message on website RFI
Add attchment
Add message
Send Message RFI
Multiple attachments RFI
RFI Portal
Request For Information
This module allow you manage your Request for Information, Timesheets.
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
Display Project Requests (qweb)
Display Request Infomation (qweb)
Request For Information Genarate (qweb)
Request For Information Type (form)
Request For Information Type (search)
Request For Information Type (tree)
Request For Information form (form)
Request For Information kanban (kanban)
Request For Information search (search)
Request For Information tree (tree)
Request Information Calendar (calendar)
Request Information Team (form)
Request Information Team (tree)
Request Information feedback (qweb)
Stage - Search (search)
Success Page (qweb)
Success Ticket (qweb)
Support Invalid (qweb)
Thanks (qweb)
message_thread_request_information (qweb)
request.information.form.simple (form)
request.information.graph (graph)
request.information.pivot (pivot)
request.information.report.pivot (pivot)
request.information.stage.config.form (form)
request.information.subject.form (form)
request.information.subject.search (search)
request.information.subject.tree (tree)
request_information.stage.config.tree (tree)
request_information_report (qweb)
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
    """,
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
