# -*- coding: utf-8 -*-
# from odoo import http


# class Helpecos(http.Controller):
#     @http.route('/helpecos/helpecos/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/helpecos/helpecos/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('helpecos.listing', {
#             'root': '/helpecos/helpecos',
#             'objects': http.request.env['helpecos.helpecos'].search([]),
#         })

#     @http.route('/helpecos/helpecos/objects/<model("helpecos.helpecos"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('helpecos.object', {
#             'object': obj
#         })
