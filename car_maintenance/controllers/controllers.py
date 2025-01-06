# -*- coding: utf-8 -*-
# from odoo import http


# class CarMaintanance(http.Controller):
#     @http.route('/car_maintenance/car_maintenance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/car_maintenance/car_maintenance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('car_maintenance.listing', {
#             'root': '/car_maintenance/car_maintenance',
#             'objects': http.request.env['car_maintenance.car_maintenance'].search([]),
#         })

#     @http.route('/car_maintenance/car_maintenance/objects/<model("car_maintenance.car_maintenance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('car_maintenance.object', {
#             'object': obj
#         })

