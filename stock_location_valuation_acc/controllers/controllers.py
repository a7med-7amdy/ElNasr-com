# -*- coding: utf-8 -*-
# from odoo import http


# class StockLocationValuationAcc(http.Controller):
#     @http.route('/stock_location_valuation_acc/stock_location_valuation_acc', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_location_valuation_acc/stock_location_valuation_acc/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_location_valuation_acc.listing', {
#             'root': '/stock_location_valuation_acc/stock_location_valuation_acc',
#             'objects': http.request.env['stock_location_valuation_acc.stock_location_valuation_acc'].search([]),
#         })

#     @http.route('/stock_location_valuation_acc/stock_location_valuation_acc/objects/<model("stock_location_valuation_acc.stock_location_valuation_acc"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_location_valuation_acc.object', {
#             'object': obj
#         })

