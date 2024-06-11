# -*- coding: utf-8 -*-
# from odoo import http


# class RwMrp(http.Controller):
#     @http.route('/rw_mrp/rw_mrp', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rw_mrp/rw_mrp/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rw_mrp.listing', {
#             'root': '/rw_mrp/rw_mrp',
#             'objects': http.request.env['rw_mrp.rw_mrp'].search([]),
#         })

#     @http.route('/rw_mrp/rw_mrp/objects/<model("rw_mrp.rw_mrp"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rw_mrp.object', {
#             'object': obj
#         })

