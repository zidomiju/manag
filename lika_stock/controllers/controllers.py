# from odoo import http


# class LikaStock(http.Controller):
#     @http.route('/lika_stock/lika_stock', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lika_stock/lika_stock/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('lika_stock.listing', {
#             'root': '/lika_stock/lika_stock',
#             'objects': http.request.env['lika_stock.lika_stock'].search([]),
#         })

#     @http.route('/lika_stock/lika_stock/objects/<model("lika_stock.lika_stock"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lika_stock.object', {
#             'object': obj
#         })

