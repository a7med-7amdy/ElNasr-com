# -*- coding: utf-8 -*-
# from odoo import http


# class ContractCustom(http.Controller):
#     @http.route('/contract_custom/contract_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/contract_custom/contract_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('contract_custom.listing', {
#             'root': '/contract_custom/contract_custom',
#             'objects': http.request.env['contract_custom.contract_custom'].search([]),
#         })

#     @http.route('/contract_custom/contract_custom/objects/<model("contract_custom.contract_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('contract_custom.object', {
#             'object': obj
#         })

