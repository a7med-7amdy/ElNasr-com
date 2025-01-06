# -*- coding: utf-8 -*-
# from odoo import http


# class ExitCarCustom(http.Controller):
#     @http.route('/exit_car_custom/exit_car_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/exit_car_custom/exit_car_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('exit_car_custom.listing', {
#             'root': '/exit_car_custom/exit_car_custom',
#             'objects': http.request.env['exit_car_custom.exit_car_custom'].search([]),
#         })

#     @http.route('/exit_car_custom/exit_car_custom/objects/<model("exit_car_custom.exit_car_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('exit_car_custom.object', {
#             'object': obj
#         })

