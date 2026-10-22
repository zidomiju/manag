# from odoo import http


# class LikaLedger(http.Controller):
#     @http.route('/lika_ledger/lika_ledger', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lika_ledger/lika_ledger/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('lika_ledger.listing', {
#             'root': '/lika_ledger/lika_ledger',
#             'objects': http.request.env['lika_ledger.lika_ledger'].search([]),
#         })

#     @http.route('/lika_ledger/lika_ledger/objects/<model("lika_ledger.lika_ledger"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lika_ledger.object', {
#             'object': obj
#         })

