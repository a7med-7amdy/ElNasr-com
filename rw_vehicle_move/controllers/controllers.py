# -*- coding: utf-8 -*-
# from odoo import http


# class RwVehicleMove(http.Controller):
#     @http.route('/rw_vehicle_move/rw_vehicle_move', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rw_vehicle_move/rw_vehicle_move/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rw_vehicle_move.listing', {
#             'root': '/rw_vehicle_move/rw_vehicle_move',
#             'objects': http.request.env['rw_vehicle_move.rw_vehicle_move'].search([]),
#         })

#     @http.route('/rw_vehicle_move/rw_vehicle_move/objects/<model("rw_vehicle_move.rw_vehicle_move"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rw_vehicle_move.object', {
#             'object': obj
#         })

