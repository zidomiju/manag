# from odoo import http


# class LikaSpareparts(http.Controller):
#     @http.route('/lika_spareparts/lika_spareparts', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lika_spareparts/lika_spareparts/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('lika_spareparts.listing', {
#             'root': '/lika_spareparts/lika_spareparts',
#             'objects': http.request.env['lika_spareparts.lika_spareparts'].search([]),
#         })

#     @http.route('/lika_spareparts/lika_spareparts/objects/<model("lika_spareparts.lika_spareparts"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lika_spareparts.object', {
#             'object': obj
#         })

