# -*- coding: utf-8 -*-
# from odoo import http


# class GestionConges(http.Controller):
#     @http.route('/gestion_conges/gestion_conges', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_conges/gestion_conges/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_conges.listing', {
#             'root': '/gestion_conges/gestion_conges',
#             'objects': http.request.env['gestion_conges.gestion_conges'].search([]),
#         })

#     @http.route('/gestion_conges/gestion_conges/objects/<model("gestion_conges.gestion_conges"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_conges.object', {
#             'object': obj
#         })

