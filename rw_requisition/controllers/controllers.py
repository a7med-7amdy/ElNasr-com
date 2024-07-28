# -*- coding: utf-8 -*-
# from odoo import http


# class RwRequisition(http.Controller):
#     @http.route('/rw_requisition/rw_requisition', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rw_requisition/rw_requisition/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rw_requisition.listing', {
#             'root': '/rw_requisition/rw_requisition',
#             'objects': http.request.env['rw_requisition.rw_requisition'].search([]),
#         })

#     @http.route('/rw_requisition/rw_requisition/objects/<model("rw_requisition.rw_requisition"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rw_requisition.object', {
#             'object': obj
#         })

